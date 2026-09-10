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

from .i18n import _t, set_language, get_current_language, format_credit_display, format_duration
from .config_manager import config, get_history_file_path, get_errors_file_path
from .models_data import get_minus_models_list, get_all_models_list
from .api_client import test_api_token, get_account_file_path, send_error_to_developer, get_server_queue
from .login_dialog import MVSEPAccountDialog
from .site_history_dialog import SiteHistoryDialog

try:
	import ui
except ImportError:
	ui = None

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
		
		# 1. API Token & Multi-Account Box
		token_box = wx.StaticBox(panel, label=_t("api_token_label"))
		token_sizer = wx.StaticBoxSizer(token_box, wx.VERTICAL)
		
		# Account selector row
		acc_row = wx.BoxSizer(wx.HORIZONTAL)
		acc_row.Add(wx.StaticText(panel, label=_t("account_selector_label") + " "), 0, wx.ALIGN_CENTER_VERTICAL)
		self.account_choice = wx.Choice(panel)
		self.account_choice.Bind(wx.EVT_CHOICE, self.OnAccountChanged)
		acc_row.Add(self.account_choice, 1, wx.EXPAND | wx.RIGHT, 8)
		
		self.del_acc_btn = wx.Button(panel, label=_t("btn_delete_account"))
		self.del_acc_btn.Bind(wx.EVT_BUTTON, self.OnDeleteAccount)
		acc_row.Add(self.del_acc_btn, 0, wx.ALIGN_CENTER_VERTICAL)
		token_sizer.Add(acc_row, 0, wx.EXPAND | wx.BOTTOM, 8)
		
		cur_token = config.get("api_token", "")
		self.token_text = wx.TextCtrl(panel, value=cur_token, style=wx.TE_PASSWORD)
		self.token_text_plain = wx.TextCtrl(panel, value=cur_token)
		self.token_text_plain.Hide()
		token_sizer.Add(self.token_text, 0, wx.EXPAND | wx.BOTTOM, 6)
		token_sizer.Add(self.token_text_plain, 0, wx.EXPAND | wx.BOTTOM, 6)
		
		# Row 1: Separate Login & Register buttons, plus Browser
		row1_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.login_btn = wx.Button(panel, label=_t("btn_open_login"))
		self.login_btn.Bind(wx.EVT_BUTTON, self.OnLoginAccount)
		row1_sizer.Add(self.login_btn, 0, wx.RIGHT, 8)
		
		self.register_btn = wx.Button(panel, label=_t("btn_open_register"))
		self.register_btn.Bind(wx.EVT_BUTTON, self.OnRegisterAccount)
		row1_sizer.Add(self.register_btn, 0, wx.RIGHT, 8)
		
		self.get_token_btn = wx.Button(panel, label=_t("btn_get_api_token"))
		self.get_token_btn.Bind(wx.EVT_BUTTON, self.OnGetToken)
		row1_sizer.Add(self.get_token_btn, 0)
		token_sizer.Add(row1_sizer, 0, wx.BOTTOM, 6)
		
		# Row 2: Copy, Test, Credits, Show Key
		row2_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.copy_btn = wx.Button(panel, label=_t("btn_copy_token"))
		self.copy_btn.Bind(wx.EVT_BUTTON, self.OnCopyToken)
		row2_sizer.Add(self.copy_btn, 0, wx.RIGHT, 8)
		
		self.test_btn = wx.Button(panel, label=_t("btn_test_token"))
		self.test_btn.Bind(wx.EVT_BUTTON, self.OnTestToken)
		row2_sizer.Add(self.test_btn, 0, wx.RIGHT, 8)
		
		self.credit_btn = wx.Button(panel, label=_t("btn_check_credits"))
		self.credit_btn.Bind(wx.EVT_BUTTON, self.OnCheckCredits)
		row2_sizer.Add(self.credit_btn, 0, wx.RIGHT, 8)
		
		self.queue_btn = wx.Button(panel, label=_t("btn_check_queue"))
		self.queue_btn.Bind(wx.EVT_BUTTON, self.OnCheckQueue)
		row2_sizer.Add(self.queue_btn, 0, wx.RIGHT, 8)
		
		self.show_key_chk = wx.CheckBox(panel, label=_t("show_key_label"))
		self.show_key_chk.Bind(wx.EVT_CHECKBOX, self.OnToggleShowKey)
		row2_sizer.Add(self.show_key_chk, 0, wx.ALIGN_CENTER_VERTICAL)
		token_sizer.Add(row2_sizer, 0, wx.BOTTOM, 6)
		
		# Row 3: Open Account File & Auto-switch Checkbox
		row3_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.open_file_btn = wx.Button(panel, label=_t("btn_open_account_file"))
		self.open_file_btn.Bind(wx.EVT_BUTTON, self.OnOpenFile)
		row3_sizer.Add(self.open_file_btn, 0, wx.RIGHT, 10)
		
		self.auto_switch_chk = wx.CheckBox(panel, label=_t("auto_switch_account_label"))
		self.auto_switch_chk.SetValue(config.get("auto_switch_account", True))
		row3_sizer.Add(self.auto_switch_chk, 0, wx.ALIGN_CENTER_VERTICAL)
		token_sizer.Add(row3_sizer, 0, wx.BOTTOM, 6)
		
		help_text = wx.StaticText(panel, label=_t("api_token_help"))
		token_sizer.Add(help_text, 0)
		
		settingsSizer.Add(token_sizer, 0, wx.EXPAND | wx.BOTTOM, 10)
		
		# 2. Default Model
		model_sizer = wx.BoxSizer(wx.HORIZONTAL)
		model_sizer.Add(wx.StaticText(panel, label=_t("default_model_label") + " "), 0, wx.ALIGN_CENTER_VERTICAL)
		
		self.model_choice = wx.Choice(panel)
		self.model_ids = []
		minus_list = get_minus_models_list()
		cur_def = config.get("default_model", "39")
		selected_idx = 0
		for i, (mid, name) in enumerate(minus_list):
			self.model_choice.Append(name)
			self.model_ids.append(mid)
			if str(mid) == str(cur_def):
				selected_idx = i
		self.model_choice.SetSelection(selected_idx)
		model_sizer.Add(self.model_choice, 1, wx.EXPAND)
		settingsSizer.Add(model_sizer, 0, wx.EXPAND | wx.BOTTOM, 6)
		
		self.trans_models_chk = wx.CheckBox(panel, label=_t("translate_models_label"))
		self.trans_models_chk.SetValue(config.get("translate_models", False))
		self.trans_models_chk.Bind(wx.EVT_CHECKBOX, self.OnToggleTranslateModels)
		settingsSizer.Add(self.trans_models_chk, 0, wx.BOTTOM, 10)
		
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
		
		# 6. History Retention & Statistics
		hist_box = wx.StaticBox(panel, label=_t("history_stats_title"))
		hist_sizer = wx.StaticBoxSizer(hist_box, wx.VERTICAL)
		
		period_sizer = wx.BoxSizer(wx.HORIZONTAL)
		period_sizer.Add(wx.StaticText(panel, label=_t("history_retention_label") + " "), 0, wx.ALIGN_CENTER_VERTICAL)
		
		self.retention_choice = wx.Choice(panel, choices=[
			_t("period_1week"),
			_t("period_1month"),
			_t("period_3months"),
			_t("period_all")
		])
		self.retention_days_list = [7, 30, 90, 0]
		cur_days = int(config.get("history_retention_days", 30))
		ret_idx = 1
		if cur_days in self.retention_days_list:
			ret_idx = self.retention_days_list.index(cur_days)
		self.retention_choice.SetSelection(ret_idx)
		self.retention_choice.Bind(wx.EVT_CHOICE, self.OnRetentionChanged)
		period_sizer.Add(self.retention_choice, 1, wx.EXPAND)
		hist_sizer.Add(period_sizer, 0, wx.EXPAND | wx.BOTTOM, 6)
		
		self.stats_text = wx.StaticText(panel, label="")
		hist_sizer.Add(self.stats_text, 0, wx.EXPAND | wx.BOTTOM, 6)
		
		hist_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.site_hist_btn = wx.Button(panel, label=_t("btn_open_site_history"))
		self.site_hist_btn.Bind(wx.EVT_BUTTON, self.OnOpenSiteHistory)
		hist_btn_sizer.Add(self.site_hist_btn, 0, wx.RIGHT, 8)
		
		self.open_hist_btn = wx.Button(panel, label=_t("btn_open_history_file"))
		self.open_hist_btn.Bind(wx.EVT_BUTTON, self.OnOpenHistoryFile)
		hist_btn_sizer.Add(self.open_hist_btn, 0, wx.RIGHT, 8)
		
		self.open_err_btn = wx.Button(panel, label=_t("btn_open_errors_file"))
		self.open_err_btn.Bind(wx.EVT_BUTTON, self.OnOpenErrorsFile)
		hist_btn_sizer.Add(self.open_err_btn, 0, wx.RIGHT, 8)
		
		self.send_err_btn = wx.Button(panel, label=_t("btn_send_error_dev"))
		self.send_err_btn.Bind(wx.EVT_BUTTON, self.OnSendErrorDev)
		hist_btn_sizer.Add(self.send_err_btn, 0)
		hist_sizer.Add(hist_btn_sizer, 0)
		
		self.PopulateAccounts()
		
		settingsSizer.Add(hist_sizer, 0, wx.EXPAND | wx.BOTTOM, 10)
		
		self.UpdateStatsDisplay()




	def PopulateAccounts(self):
		self.account_choice.Clear()
		self.account_ids = []
		accs = config.get_accounts()
		sel_idx = 0
		for i, acc in enumerate(accs):
			email = acc.get("email", "user")
			if email == "user":
				email = acc.get("name") or "Asosiy kalit"
			cr = acc.get("credits", "active_free")
			cr_text = format_credit_display(cr)
			disp = f"{i+1}. {email} ({cr_text})"
			self.account_choice.Append(disp)
			self.account_ids.append(acc.get("id"))
			if acc.get("is_active"):
				sel_idx = i
		if self.account_ids:
			self.account_choice.SetSelection(sel_idx)

	def OnAccountChanged(self, event):
		sel = self.account_choice.GetSelection()
		if sel != wx.NOT_FOUND and sel < len(self.account_ids):
			acc_id = self.account_ids[sel]
			config.set_active_account(acc_id)
			active = config.get_active_account()
			if active:
				tok = active.get("api_token", "")
				self.set_token_value(tok)
				if ui and hasattr(ui, 'message'):
					ui.message(f"{_t('status_active')}: {active.get('email', 'account')}")
			self.PopulateAccounts()

	def OnDeleteAccount(self, event):
		sel = self.account_choice.GetSelection()
		if sel != wx.NOT_FOUND and sel < len(self.account_ids):
			acc_id = self.account_ids[sel]
			config.remove_account(acc_id)
			active = config.get_active_account()
			if active:
				self.set_token_value(active.get("api_token", ""))
			else:
				self.set_token_value("")
			self.PopulateAccounts()
			if ui and hasattr(ui, 'message'):
				ui.message(_t("msg_account_deleted"))

	def OnOpenErrorsFile(self, event):
		path = get_errors_file_path()
		if os.path.isfile(path):
			try:
				os.startfile(path)
			except Exception:
				webbrowser.open(path)
		else:
			msg = _t("msg_errors_file_not_found")
			if ui and hasattr(ui, 'message'):
				ui.message(msg)
			wx.MessageBox(msg, _t("addon_name"), wx.OK | wx.ICON_INFORMATION, self)

	def OnSendErrorDev(self, event):
		send_error_to_developer(self)

	def OnToggleTranslateModels(self, event):
		is_trans = self.trans_models_chk.IsChecked()
		cur_sel = self.model_choice.GetSelection()
		chosen_id = self.model_ids[cur_sel] if (cur_sel != wx.NOT_FOUND and cur_sel < len(self.model_ids)) else config.get("default_model", "39")
		
		self.model_choice.Clear()
		self.model_ids = []
		minus_list = get_minus_models_list(translated=is_trans)
		selected_idx = 0
		for i, (mid, name) in enumerate(minus_list):
			self.model_choice.Append(name)
			self.model_ids.append(mid)
			if str(mid) == str(chosen_id):
				selected_idx = i
		self.model_choice.SetSelection(selected_idx)

	def UpdateStatsDisplay(self):
		sel = self.retention_choice.GetSelection()
		days = self.retention_days_list[sel] if (sel != wx.NOT_FOUND and sel < len(self.retention_days_list)) else 30
		stats = config.get_history_stats(days=days)
		
		dur_str = format_duration(stats["total_seconds"])
		count = stats["total_count"]
		spent = stats["total_spent"]
		bal_str = format_credit_display(stats["balance"])
		
		period_names = [_t("period_1week"), _t("period_1month"), _t("period_3months"), _t("period_all")]
		p_name = period_names[sel] if sel < len(period_names) else f"{days} kun"
		
		msg = _t(
			"history_stats_summary",
			period=p_name,
			total_time=dur_str,
			count=count,
			spent=spent,
			balance=bal_str
		)
		self.stats_text.SetLabel(msg)

	def OnRetentionChanged(self, event):
		self.UpdateStatsDisplay()

	def OnOpenSiteHistory(self, event):
		token = self.get_current_token()
		if not token:
			wx.MessageBox(_t("msg_no_api_token"), _t("addon_name"), wx.OK | wx.ICON_WARNING, self)
			return
		dlg = SiteHistoryDialog(self)
		dlg.ShowModal()
		dlg.Destroy()

	def OnCheckQueue(self, event):
		def _worker():
			ok, res = get_server_queue()
			if ok and isinstance(res, dict):
				msg = _t("msg_queue_status", proc=res.get("in_process", 0), prem=res.get("premium", 0), free=res.get("free", 0))
				if ui and hasattr(ui, 'message'):
					ui.message(msg)
				wx.CallAfter(lambda: wx.MessageBox(msg, _t("btn_check_queue"), wx.OK | wx.ICON_INFORMATION, self))
			else:
				err = str(res)
				if ui and hasattr(ui, 'message'):
					ui.message(err)
				wx.CallAfter(lambda: wx.MessageBox(err, _t("btn_check_queue"), wx.OK | wx.ICON_ERROR, self))
		t = threading.Thread(target=_worker)
		t.daemon = True
		t.start()

	def OnOpenHistoryFile(self, event):
		path = get_history_file_path()
		if os.path.isfile(path):
			try:
				os.startfile(path)
			except Exception:
				webbrowser.open(path)
		else:
			msg = _t("msg_history_file_not_found")
			if ui and hasattr(ui, 'message'):
				ui.message(msg)
			wx.MessageBox(msg, _t("addon_name"), wx.OK | wx.ICON_INFORMATION, self)

	def OnGetToken(self, event):
		url = get_localized_mvsep_url("full_api")
		try:
			webbrowser.open(url)
		except Exception:
			os.system(f'start {url}')

	def get_current_token(self):
		if hasattr(self, 'token_text_plain') and self.token_text_plain.IsShown():
			return self.token_text_plain.GetValue().strip()
		return self.token_text.GetValue().strip()

	def set_token_value(self, token):
		self.token_text.SetValue(token)
		if hasattr(self, 'token_text_plain'):
			self.token_text_plain.SetValue(token)

	def OnLoginAccount(self, event):
		dlg = MVSEPAccountDialog(self, mode="login", on_token_saved_callback=self.set_token_value)
		dlg.ShowModal()
		dlg.Destroy()

	def OnRegisterAccount(self, event):
		dlg = MVSEPAccountDialog(self, mode="register", on_token_saved_callback=self.set_token_value)
		dlg.ShowModal()
		dlg.Destroy()

	def OnCopyToken(self, event):
		token = self.get_current_token()
		if not token:
			if ui and hasattr(ui, 'message'):
				ui.message(_t("msg_no_api_token"))
			wx.MessageBox(_t("msg_no_api_token"), _t("addon_name"), wx.OK | wx.ICON_WARNING, self)
			return
		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(wx.TextDataObject(token))
			wx.TheClipboard.Close()
			if ui and hasattr(ui, 'message'):
				ui.message(_t("msg_token_copied"))
			wx.MessageBox(_t("msg_token_copied"), _t("addon_name"), wx.OK | wx.ICON_INFORMATION, self)

	def OnOpenFile(self, event):
		path = get_account_file_path()
		if os.path.isfile(path):
			try:
				os.startfile(path)
			except Exception:
				webbrowser.open(path)
		else:
			msg = _t("msg_account_file_not_found", path=path)
			if ui and hasattr(ui, 'message'):
				ui.message(msg)
			wx.MessageBox(msg, _t("addon_name"), wx.OK | wx.ICON_INFORMATION, self)

	def OnToggleShowKey(self, event):
		is_shown = self.show_key_chk.IsChecked()
		if is_shown:
			val = self.token_text.GetValue()
			self.token_text_plain.SetValue(val)
			self.token_text.Hide()
			self.token_text_plain.Show()
		else:
			val = self.token_text_plain.GetValue()
			self.token_text.SetValue(val)
			self.token_text_plain.Hide()
			self.token_text.Show()
		self.Layout()

	def OnBrowseDir(self, event):
		dlg = wx.DirDialog(self, _t("output_dir_label"), style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
		if dlg.ShowModal() == wx.ID_OK:
			self.out_text.SetValue(dlg.GetPath())
		dlg.Destroy()

	def OnTestToken(self, event):
		token = self.get_current_token()
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
		token = self.get_current_token()
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
		config.set("api_token", self.get_current_token())
		
		sel_m = self.model_choice.GetSelection()
		if sel_m != wx.NOT_FOUND and sel_m < len(self.model_ids):
			config.set("default_model", self.model_ids[sel_m])
		config.set("translate_models", self.trans_models_chk.IsChecked())
		config.set("auto_switch_account", self.auto_switch_chk.IsChecked())
			
		config.set("output_dir", self.out_text.GetValue().strip())
		config.set("announce_progress", self.announce_chk.IsChecked())
		config.set("play_sound_on_finish", self.sound_chk.IsChecked())
		
		lang_idx = self.lang_choice.GetSelection()
		lang_codes = ["auto", "uz", "ru", "en"]
		selected_lang = lang_codes[lang_idx] if lang_idx < len(lang_codes) else "auto"
		config.set("language", selected_lang)
		set_language(selected_lang)
		
		sel_ret = self.retention_choice.GetSelection()
		if sel_ret != wx.NOT_FOUND and sel_ret < len(self.retention_days_list):
			config.set("history_retention_days", self.retention_days_list[sel_ret])
			config.prune_history()
			config.sync_history_file()
