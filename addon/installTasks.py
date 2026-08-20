# -*- coding: UTF-8 -*-
import addonHandler
import gui
import wx
import os

addonHandler.initTranslation()

def onInstall():
    for addon in addonHandler.getAvailableAddons():
        if addon.manifest['name'] == "mvsep_minus" and addon.isPendingRemove == False:
            if addon.manifest['version'] != "1.0.0":
                addon.requestRemove()
