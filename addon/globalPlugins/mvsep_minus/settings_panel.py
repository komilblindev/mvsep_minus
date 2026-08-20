# -*- coding: utf-8 -*-
"""
NVDA Settings Panel for MVSEP Minus Add-on.
Provides configuration options for:
- API Token (with 3-language site launcher: UZ, RU, EN, token tester & credit checker)
- Default separation model
- Output directory
- Feedback options
- Language selection (Uzbek, Russian, English).
Compatible with Python 3.7+ (NVDA 2019.3 - 2026.1+).
"""

import os
import wx
import webbrowser
import threading

from .i18n import _t, set_language, get_current_language, format_credit_display
from .config_manager import config
from .models_data import get_minus_models_list, get_all_models_list
from .api_client import test_api_token

try:
    import gui.settingsDialogs
    SettingsPanelBase = gui.settingsDialogs.SettingsPanel
except (ImportError, AttributeError):
    try:
        import gui
        SettingsPanelBase = gui.SettingsPanel
    except (ImportError, AttributeError):
        SettingsPanelBase = wx.Panel


def get_localized_mvsep_url(page="full_api"):
    """
    Returns localized MVSEP URL for the 3 target languages:
    - Uzbek: https://mvsep.com/uz/full_api
    - Russian: https://mvsep.com/ru/full_api
    - English: https://mvsep.com/full_api
    """
    lang_code = get_current_language()
    
    if lang_code == "uz":
        return f"https://mvsep.com/uz/{page}"
    elif lang_code == "ru":
        return f"https://mvsep.com/ru/{page}"
    else:
        return f"https://mvsep.com/{page}"


