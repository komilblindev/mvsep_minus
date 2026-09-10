# -*- coding: utf-8 -*-
"""
MVSEP Account and API Key Dialog for NVDA Add-on.
"""

import os
import sys
import threading
import webbrowser
import wx

try:
	import ui
except ImportError:
	ui = None

from .i18n import _t, format_credit_display, get_current_language
from .config_manager import config
from .api_client import (
	login_mvsep,
	register_mvsep,
	save_account_to_downloads,
	get_account_file_path
)


def _speak(text):
	if ui and hasattr(ui, 'message'):
		ui.message(text)


class MVSEPAccountDialog(wx.Dialog):
	def __init__(self, parent, mode="login", on_token_saved_callback=None):
		title = _t("dialog_register_title") if mode == "register" else _t("dialog_login_title")
		super(MVSEPAccountDialog, self).__init__(
			parent,
			title=title,
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
		)
		self.on_token_saved_callback = on_token_saved_callback
		self.is_busy = False

		self.panel = wx.Panel(self)
		main_sizer = wx.BoxSizer(wx.VERTICAL)

		# 1. Mode selector (Radio buttons)
		mode_box = wx.StaticBox(self.panel, label=_t("login_dialog_title"))
		mode_sizer = wx.StaticBoxSizer(mode_box, wx.VERTICAL)

		self.mode_login_rb = wx.RadioButton(self.panel, label=_t("mode_login"), style=wx.RB_GROUP)
		self.mode_login_rb.Bind(wx.EVT_RADIOBUTTON, self.on_mode_change)
		mode_sizer.Add(self.mode_login_rb, 0, wx.BOTTOM, 5)

		self.mode_register_rb = wx.RadioButton(self.panel, label=_t("mode_register"))
		self.mode_register_rb.Bind(wx.EVT_RADIOBUTTON, self.on_mode_change)
		mode_sizer.Add(self.mode_register_rb, 0, wx.BOTTOM, 5)
		
		if mode == "register":
			self.mode_register_rb.SetValue(True)
			self.mode_login_rb.SetValue(False)
		else:
			self.mode_login_rb.SetValue(True)
			self.mode_register_rb.SetValue(False)

		main_sizer.Add(mode_sizer, 0, wx.EXPAND | wx.ALL, 10)

		# 2. Form Fields
		form_sizer = wx.BoxSizer(wx.VERTICAL)

		# Name (Register only)
		self.name_label = wx.StaticText(self.panel, label=_t("name_label"))
		self.name_ctrl = wx.TextCtrl(self.panel)
		form_sizer.Add(self.name_label, 0, wx.BOTTOM, 2)
		form_sizer.Add(self.name_ctrl, 0, wx.EXPAND | wx.BOTTOM, 8)

		# Email
		self.email_label = wx.StaticText(self.panel, label=_t("email_label"))
		self.email_ctrl = wx.TextCtrl(self.panel)
		form_sizer.Add(self.email_label, 0, wx.BOTTOM, 2)
		form_sizer.Add(self.email_ctrl, 0, wx.EXPAND | wx.BOTTOM, 8)

		# Password (with Password and Plain versions for Show/Hide)
		self.password_label = wx.StaticText(self.panel, label=_t("password_label"))
		self.password_ctrl = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD)
		self.password_plain_ctrl = wx.TextCtrl(self.panel)
		self.password_plain_ctrl.Hide()
		form_sizer.Add(self.password_label, 0, wx.BOTTOM, 2)
		form_sizer.Add(self.password_ctrl, 0, wx.EXPAND | wx.BOTTOM, 8)
		form_sizer.Add(self.password_plain_ctrl, 0, wx.EXPAND | wx.BOTTOM, 8)

		# Password Confirm (Register only)
		self.password_confirm_label = wx.StaticText(self.panel, label=_t("password_confirm_label"))
		self.password_confirm_ctrl = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD)
		self.password_confirm_plain_ctrl = wx.TextCtrl(self.panel)
		self.password_confirm_plain_ctrl.Hide()
		form_sizer.Add(self.password_confirm_label, 0, wx.BOTTOM, 2)
		form_sizer.Add(self.password_confirm_ctrl, 0, wx.EXPAND | wx.BOTTOM, 8)
		form_sizer.Add(self.password_confirm_plain_ctrl, 0, wx.EXPAND | wx.BOTTOM, 8)

		# Show Password Checkbox
		self.show_pwd_chk = wx.CheckBox(self.panel, label=_t("show_password_label"))
		self.show_pwd_chk.Bind(wx.EVT_CHECKBOX, self.on_toggle_show_password)
		form_sizer.Add(self.show_pwd_chk, 0, wx.BOTTOM, 8)

		# Save to Downloads Checkbox
		self.save_account_chk = wx.CheckBox(self.panel, label=_t("save_account_label"))
		self.save_account_chk.SetValue(True)
		form_sizer.Add(self.save_account_chk, 0, wx.BOTTOM, 12)

		main_sizer.Add(form_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

		# 3. Action Buttons
		btn_sizer = wx.BoxSizer(wx.VERTICAL)

		self.action_btn = wx.Button(self.panel, label=_t("btn_do_login"))
		self.action_btn.Bind(wx.EVT_BUTTON, self.on_action_clicked)
		btn_sizer.Add(self.action_btn, 0, wx.EXPAND | wx.BOTTOM, 6)

		self.browser_btn = wx.Button(self.panel, label=_t("btn_open_browser_api"))
		self.browser_btn.Bind(wx.EVT_BUTTON, self.on_open_browser)
		btn_sizer.Add(self.browser_btn, 0, wx.EXPAND | wx.BOTTOM, 6)

		self.close_btn = wx.Button(self.panel, wx.ID_CANCEL, label=_t("btn_close"))
		btn_sizer.Add(self.close_btn, 0, wx.EXPAND)

		main_sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 10)

		self.panel.SetSizer(main_sizer)
		main_sizer.Fit(self)
		self.CenterOnParent()

		self.update_ui_state()
		if mode == "register":
			wx.CallAfter(self.name_ctrl.SetFocus)
		else:
			wx.CallAfter(self.email_ctrl.SetFocus)

	def get_password(self):
		if self.show_pwd_chk.IsChecked():
			return self.password_plain_ctrl.GetValue()
		return self.password_ctrl.GetValue()

	def get_password_confirm(self):
		if self.show_pwd_chk.IsChecked():
			return self.password_confirm_plain_ctrl.GetValue()
		return self.password_confirm_ctrl.GetValue()

	def on_toggle_show_password(self, event):
		show = self.show_pwd_chk.IsChecked()
		if show:
			pwd = self.password_ctrl.GetValue()
			self.password_plain_ctrl.SetValue(pwd)
			self.password_ctrl.Hide()
			self.password_plain_ctrl.Show()

			c_pwd = self.password_confirm_ctrl.GetValue()
			self.password_confirm_plain_ctrl.SetValue(c_pwd)
			self.password_confirm_ctrl.Hide()
			if self.mode_register_rb.GetValue():
				self.password_confirm_plain_ctrl.Show()
		else:
			pwd = self.password_plain_ctrl.GetValue()
			self.password_ctrl.SetValue(pwd)
			self.password_plain_ctrl.Hide()
			self.password_ctrl.Show()

			c_pwd = self.password_confirm_plain_ctrl.GetValue()
			self.password_confirm_ctrl.SetValue(c_pwd)
			self.password_confirm_plain_ctrl.Hide()
			if self.mode_register_rb.GetValue():
				self.password_confirm_ctrl.Show()

		self.panel.Layout()

	def on_mode_change(self, event):
		is_reg = self.mode_register_rb.GetValue()
		self.SetTitle(_t("dialog_register_title") if is_reg else _t("dialog_login_title"))
		self.update_ui_state()

	def update_ui_state(self):
		is_reg = self.mode_register_rb.GetValue()

		self.name_label.Show(is_reg)
		self.name_ctrl.Show(is_reg)

		self.password_confirm_label.Show(is_reg)
		if self.show_pwd_chk.IsChecked():
			self.password_confirm_ctrl.Hide()
			self.password_confirm_plain_ctrl.Show(is_reg)
		else:
			self.password_confirm_plain_ctrl.Hide()
			self.password_confirm_ctrl.Show(is_reg)

		if is_reg:
			self.action_btn.SetLabel(_t("btn_do_register"))
		else:
			self.action_btn.SetLabel(_t("btn_do_login"))

		self.panel.Layout()

	def on_open_browser(self, event):
		lang_code = get_current_language()
		if lang_code == "uz":
			url = "https://mvsep.com/uz/full_api"
		elif lang_code == "ru":
			url = "https://mvsep.com/ru/full_api"
		else:
			url = "https://mvsep.com/full_api"
		try:
			webbrowser.open(url)
		except Exception:
			os.system(f'start {url}')

	def on_action_clicked(self, event):
		if self.is_busy:
			return

		is_reg = self.mode_register_rb.GetValue()
		email = self.email_ctrl.GetValue().strip()
		pwd = self.get_password()

		if not email or not pwd:
			_speak(_t("err_fill_all_fields"))
			wx.MessageBox(_t("err_fill_all_fields"), _t("addon_name"), wx.OK | wx.ICON_WARNING, self)
			return

		if len(pwd) < 6:
			_speak(_t("err_pwd_short"))
			wx.MessageBox(_t("err_pwd_short"), _t("addon_name"), wx.OK | wx.ICON_WARNING, self)
			return

		if is_reg:
			name = self.name_ctrl.GetValue().strip()
			c_pwd = self.get_password_confirm()
			if not name:
				_speak(_t("err_fill_all_fields"))
				wx.MessageBox(_t("err_fill_all_fields"), _t("addon_name"), wx.OK | wx.ICON_WARNING, self)
				return
			if pwd != c_pwd:
				_speak(_t("err_pwd_mismatch"))
				wx.MessageBox(_t("err_pwd_mismatch"), _t("addon_name"), wx.OK | wx.ICON_WARNING, self)
				return

			self.start_register_thread(name, email, pwd, c_pwd)
		else:
			self.start_login_thread(email, pwd)

	def start_login_thread(self, email, pwd):
		self.is_busy = True
		self.action_btn.Enable(False)
		_speak(_t("login_in_progress"))

		def _worker():
			ok, result = login_mvsep(email, pwd)
			wx.CallAfter(self._on_login_finished, ok, result, email, pwd)

		t = threading.Thread(target=_worker)
		t.daemon = True
		t.start()

	def _on_login_finished(self, ok, result, email, pwd):
		self.is_busy = False
		self.action_btn.Enable(True)

		if ok and isinstance(result, dict):
			token = result.get("api_token", "").strip()
			credits_raw = result.get("premium_minutes", 0)
			credits_str = format_credit_display(credits_raw)

			if token:
				config.set("api_token", token)
				config.set("last_known_credits", credits_raw)
				config.add_or_update_account(email, token, name="", credits=credits_str)
				config.save()

			# Save credentials to Downloads if checkbox enabled
			if self.save_account_chk.IsChecked():
				saved_path = save_account_to_downloads(email, pwd, token, credits_str)
				if saved_path:
					_speak(_t("account_saved_to_path"))

			msg = _t("login_success", credits=credits_str)
			_speak(msg)
			wx.MessageBox(msg, _t("addon_name"), wx.OK | wx.ICON_INFORMATION, self)

			if self.on_token_saved_callback:
				self.on_token_saved_callback(token)

			self.EndModal(wx.ID_OK)
		else:
			err_msg = str(result)
			_speak(_t("token_invalid", error=err_msg))
			wx.MessageBox(_t("token_invalid", error=err_msg), _t("addon_name"), wx.OK | wx.ICON_ERROR, self)

	def start_register_thread(self, name, email, pwd, c_pwd):
		self.is_busy = True
		self.action_btn.Enable(False)
		_speak(_t("register_in_progress"))

		def _worker():
			ok, result = register_mvsep(name, email, pwd, c_pwd)
			wx.CallAfter(self._on_register_finished, ok, result, email, pwd)

		t = threading.Thread(target=_worker)
		t.daemon = True
		t.start()

	def _on_register_finished(self, ok, result, email, pwd):
		self.is_busy = False
		self.action_btn.Enable(True)

		if ok:
			# Save to downloads right away so user doesn't lose credentials
			if self.save_account_chk.IsChecked():
				saved_path = save_account_to_downloads(email, pwd, api_token=None, credits_info="Pending email verification")
				if saved_path:
					_speak(_t("account_saved_to_path"))

			msg = _t("register_success")
			_speak(msg)
			wx.MessageBox(msg, _t("addon_name"), wx.OK | wx.ICON_INFORMATION, self)

			# Switch to login mode
			self.mode_login_rb.SetValue(True)
			self.update_ui_state()
		else:
			err_msg = str(result)
			_speak(_t("status_error", error=err_msg))
			wx.MessageBox(_t("status_error", error=err_msg), _t("addon_name"), wx.OK | wx.ICON_ERROR, self)
