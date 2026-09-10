# -*- coding: utf-8 -*-
"""
Site Separation History Dialog for MVSEP Minus NVDA Add-on.
Displays previously separated tracks directly from https://mvsep.com/api/app/separation_history
and allows downloading files directly to local computer.
"""

import os
import time
import threading
import urllib.request
import json
import wx

from .i18n import _t
from .config_manager import config
from .api_client import get_site_separation_history, download_file, clean_output_filename, _create_ssl_context, MVSEP_GET_URL

try:
	import ui
except ImportError:
	ui = None

try:
	import tones
except ImportError:
	tones = None

try:
	import winsound
except ImportError:
	winsound = None


def play_progress_beep(percent):
	"""Play NVDA rising progress beep (220 Hz to 1760 Hz)."""
	if tones and config.get("play_progress_beeps", True):
		try:
			freq = int(220 + (max(0, min(100, percent)) / 100.0) * (1760 - 220))
			tones.beep(freq, 40)
		except Exception:
			pass


def _speak(text):
	if ui and hasattr(ui, "message"):
		ui.message(text)


class SiteHistoryDialog(wx.Dialog):
	def __init__(self, parent):
		super(SiteHistoryDialog, self).__init__(
			parent,
			title=_t("dialog_site_history_title"),
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
		)
		self.parent = parent
		self.items = []
		self.cancel_download = threading.Event()
		self.is_downloading = False

		self.InitUI()
		wx.CallAfter(self.LoadHistory)

	def InitUI(self):
		panel = wx.Panel(self)
		main_sizer = wx.BoxSizer(wx.VERTICAL)

		# Label
		lbl = wx.StaticText(panel, label=_t("history_list_label"))
		main_sizer.Add(lbl, 0, wx.ALL, 10)

		# List of tracks
		self.track_list = wx.ListBox(panel, style=wx.LB_SINGLE)
		main_sizer.Add(self.track_list, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

		# Status label
		self.status_lbl = wx.StaticText(panel, label="")
		main_sizer.Add(self.status_lbl, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

		# Buttons
		btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

		self.dl_btn = wx.Button(panel, label=_t("btn_download_selected"))
		self.dl_btn.SetDefault()
		self.dl_btn.Bind(wx.EVT_BUTTON, self.OnDownloadSelected)
		btn_sizer.Add(self.dl_btn, 0, wx.RIGHT, 8)

		self.refresh_btn = wx.Button(panel, label=_t("btn_refresh_history"))
		self.refresh_btn.Bind(wx.EVT_BUTTON, lambda evt: self.LoadHistory())
		btn_sizer.Add(self.refresh_btn, 0, wx.RIGHT, 8)

		self.close_btn = wx.Button(panel, wx.ID_CANCEL, label=_t("btn_close"))
		self.close_btn.Bind(wx.EVT_BUTTON, self.OnClose)
		btn_sizer.Add(self.close_btn, 0)

		main_sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

		panel.SetSizer(main_sizer)
		self.SetSize((550, 420))
		self.CenterOnParent()

	def LoadHistory(self):
		token = config.get("api_token", "").strip()
		if not token:
			wx.MessageBox(_t("msg_no_api_token"), _t("addon_name"), wx.OK | wx.ICON_WARNING, self)
			return

		self.track_list.Clear()
		self.status_lbl.SetLabel(_t("msg_loading_history"))
		self.dl_btn.Enable(False)
		_speak(_t("msg_loading_history"))

		def _worker():
			ok, res = get_site_separation_history(token)
			wx.CallAfter(self._on_history_loaded, ok, res)

		t = threading.Thread(target=_worker)
		t.daemon = True
		t.start()

	def _on_history_loaded(self, ok, result):
		self.dl_btn.Enable(True)
		if not ok or not result:
			msg = _t("msg_no_history_found")
			self.status_lbl.SetLabel(msg)
			_speak(msg)
			return

		self.items = result
		self.track_list.Clear()

		for idx, it in enumerate(self.items):
			date_str = it.get("created_at", "")
			algo = it.get("algorithm", {}).get("name", "Model")
			hash_val = it.get("hash", "")
			# Clean filename from hash
			parts = hash_val.split("-")
			song_name = "-".join(parts[2:]) if len(parts) >= 3 else hash_val
			if not song_name:
				song_name = hash_val
			display_text = f"{date_str} - {song_name} ({algo})"
			self.track_list.Append(display_text)

		if self.items:
			self.track_list.SetSelection(0)
			status = _t("msg_total_tracks_count", count=len(self.items))
			self.status_lbl.SetLabel(status)
			_speak(f"{status}. " + self.track_list.GetString(0))

	def OnDownloadSelected(self, event):
		if self.is_downloading:
			return

		sel = self.track_list.GetSelection()
		if sel == wx.NOT_FOUND or sel >= len(self.items):
			return

		it = self.items[sel]
		hash_val = it.get("hash", "")
		if not hash_val:
			return

		token = config.get("api_token", "").strip()
		parts = hash_val.split("-")
		song_name = "-".join(parts[2:]) if len(parts) >= 3 else hash_val

		msg = _t("msg_downloading_history_track", name=song_name)
		self.status_lbl.SetLabel(msg)
		_speak(msg)
		self.is_downloading = True
		self.dl_btn.Enable(False)
		self.cancel_download.clear()

		def _worker():
			target_dir = config.get("output_dir", "").strip()
			if not target_dir or not os.path.isdir(target_dir):
				user_profile = os.environ.get('USERPROFILE', os.path.expanduser('~'))
				target_dir = os.path.join(user_profile, 'Downloads', 'MVSEP_Minus')
				os.makedirs(target_dir, exist_ok=True)

			url = f"{MVSEP_GET_URL}?hash={hash_val}&api_token={token}"
			try:
				ctx = _create_ssl_context()
				req = urllib.request.Request(url, headers={"User-Agent": "NVDA-MVSEP-Minus/1.0"})
				with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
					data = json.loads(resp.read().decode("utf-8", errors="ignore"))
					files = data.get("data", {}).get("files", [])
					if not files:
						wx.CallAfter(self._on_download_finished, False, _t("msg_history_file_expired"))
						return

					saved = []
					for f in files:
						f_url = f.get("url")
						if not f_url:
							continue
						f_type = f.get("type", "minus").lower()
						clean_name = clean_output_filename(f_url, song_name, f_type)
						out_path = os.path.join(target_dir, clean_name)
						last_pct = [-1]
						def on_progress(pct):
							if pct != last_pct[0]:
								last_pct[0] = pct
								play_progress_beep(pct)
						try:
							download_file(f_url, out_path, cancel_event=self.cancel_download, progress_callback=on_progress)
							saved.append(out_path)
						except urllib.error.HTTPError as he:
							if he.code == 404:
								wx.CallAfter(self._on_download_finished, False, _t("msg_history_file_expired"))
								return
							raise he

					wx.CallAfter(self._on_download_finished, True, _t("msg_history_download_success"))
			except Exception as ex:
				wx.CallAfter(self._on_download_finished, False, str(ex))

		t = threading.Thread(target=_worker)
		t.daemon = True
		t.start()

	def _on_download_finished(self, ok, msg):
		self.is_downloading = False
		self.dl_btn.Enable(True)
		self.status_lbl.SetLabel(msg)
		_speak(msg)
		if ok:
			play_progress_beep(100)
			if winsound and config.get("play_completion_sound", True):
				try:
					winsound.MessageBeep(winsound.MB_OK)
				except Exception:
					pass
			wx.MessageBox(msg, _t("addon_name"), wx.OK | wx.ICON_INFORMATION, self)
		else:
			wx.MessageBox(msg, _t("addon_name"), wx.OK | wx.ICON_WARNING, self)

	def OnClose(self, event):
		if self.is_downloading:
			self.cancel_download.set()
		self.Destroy()