class MVSEPMinusSettingsPanel(SettingsPanelBase):
    title = _t("settings_category")
    
    def makeSettings(self, settingsSizer):
        self.title = _t("settings_category")
        panel = self
        
        # 1. API Token Box
        token_box = wx.StaticBox(panel, label=_t("api_token_label"))
        token_sizer = wx.StaticBoxSizer(token_box, wx.VERTICAL)
        
        self.token_text = wx.TextCtrl(panel, value=config.get("api_token", ""), style=wx.TE_PASSWORD)
        token_sizer.Add(self.token_text, 0, wx.EXPAND | wx.BOTTOM, 6)
        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.get_token_btn = wx.Button(panel, label=_t("btn_get_api_token"))
        self.get_token_btn.Bind(wx.EVT_BUTTON, self.OnGetToken)
        btn_sizer.Add(self.get_token_btn, 0, wx.RIGHT, 8)
        
        self.test_btn = wx.Button(panel, label=_t("btn_test_token"))
        self.test_btn.Bind(wx.EVT_BUTTON, self.OnTestToken)
        btn_sizer.Add(self.test_btn, 0, wx.RIGHT, 8)
        
        self.credit_btn = wx.Button(panel, label=_t("btn_check_credits"))
        self.credit_btn.Bind(wx.EVT_BUTTON, self.OnCheckCredits)
        btn_sizer.Add(self.credit_btn, 0, wx.RIGHT, 8)
        
        self.show_key_chk = wx.CheckBox(panel, label=_t("show_key_label"))
        self.show_key_chk.Bind(wx.EVT_CHECKBOX, self.OnToggleShowKey)
        btn_sizer.Add(self.show_key_chk, 0, wx.ALIGN_CENTER_VERTICAL)
        token_sizer.Add(btn_sizer, 0, wx.BOTTOM, 6)
        
        help_text = wx.StaticText(panel, label=_t("api_token_help"))
        token_sizer.Add(help_text, 0)
        
        settingsSizer.Add(token_sizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        
        # 2. Default Model
        model_sizer = wx.BoxSizer(wx.HORIZONTAL)
        model_sizer.Add(wx.StaticText(panel, label=_t("default_model_label") + " "), 0, wx.ALIGN_CENTER_VERTICAL)
        
        self.model_choice = wx.Choice(panel)
        self.model_ids = []
        minus_list = get_minus_models_list()
        cur_def = config.get("default_model", "40")
        selected_idx = 0
        for i, (mid, name) in enumerate(minus_list):
            self.model_choice.Append(name)
            self.model_ids.append(mid)
            if str(mid) == str(cur_def):
                selected_idx = i
        self.model_choice.SetSelection(selected_idx)
        model_sizer.Add(self.model_choice, 1, wx.EXPAND)
        settingsSizer.Add(model_sizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        
        # 3. Output Directory
        out_box = wx.StaticBox(panel, label=_t("output_dir_label"))
        out_sizer = wx.StaticBoxSizer(out_box, wx.HORIZONTAL)
        self.out_text = wx.TextCtrl(panel, value=config.get("output_dir", ""))
        out_sizer.Add(self.out_text, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 8)
        self.out_browse = wx.Button(panel, label=_t("browse"))
        self.out_browse.Bind(wx.EVT_BUTTON, self.OnBrowseDir)
        out_sizer.Add(self.out_browse, 0, wx.ALIGN_CENTER_VERTICAL)
        settingsSizer.Add(out_sizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        
        # 4. Feedback Options
        self.announce_chk = wx.CheckBox(panel, label=_t("announce_progress_label"))
        self.announce_chk.SetValue(config.get("announce_progress", True))
        settingsSizer.Add(self.announce_chk, 0, wx.BOTTOM, 5)
        
        self.sound_chk = wx.CheckBox(panel, label=_t("play_sound_label"))
        self.sound_chk.SetValue(config.get("play_sound_on_finish", True))
        settingsSizer.Add(self.sound_chk, 0, wx.BOTTOM, 10)
        
        # 5. Language Choice
        lang_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lang_sizer.Add(wx.StaticText(panel, label=_t("language_label") + " "), 0, wx.ALIGN_CENTER_VERTICAL)
        self.lang_choice = wx.Choice(panel, choices=[
            _t("lang_auto"),
            _t("lang_uz"),
            _t("lang_ru"),
            _t("lang_en")
        ])
        lang_map = {"auto": 0, "uz": 1, "ru": 2, "en": 3}
        cur_lang = config.get("language", "auto")
        self.lang_choice.SetSelection(lang_map.get(cur_lang, 0))
        lang_sizer.Add(self.lang_choice, 1, wx.EXPAND)
        settingsSizer.Add(lang_sizer, 0, wx.EXPAND | wx.BOTTOM, 10)

    def OnGetToken(self, event):
        url = get_localized_mvsep_url("full_api")
        try:
            webbrowser.open(url)
        except Exception:
            os.system(f'start {url}')

    def OnToggleShowKey(self, event):
        val = self.token_text.GetValue()
        if self.show_key_chk.IsChecked():
            wx.MessageBox(_t("api_key_display_text", key=val), _t("api_key_dialog_title"), wx.OK | wx.ICON_INFORMATION, self)
            
    def OnBrowseDir(self, event):
        dlg = wx.DirDialog(self, _t("output_dir_label"), style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.out_text.SetValue(dlg.GetPath())
        dlg.Destroy()
        
    def OnTestToken(self, event):
        token = self.token_text.GetValue().strip()
        if not token:
            wx.MessageBox(_t("msg_no_api_token"), _t("addon_name"), wx.OK | wx.ICON_WARNING, self)
            return
            
        def _test_thread():
            ok, msg = test_api_token(token)
            if ok:
                wx.CallAfter(lambda: wx.MessageBox(_t("token_valid") + f" ({msg})", _t("addon_name"), wx.OK | wx.ICON_INFORMATION, self))
            else:
                wx.CallAfter(lambda: wx.MessageBox(_t("token_invalid", error=msg), _t("addon_name"), wx.OK | wx.ICON_ERROR, self))
                
        t = threading.Thread(target=_test_thread)
        t.daemon = True
        t.start()

    def OnCheckCredits(self, event):
        token = self.token_text.GetValue().strip()
        if not token:
            wx.MessageBox(_t("msg_no_api_token"), _t("addon_name"), wx.OK | wx.ICON_WARNING, self)
            return
            
        def _check_thread():
            ok, msg = test_api_token(token)
            left = format_credit_display(config.get("last_known_credits", "active_free"))
            spent = config.get("last_spent_credits", 1)
            total = config.get("total_separations_count", 0)
            
            if ok:
                body = _t("credit_info_dialog_body", left=left, spent=spent, total=total)
                wx.CallAfter(lambda: wx.MessageBox(body, _t("credit_info_dialog_title"), wx.OK | wx.ICON_INFORMATION, self))
            else:
                wx.CallAfter(lambda: wx.MessageBox(_t("token_invalid", error=msg), _t("addon_name"), wx.OK | wx.ICON_ERROR, self))
                
        t = threading.Thread(target=_check_thread)
        t.daemon = True
        t.start()
        
    def onSave(self):
        config.set("api_token", self.token_text.GetValue().strip())
        
        sel_m = self.model_choice.GetSelection()
        if sel_m != wx.NOT_FOUND and sel_m < len(self.model_ids):
            config.set("default_model", self.model_ids[sel_m])
            
        config.set("output_dir", self.out_text.GetValue().strip())
        config.set("announce_progress", self.announce_chk.IsChecked())
        config.set("play_sound_on_finish", self.sound_chk.IsChecked())
        
        lang_idx = self.lang_choice.GetSelection()
        lang_codes = ["auto", "uz", "ru", "en"]
        selected_lang = lang_codes[lang_idx] if lang_idx < len(lang_codes) else "auto"
        config.set("language", selected_lang)
        set_language(selected_lang)
