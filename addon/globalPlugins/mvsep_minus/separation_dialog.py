# -*- coding: utf-8 -*-
"""
Interactive wxPython Dialog for MVSEP Minus Separation.
Includes:
- NVDA rising progress beeps (tones.beep) during upload, processing, and download.
- Spoken percentages at key milestones (or continuous based on settings).
- Credit info badge & live credit deduction notice.
- Background thread separation with cancel support.
Compatible with Python 3.7+ (NVDA 2019.3 - 2026.1).
"""

import os
import sys
import threading
import winsound
import wx

from .i18n import _t, get_current_language, format_credit_display
from .config_manager import config
from .models_data import (
    get_minus_models_list,
    get_all_models_list,
    get_model_title,
    DEFAULT_FAVORITES
)
from .api_client import (
    create_separation,
    poll_separation,
    download_file,
    clean_output_filename
)
from .explorer_helper import is_audio_file

try:
    import ui
except ImportError:
    ui = None

try:
    import tones
except ImportError:
    tones = None


def play_progress_beep(percent):
    """Play NVDA rising progress beep (220 Hz to 1760 Hz)."""
    if tones and config.get("play_progress_beeps", True):
        try:
            # Scale pitch from 220Hz (0%) to 1760Hz (100%)
            freq = int(220 + (max(0, min(100, percent)) / 100.0) * (1760 - 220))
            tones.beep(freq, 40)  # 40ms short beep
        except Exception:
            pass


