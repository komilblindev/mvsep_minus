# -*- coding: utf-8 -*-
"""
Configuration Manager for MVSEP Minus NVDA Add-on.
Stores settings in NVDA's user configuration directory:
<NVDA_CONFIG_DIR>/mvsep_minus.json
Compatible with Python 3.7+ (NVDA 2019.3 - 2026.1).
"""

import os
import json

try:
    import globalVars
    CONFIG_DIR = globalVars.appArgs.configPath
except Exception:
    CONFIG_DIR = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "nvda")

CONFIG_FILE = os.path.join(CONFIG_DIR, "mvsep_minus.json")

DEFAULT_CONFIG = {
    "api_token": "",
    "default_model": "40",          # BS Roformer
    "output_dir": "",               # Empty means save next to original file
    "announce_progress": True,      # Announce 25%, 50%, 75%, 100%
    "play_progress_beeps": True,    # Rising NVDA tone beeps
    "play_sound_on_finish": True,
    "last_known_credits": "active_free",  # Language-neutral key
    "last_spent_credits": 0,
    "total_separations_count": 0,
    "favorite_models": ["40", "48", "49", "25", "22"],
    "language": "auto"              # "auto", "uz", "ru", "en"
}


class ConfigManager:
    def __init__(self):
        self.config_path = CONFIG_FILE
        self.data = dict(DEFAULT_CONFIG)
        self.load()

    def load(self):
        """Loads configuration from JSON file."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self.data.update(loaded)
            except Exception:
                pass
        else:
            self.save()

    def save(self):
        """Saves current configuration to JSON file."""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def add_favorite(self, model_id):
        favs = self.data.get("favorite_models", [])
        mid = str(model_id)
        if mid not in favs:
            favs.append(mid)
            self.set("favorite_models", favs)

    def remove_favorite(self, model_id):
        favs = self.data.get("favorite_models", [])
        mid = str(model_id)
        if mid in favs:
            favs.remove(mid)
            self.set("favorite_models", favs)

    def toggle_favorite(self, model_id):
        mid = str(model_id)
        if self.is_favorite(mid):
            self.remove_favorite(mid)
            return False
        else:
            self.add_favorite(mid)
            return True

    def is_favorite(self, model_id):
        return str(model_id) in self.data.get("favorite_models", [])

    def increment_separation_count(self, spent=0, remaining=None):
        count = self.data.get("total_separations_count", 0) + 1
        self.data["total_separations_count"] = count
        if spent > 0:
            self.data["last_spent_credits"] = spent
        if remaining is not None:
            self.data["last_known_credits"] = str(remaining)
        self.save()


config = ConfigManager()
