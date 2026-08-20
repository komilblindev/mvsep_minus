# -*- coding: utf-8 -*-
"""
Ultra-Robust Windows Explorer & Desktop Active File Detection for NVDA.
Supports:
1. win32com (if available)
2. comtypes (NVDA's native COM client)
3. NVDA UIA / IAccessible Focus Object
4. Explorer Window Folder Path + Focused Item Name
5. Windows Clipboard HDROP (Copied files)
Compatible with Windows 7, 8, 10, 11 and NVDA 2019.3 - 2026.1+.
"""

import os
import sys
import ctypes
import time

AUDIO_EXTENSIONS = {
    ".mp3", ".wav", ".flac", ".m4a", ".ogg", ".wma", ".aac", ".opus",
    ".aiff", ".aif", ".ape", ".wv", ".mp4", ".mkv", ".webm"
}


def is_audio_file(file_path):
    """Check if file has an audio extension and exists."""
    if not file_path or not isinstance(file_path, str):
        return False
    clean_path = file_path.strip().strip('"\'')
    ext = os.path.splitext(clean_path)[1].lower()
    return ext in AUDIO_EXTENSIONS and os.path.isfile(clean_path)


def _get_via_win32com():
    """Try getting selected file via win32com if installed."""
    try:
        import win32com.client
        shell = win32com.client.Dispatch("Shell.Application")
        windows = shell.Windows()
        for i in range(windows.Count):
            try:
                win = windows.Item(i)
                doc = win.Document
                
                # Check FocusedItem
                try:
                    f = doc.FocusedItem
                    if f and hasattr(f, 'Path') and is_audio_file(f.Path):
                        return f.Path
                except Exception:
                    pass
                
                # Check SelectedItems
                try:
                    sel = doc.SelectedItems()
                    for s_idx in range(sel.Count):
                        item = sel.Item(s_idx)
                        if item and hasattr(item, 'Path') and is_audio_file(item.Path):
                            return item.Path
                except Exception:
                    pass
            except Exception:
                continue
    except Exception:
        pass
    return None


def _get_via_comtypes():
    """Try getting selected file via NVDA native comtypes."""
    try:
        import comtypes.client
        shell = comtypes.client.CreateObject("Shell.Application")
        windows = shell.Windows()
        for i in range(windows.Count):
            try:
                win = windows.Item(i)
                doc = win.Document
                
                # Check FocusedItem
                try:
                    f = doc.FocusedItem
                    if f:
                        path = getattr(f, 'Path', None)
                        if path and is_audio_file(path):
                            return path
                except Exception:
                    pass
                
                # Check SelectedItems
                try:
                    sel = doc.SelectedItems()
                    if sel:
                        count = getattr(sel, 'Count', 0)
                        for s_idx in range(count):
                            item = sel.Item(s_idx)
                            path = getattr(item, 'Path', None)
                            if path and is_audio_file(path):
                                return path
                except Exception:
                    pass
            except Exception:
                continue
    except Exception:
        pass
    return None


def _get_via_nvda_focus():
    """Try getting selected file from NVDA's current focus object."""
    try:
        import api
        obj = api.getFocusObject()
        if not obj:
            return None
            
        # 1. Direct path in value or name
        val = getattr(obj, 'value', None)
        if val and is_audio_file(val):
            return val
            
        name = getattr(obj, 'name', None)
        if name and is_audio_file(name):
            return name
            
        # 2. Check if name is audio filename and match with active Explorer window
        if name and any(name.lower().endswith(ext) for ext in AUDIO_EXTENSIONS):
            # Check all open Explorer folder paths
            folder_candidates = []
            try:
                import comtypes.client
                shell = comtypes.client.CreateObject("Shell.Application")
                for i in range(shell.Windows().Count):
                    try:
                        w = shell.Windows().Item(i)
                        f_path = w.Document.Folder.Self.Path
                        if f_path and os.path.isdir(f_path):
                            folder_candidates.append(f_path)
                    except Exception:
                        pass
            except Exception:
                pass
                
            for fc in folder_candidates:
                candidate = os.path.join(fc, name)
                if is_audio_file(candidate):
                    return candidate
    except Exception:
        pass
    return None


def _get_via_clipboard_hdrop():
    """Try getting file from Windows clipboard CF_HDROP."""
    try:
        import winUser
        CF_HDROP = 15
        if winUser.OpenClipboard(0):
            try:
                hDrop = winUser.GetClipboardData(CF_HDROP)
                if hDrop:
                    shell32 = ctypes.windll.shell32
                    count = shell32.DragQueryFileW(hDrop, 0xFFFFFFFF, None, 0)
                    for i in range(count):
                        length = shell32.DragQueryFileW(hDrop, i, None, 0)
                        buf = ctypes.create_unicode_buffer(length + 1)
                        shell32.DragQueryFileW(hDrop, i, buf, length + 1)
                        path = buf.value
                        if is_audio_file(path):
                            return path
            finally:
                winUser.CloseClipboard()
    except Exception:
        pass
    return None


def get_selected_file_in_explorer():
    """
    Finds the active selected/focused audio file in Windows Explorer or Desktop.
    Uses all available strategies in priority order.
    """
    # 1. Try win32com first
    res = _get_via_win32com()
    if res:
        return res
        
    # 2. Try comtypes
    res = _get_via_comtypes()
    if res:
        return res
        
    # 3. Try NVDA focus object & folder match
    res = _get_via_nvda_focus()
    if res:
        return res
        
    # 4. Try clipboard HDROP
    res = _get_via_clipboard_hdrop()
    if res:
        return res

    # 5. Try clipboard plain text
    try:
        import api
        clip_data = api.getClipData()
        if clip_data and is_audio_file(clip_data.strip()):
            return clip_data.strip()
    except Exception:
        pass

    return None