class MinusSeparationDialog(wx.Dialog):
    def __init__(self, parent, initial_file=None):
        title = _t("dialog_title")
        super(MinusSeparationDialog, self).__init__(
            parent,
            title=title,
            size=(580, 500),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        self.initial_file = initial_file
        self.is_running = False
        self.cancel_event = threading.Event()
        self.worker_thread = None
        self.saved_files = []
        self.last_spent_credits = 0
        self.last_left_credits = config.get("last_known_credits", "active_free")
        
        self.InitUI()
        self.Centre()
        
    def InitUI(self):
        panel = self
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 1. File Selection Group
        file_box = wx.StaticBox(panel, label=_t("file_label"))
        file_sizer = wx.StaticBoxSizer(file_box, wx.HORIZONTAL)
        
        self.file_text = wx.TextCtrl(panel, value=self.initial_file or "")
        file_sizer.Add(self.file_text, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 8)
        
        self.browse_btn = wx.Button(panel, label=_t("browse"))
        self.browse_btn.Bind(wx.EVT_BUTTON, self.OnBrowse)
        file_sizer.Add(self.browse_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        
        main_sizer.Add(file_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # 2. Model Selection Group
        model_box = wx.StaticBox(panel, label=_t("model_category"))
        model_sizer = wx.StaticBoxSizer(model_box, wx.VERTICAL)
        
        cat_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cat_choice = wx.Choice(panel, choices=[
            _t("cat_favorites"),
            _t("cat_minus"),
            _t("cat_all")
        ])
        self.cat_choice.SetSelection(0)
        self.cat_choice.Bind(wx.EVT_CHOICE, self.OnCategoryChanged)
        cat_sizer.Add(wx.StaticText(panel, label=_t("model_category") + " "), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        cat_sizer.Add(self.cat_choice, 1, wx.EXPAND)
        model_sizer.Add(cat_sizer, 0, wx.EXPAND | wx.BOTTOM, 8)
        
        model_select_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.model_choice = wx.Choice(panel)
        model_select_sizer.Add(self.model_choice, 1, wx.EXPAND | wx.RIGHT, 8)
        
        self.fav_btn = wx.Button(panel, label=_t("btn_toggle_fav"))
        self.fav_btn.Bind(wx.EVT_BUTTON, self.OnToggleFavorite)
        model_select_sizer.Add(self.fav_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        model_sizer.Add(model_select_sizer, 0, wx.EXPAND)
        
        main_sizer.Add(model_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        # 3. Download Options Group
        opt_box = wx.StaticBox(panel, label=_t("download_options"))
        opt_sizer = wx.StaticBoxSizer(opt_box, wx.HORIZONTAL)
        
        download_modes = [
            _t("opt_minus_only"),
            _t("opt_minus_and_vocal"),
            _t("opt_all_stems")
        ]
        self.dl_choice = wx.Choice(panel, choices=download_modes)
        cur_dl = config.get("download_choice", "minus_only")
        if cur_dl == "minus_and_vocal":
            self.dl_choice.SetSelection(1)
        elif cur_dl == "all":
            self.dl_choice.SetSelection(2)
        else:
            self.dl_choice.SetSelection(0)
        opt_sizer.Add(self.dl_choice, 1, wx.EXPAND | wx.RIGHT, 10)
        
        opt_sizer.Add(wx.StaticText(panel, label=_t("output_format") + " "), 0, wx.ALIGN_CENTER_VERTICAL)
        self.format_choice = wx.Choice(panel, choices=["MP3", "WAV", "FLAC"])
        fmt_idx = int(config.get("output_format", "0"))
        self.format_choice.SetSelection(min(max(fmt_idx, 0), 2))
        opt_sizer.Add(self.format_choice, 0, wx.ALIGN_CENTER_VERTICAL)
        
        main_sizer.Add(opt_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        # 4. Progress & Status
        self.gauge = wx.Gauge(panel, range=100, style=wx.GA_HORIZONTAL)
        main_sizer.Add(self.gauge, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        self.status_label = wx.StaticText(panel, label=_t("status_idle"))
        main_sizer.Add(self.status_label, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        
        # 5. Buttons & Credit info Row
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.credit_badge = wx.StaticText(panel, label=_t("credit_status_badge", status=format_credit_display(config.get("last_known_credits", "active_free"))))
        btn_sizer.Add(self.credit_badge, 1, wx.ALIGN_CENTER_VERTICAL)
        
        self.start_btn = wx.Button(panel, label=_t("btn_start"))
        self.start_btn.SetDefault()
        self.start_btn.Bind(wx.EVT_BUTTON, self.OnStart)
        btn_sizer.Add(self.start_btn, 0, wx.RIGHT, 10)
        
        self.cancel_btn = wx.Button(panel, label=_t("btn_cancel"))
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.cancel_btn.Enable(False)
        btn_sizer.Add(self.cancel_btn, 0, wx.RIGHT, 10)
        
        self.close_btn = wx.Button(panel, label=_t("btn_close"))
        self.close_btn.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
        btn_sizer.Add(self.close_btn, 0)
        
        main_sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        panel.SetSizer(main_sizer)
        self.PopulateModels()
        
    def PopulateModels(self):
        cat_idx = self.cat_choice.GetSelection()
        self.model_choice.Clear()
        self.current_model_ids = []
        
        default_model = config.get("default_model", "40")
        selected_idx = 0
        
        if cat_idx == 0:  # Favorites
            fav_ids = config.get("favorite_models", list(DEFAULT_FAVORITES))
            for mid in fav_ids:
                title = get_model_title(mid)
                self.model_choice.Append(f"⭐ {title}")
                self.current_model_ids.append(mid)
        elif cat_idx == 1:  # Minus & Vocal models
            minus_list = get_minus_models_list()
            for mid, name in minus_list:
                fav_mark = "⭐ " if config.is_favorite(mid) else ""
                self.model_choice.Append(f"{fav_mark}{name}")
                self.current_model_ids.append(mid)
        else:  # All models
            all_list = get_all_models_list()
            for mid, name in all_list:
                fav_mark = "⭐ " if config.is_favorite(mid) else ""
                self.model_choice.Append(f"{fav_mark}{name}")
                self.current_model_ids.append(mid)
                
        if not self.current_model_ids:
            self.model_choice.Append(get_model_title("40"))
            self.current_model_ids.append("40")
            
        for i, mid in enumerate(self.current_model_ids):
            if str(mid) == str(default_model):
                selected_idx = i
                break
        self.model_choice.SetSelection(selected_idx)
        
    def OnCategoryChanged(self, event):
        self.PopulateModels()
        
    def OnToggleFavorite(self, event):
        sel = self.model_choice.GetSelection()
        if sel != wx.NOT_FOUND and sel < len(self.current_model_ids):
            mid = self.current_model_ids[sel]
            added = config.toggle_favorite(mid)
            msg = _t("fav_added") if added else _t("fav_removed")
            self.UpdateStatus(msg)
            if ui:
                ui.message(msg)
            self.PopulateModels()
            
    def OnBrowse(self, event):
        wildcard = "Audio Files (*.mp3;*.wav;*.flac;*.m4a;*.ogg;*.wma;*.aac;*.opus)|*.mp3;*.wav;*.flac;*.m4a;*.ogg;*.wma;*.aac;*.opus|All Files (*.*)|*.*"
        dlg = wx.FileDialog(
            self,
            message=_t("dialog_title"),
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.file_text.SetValue(path)
        dlg.Destroy()
        
    def UpdateStatus(self, text, percent=None, play_beep=True):
        def _update():
            self.status_label.SetLabel(text)
            if percent is not None:
                val = max(0, min(100, int(percent)))
                self.gauge.SetValue(val)
                if play_beep:
                    play_progress_beep(val)
        wx.CallAfter(_update)
        
    def OnStart(self, event):
        if self.is_running:
            return
            
        api_token = config.get("api_token", "").strip()
        if not api_token:
            err_msg = _t("msg_no_api_token")
            wx.MessageBox(err_msg, _t("addon_name"), wx.OK | wx.ICON_WARNING, self)
            if ui:
                ui.message(err_msg)
            return
            
        file_path = self.file_text.GetValue().strip()
        if not file_path or not os.path.isfile(file_path):
            err_msg = _t("msg_no_file_selected")
            wx.MessageBox(err_msg, _t("addon_name"), wx.OK | wx.ICON_WARNING, self)
            if ui:
                ui.message(err_msg)
            return
            
        sel_model = self.model_choice.GetSelection()
        model_id = self.current_model_ids[sel_model] if (sel_model != wx.NOT_FOUND and sel_model < len(self.current_model_ids)) else "40"
        
        fmt_idx = str(self.format_choice.GetSelection())
        dl_sel = self.dl_choice.GetSelection()
        dl_mode = "minus_only" if dl_sel == 0 else ("minus_and_vocal" if dl_sel == 1 else "all")
        
        self.is_running = True
        self.cancel_event.clear()
        self.start_btn.Enable(False)
        self.cancel_btn.Enable(True)
        self.browse_btn.Enable(False)
        self.file_text.Enable(False)
        self.model_choice.Enable(False)
        self.cat_choice.Enable(False)
        self.fav_btn.Enable(False)
        self.gauge.SetValue(0)
        
        model_name = get_model_title(model_id)
        start_msg = _t("msg_starting_separation", model=model_name)
        self.UpdateStatus(start_msg, 0)
        if ui:
            ui.message(start_msg)
            
        self.worker_thread = threading.Thread(
            target=self._run_separation_thread,
            args=(api_token, file_path, model_id, fmt_idx, dl_mode)
        )
        self.worker_thread.daemon = True
        self.worker_thread.start()
        
    def _run_separation_thread(self, api_token, file_path, model_id, output_format, dl_mode):
        announce = config.get("announce_progress", True)
        self.saved_files = []
        spent_credits = 0
        remaining_credits = None
        
        try:
            # Step 1: Upload (0% - 100% of upload, scaled to 0% - 40% overall)
            last_upload_spoken = -20
            def upload_cb(pct):
                nonlocal last_upload_spoken
                msg = _t("status_uploading", percent=pct)
                overall = int(pct * 0.4)
                self.UpdateStatus(msg, overall, play_beep=True)
                if announce and ui and (pct - last_upload_spoken >= 25 or pct == 100):
                    last_upload_spoken = pct
                    ui.message(msg)
            
            self.UpdateStatus(_t("status_reading_file"), 2, play_beep=False)
            sep_res = create_separation(
                api_token,
                file_path,
                sep_type=model_id,
                output_format=output_format,
                progress_callback=upload_cb,
                cancel_event=self.cancel_event
            )
            
            hash_val = sep_res.get("hash")
            if sep_res.get("credits_spent"):
                spent_credits = sep_res["credits_spent"]
            if sep_res.get("credits_left") is not None:
                remaining_credits = sep_res["credits_left"]
                
            if not hash_val:
                raise ValueError("No hash returned from MVSEP server.")
                
            # Step 2: Poll (40% - 80% overall)
            last_poll_spoken = -20
            def poll_cb(pct, status_type):
                nonlocal last_poll_spoken
                overall = 40 + int(pct * 0.4)
                msg = _t("status_processing", percent=pct)
                self.UpdateStatus(msg, overall, play_beep=True)
                if announce and ui and (pct - last_poll_spoken >= 25 or pct in [25, 50, 75, 95]):
                    last_poll_spoken = pct
                    ui.message(msg)
                    
            files, cr_info = poll_separation(
                api_token,
                hash_val,
                progress_callback=poll_cb,
                cancel_event=self.cancel_event,
                max_retries=120,
                interval=6
            )
            
            if cr_info.get("credits_spent"):
                spent_credits = cr_info["credits_spent"]
            if cr_info.get("credits_left") is not None:
                remaining_credits = cr_info["credits_left"]
                
            if not files:
                raise RuntimeError("No separated tracks received.")
                
            # Step 3: Download Tracks (80% - 100% overall)
            target_dir = config.get("output_dir", "").strip()
            if not target_dir or not os.path.isdir(target_dir):
                target_dir = os.path.dirname(os.path.abspath(file_path))
                
            files_to_download = []
            for f_url in files:
                f_str = f_url if isinstance(f_url, str) else (f_url.get("url") or f_url.get("download") or "")
                if not f_str:
                    continue
                lower = f_str.lower()
                is_vocal = "vocal" in lower and "back" not in lower and "instr" not in lower
                is_minus = any(k in lower for k in ["instr", "minus", "music", "accompaniment", "other"]) or not is_vocal
                
                if dl_mode == "minus_only":
                    if is_minus:
                        files_to_download.append((f_str, "minus"))
                elif dl_mode == "minus_and_vocal":
                    if is_minus:
                        files_to_download.append((f_str, "minus"))
                    elif is_vocal:
                        files_to_download.append((f_str, "vocals"))
                else:  # all
                    role = "vocals" if is_vocal else ("minus" if is_minus else "stem")
                    files_to_download.append((f_str, role))
                    
            if not files_to_download:
                first_url = files[0] if isinstance(files[0], str) else (files[0].get("url") or "")
                files_to_download.append((first_url, "minus"))
                
            num_files = len(files_to_download)
            for idx, (f_url, role) in enumerate(files_to_download):
                clean_name = clean_output_filename(f_url, file_path, role)
                out_path = os.path.join(target_dir, clean_name)
                
                last_dl_spoken = -25
                def dl_cb(pct):
                    nonlocal last_dl_spoken
                    item_pct = 80 + int((idx + pct / 100.0) / num_files * 20)
                    msg = _t("status_downloading", filename=clean_name)
                    self.UpdateStatus(msg, item_pct, play_beep=True)
                    if announce and ui and (pct - last_dl_spoken >= 50):
                        last_dl_spoken = pct
                        ui.message(f"{msg} {pct}%")
                    
                download_file(f_url, out_path, progress_callback=dl_cb, cancel_event=self.cancel_event)
                self.saved_files.append(out_path)
                
            # Record credits usage in config accurately
            spent_val = cr_info.get("credits_spent", 0) if isinstance(cr_info, dict) else 0
            if remaining_credits is not None and remaining_credits > 0:
                config.increment_separation_count(spent=spent_val, remaining=remaining_credits)
                self.last_spent_credits = spent_val
                self.last_left_credits = remaining_credits
            else:
                config.increment_separation_count(spent=0, remaining="active_free")
                self.last_spent_credits = 0
                self.last_left_credits = "active_free"
            
            # Completion
            self.UpdateStatus(_t("status_completed"), 100, play_beep=True)
            if config.get("play_sound_on_finish", True):
                try:
                    winsound.MessageBeep(winsound.MB_OK)
                except Exception:
                    pass
                    
            done_msg = _t("msg_done_saved", path=self.saved_files[0] if self.saved_files else target_dir)
            formatted_left = format_credit_display(self.last_left_credits)
            if self.last_spent_credits > 0:
                credit_msg = _t("credit_deducted_notice", spent=self.last_spent_credits, left=formatted_left)
                full_announce = f"{done_msg} {credit_msg}"
            else:
                full_announce = f"{done_msg} ({_t('credit_status_badge', status=formatted_left)})"
                
            if ui:
                ui.message(full_announce)
                
            wx.CallAfter(self._on_success_dialog)
            
        except InterruptedError:
            self.UpdateStatus(_t("status_cancelled"), 0, play_beep=False)
            if ui:
                ui.message(_t("status_cancelled"))
        except PermissionError:
            err_text = _t("msg_quota_exceeded")
            self.UpdateStatus(err_text, 0, play_beep=False)
            if ui:
                ui.message(err_text)
            wx.CallAfter(lambda: wx.MessageBox(err_text, _t("addon_name"), wx.OK | wx.ICON_ERROR, self))
        except Exception as e:
            err_text = str(e)
            self.UpdateStatus(_t("status_error", error=err_text), 0, play_beep=False)
            if ui:
                ui.message(_t("status_error", error=err_text))
            wx.CallAfter(lambda: wx.MessageBox(_t("status_error", error=err_text), _t("addon_name"), wx.OK | wx.ICON_ERROR, self))
        finally:
            self.is_running = False
            wx.CallAfter(self._reset_controls)
            
    def _on_success_dialog(self):
        if not self.saved_files:
            return
        saved_p = self.saved_files[0]
        formatted_left = format_credit_display(self.last_left_credits)
        if self.last_spent_credits > 0:
            credit_notice = _t("credit_deducted_notice", spent=self.last_spent_credits, left=formatted_left)
        else:
            credit_notice = _t("credit_status_badge", status=formatted_left)
            
        dlg = wx.MessageDialog(
            self,
            _t("msg_done_saved", path=saved_p) + "\n\n" + credit_notice + "\n\n" + _t("open_result_folder") + "?",
            _t("addon_name"),
            wx.YES_NO | wx.ICON_INFORMATION
        )
        if dlg.ShowModal() == wx.ID_YES:
            try:
                os.system(f'explorer /select,"{os.path.abspath(saved_p)}"')
            except Exception:
                pass
        dlg.Destroy()
        
    def _reset_controls(self):
        self.start_btn.Enable(True)
        self.cancel_btn.Enable(False)
        self.browse_btn.Enable(True)
        self.file_text.Enable(True)
        self.model_choice.Enable(True)
        self.cat_choice.Enable(True)
        self.fav_btn.Enable(True)
        self.credit_badge.SetLabel(_t("credit_status_badge", status=format_credit_display(self.last_left_credits)))
        
    def OnCancel(self, event):
        if self.is_running:
            self.cancel_event.set()
            self.UpdateStatus(_t("status_cancelled"), 0, play_beep=False)
