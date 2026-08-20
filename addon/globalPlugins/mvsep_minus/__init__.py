# -*- coding: utf-8 -*-
"""
MVSEP Minus Creator - Global Plugin for NVDA
Supports NVDA 2019.3 up to 2026.1+.
Fully customizable gestures via NVDA Menu -> Preferences -> Input Gestures (Boshqaruv tugmalari).
"""

import os
import sys
import threading
import wx

import globalPluginHandler
import gui
import ui
from scriptHandler import script

from .i18n import _t, set_language, format_credit_display
from .config_manager import config
from .explorer_helper import get_selected_file_in_explorer, is_audio_file
from .separation_dialog import MinusSeparationDialog
from .settings_panel import MVSEPMinusSettingsPanel
from .api_client import test_api_token


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _t("addon_name")
    
    __gestures__ = {
        "kb:NVDA+alt+m": "createMinus",
        "kb:NVDA+alt+k": "checkCredits",
        "kb:NVDA+alt+shift+m": "openSettings",
    }
    
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        
        lang = config.get("language", "auto")
        set_language(lang)
        self.scriptCategory = _t("addon_name")
        
        try:
            import gui.settingsDialogs
            if hasattr(gui.settingsDialogs, 'NVDASettingsDialog'):
                gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(MVSEPMinusSettingsPanel)
        except Exception:
            try:
                if hasattr(gui, 'NVDASettingsDialog'):
                    gui.NVDASettingsDialog.categoryClasses.append(MVSEPMinusSettingsPanel)
            except Exception:
                pass
            
        self.create_menu_items()

    def create_menu_items(self):
        try:
            tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
            
            self.create_minus_item = tools_menu.Append(
                wx.ID_ANY,
                _t("menu_create_minus"),
                _t("menu_create_minus_desc")
            )
            gui.mainFrame.sysTrayIcon.Bind(
                wx.EVT_MENU,
                self.on_menu_create_minus,
                self.create_minus_item
            )
            
            self.check_credits_item = tools_menu.Append(
                wx.ID_ANY,
                _t("menu_check_credits"),
                _t("menu_check_credits_desc")
            )
            gui.mainFrame.sysTrayIcon.Bind(
                wx.EVT_MENU,
                self.on_menu_check_credits,
                self.check_credits_item
            )
            
            self.settings_item = tools_menu.Append(
                wx.ID_ANY,
                _t("menu_settings"),
                _t("menu_settings_desc")
            )
            gui.mainFrame.sysTrayIcon.Bind(
                wx.EVT_MENU,
                self.on_menu_settings,
                self.settings_item
            )
        except Exception:
            pass

    def terminate(self):
        try:
            import gui.settingsDialogs
            if hasattr(gui.settingsDialogs, 'NVDASettingsDialog'):
                if MVSEPMinusSettingsPanel in gui.settingsDialogs.NVDASettingsDialog.categoryClasses:
                    gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(MVSEPMinusSettingsPanel)
        except Exception:
            try:
                if hasattr(gui, 'NVDASettingsDialog'):
                    if MVSEPMinusSettingsPanel in gui.NVDASettingsDialog.categoryClasses:
                        gui.NVDASettingsDialog.categoryClasses.remove(MVSEPMinusSettingsPanel)
            except Exception:
                pass
        super(GlobalPlugin, self).terminate()

    def on_menu_create_minus(self, event):
        self.script_createMinus(None)

    def on_menu_check_credits(self, event):
        self.script_checkCredits(None)

    def on_menu_settings(self, event):
        self.open_settings_dialog()

    def open_settings_dialog(self):
        try:
            import gui.settingsDialogs
            if hasattr(gui.settingsDialogs, 'NVDASettingsDialog'):
                gui.mainFrame.onSetGeneralSettings(None)
            else:
                dlg = wx.Dialog(gui.mainFrame, title=_t("settings_category"), size=(520, 480))
                panel = MVSEPMinusSettingsPanel(dlg)
                sizer = wx.BoxSizer(wx.VERTICAL)
                panel_sizer = wx.BoxSizer(wx.VERTICAL)
                panel.makeSettings(panel_sizer)
                sizer.Add(panel_sizer, 1, wx.EXPAND | wx.ALL, 10)
                
                btn_sizer = dlg.CreateButtonSizer(wx.OK | wx.CANCEL)
                sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
                dlg.SetSizer(sizer)
                
                if dlg.ShowModal() == wx.ID_OK:
                    panel.onSave()
                dlg.Destroy()
        except Exception:
            pass

    @script(
        description=_t("menu_create_minus_desc"),
        category=_t("addon_name")
    )
    def script_createMinus(self, gesture):
        """Audio faylni vokal va instrumentalga ajratib minus yaratish."""
        selected_file = get_selected_file_in_explorer()
        
        def _open_dialog():
            dlg = MinusSeparationDialog(gui.mainFrame, initial_file=selected_file)
            dlg.ShowModal()
            dlg.Destroy()
            
        wx.CallAfter(_open_dialog)

    @script(
        description=_t("menu_check_credits_desc"),
        category=_t("addon_name")
    )
    def script_checkCredits(self, gesture):
        """MVSEP hisobidagi qolgan kreditlar va balansni tekshirish."""
        token = config.get("api_token", "").strip()
        if not token:
            ui.message(_t("msg_no_api_token"))
            return
            
        ui.message(_t("credit_checking"))
        
        def _check():
            ok, msg = test_api_token(token)
            left = format_credit_display(config.get("last_known_credits", "active_free"))
            total = config.get("total_separations_count", 0)
            if ok:
                speech = _t("credit_balance_speech", left=left, total=total)
                ui.message(speech)
            else:
                ui.message(_t("token_invalid", error=msg))
                
        t = threading.Thread(target=_check)
        t.daemon = True
        t.start()

    @script(
        description=_t("menu_settings_desc"),
        category=_t("addon_name")
    )
    def script_openSettings(self, gesture):
        """MVSEP API kaliti va minus parametrlarini sozlash."""
        wx.CallAfter(self.open_settings_dialog)
