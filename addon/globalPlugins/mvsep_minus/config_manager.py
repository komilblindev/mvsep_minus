# -*- coding: utf-8 -*-
"""
Configuration Manager for MVSEP Minus NVDA Add-on.
Stores settings in NVDA's user configuration directory:
<NVDA_CONFIG_DIR>/mvsep_minus.json
Compatible with Python 3.7+ (NVDA 2019.3 - 2026.1).
"""

import os
import json
import time

try:
	import globalVars
	CONFIG_DIR = globalVars.appArgs.configPath
except Exception:
	CONFIG_DIR = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "nvda")

CONFIG_FILE = os.path.join(CONFIG_DIR, "mvsep_minus.json")

DEFAULT_CONFIG = {
	"api_token": "",
	"default_model": "39",          # BS Roformer (vocals, instrumental)
	"output_dir": "",               # Empty means save next to original file
	"announce_progress": True,      # Announce 25%, 50%, 75%, 100%
	"play_progress_beeps": True,    # Rising NVDA tone beeps
	"play_sound_on_finish": True,
	"last_known_credits": "active_free",  # Language-neutral key
	"last_spent_credits": 0,
	"total_separations_count": 0,
	"favorite_models": ["39", "47", "45", "48", "27", "23"],
	"history_retention_days": 30,   # 7, 30, 90, or 0 (unlimited)
	"separation_history": [],
	"translate_models": False,      # Translate model names into active language
	"accounts": [],                 # List of user accounts
	"auto_switch_account": True,    # Automatically failover to next account if quota exceeded
	"language": "auto"              # "auto", "uz", "ru", "en"
}


def get_history_file_path():
	"""Returns the path to Downloads/MVSEP_Minus/mvsep_history.txt"""
	user_profile = os.environ.get('USERPROFILE', os.path.expanduser('~'))
	downloads_dir = os.path.join(user_profile, 'Downloads')
	mvsep_dir = os.path.join(downloads_dir, 'MVSEP_Minus')
	return os.path.join(mvsep_dir, 'mvsep_history.txt')


def get_errors_file_path():
	"""Returns the path to Downloads/MVSEP_Minus/mvsep_errors.txt"""
	user_profile = os.environ.get('USERPROFILE', os.path.expanduser('~'))
	downloads_dir = os.path.join(user_profile, 'Downloads')
	mvsep_dir = os.path.join(downloads_dir, 'MVSEP_Minus')
	return os.path.join(mvsep_dir, 'mvsep_errors.txt')


def log_api_error(stage, error_type, error_message, file_path="", model_id="", account_email="", action_taken=""):
	"""
	Logs an error entry to Downloads/MVSEP_Minus/mvsep_errors.txt
	"""
	try:
		err_path = get_errors_file_path()
		os.makedirs(os.path.dirname(err_path), exist_ok=True)
		
		now_str = time.strftime('%Y-%m-%d %H:%M:%S')
		file_exists = os.path.isfile(err_path)
		
		lines = []
		if not file_exists or os.path.getsize(err_path) == 0:
			lines.extend([
				"===================================================================",
				"   MVSEP MINUS - XATOLIKLAR JURNALI / ЖУРНАЛ ОШИБОК / ERROR LOG    ",
				"===================================================================",
				"Dasturchi / Связь с разработчиком / Developer: hamzayevkomil52@gmail.com",
				f"Yaratilgan / Создан / Created: {now_str}",
				"===================================================================",
				""
			])
			
		fname = os.path.basename(file_path) if file_path else "-"
		acc = account_email or "-"
		
		lines.append(f"[{now_str}]")
		lines.append(f"Fayl / Файл / File: {fname}")
		if model_id:
			lines.append(f"Model: {model_id}")
		lines.append(f"Bosqich / Этап / Stage: {stage}")
		lines.append(f"Hisob / Аккаунт / Account: {acc}")
		lines.append(f"Xatolik / Ошибка / Error: {error_type} - {error_message}")
		if action_taken:
			lines.append(f"Chora / Действие / Action: {action_taken}")
		lines.append("-------------------------------------------------------------------")
		
		with open(err_path, "a", encoding="utf-8") as f:
			f.write("\n".join(lines) + "\n")
		return err_path
	except Exception:
		return None


def format_duration_simple(seconds):
	"""Simple duration formatter."""
	s = int(seconds)
	m, s = divmod(s, 60)
	if m > 0:
		return f"{m}m {s}s"
	return f"{s}s"


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

	def prune_history(self):
		"""Prunes separation history older than history_retention_days."""
		days = int(self.data.get("history_retention_days", 30))
		if days <= 0:
			return
		cutoff = time.time() - (days * 86400)
		hist = self.data.get("separation_history", [])
		pruned = [x for x in hist if x.get("timestamp", 0) >= cutoff]
		self.data["separation_history"] = pruned

	def add_history_entry(self, entry):
		"""
		Records a separation record, prunes old entries, and syncs history file.
		"""
		hist = self.data.get("separation_history", [])
		hist.append(entry)
		self.data["separation_history"] = hist
		
		count = self.data.get("total_separations_count", 0) + 1
		self.data["total_separations_count"] = count
		spent = entry.get("credits_spent", 0)
		if spent > 0:
			self.data["last_spent_credits"] = spent
		rem = entry.get("credits_remaining")
		if rem is not None:
			self.data["last_known_credits"] = str(rem)
			
		self.prune_history()
		self.save()
		self.sync_history_file()

	def get_history_stats(self, days=None):
		"""
		Calculates summary statistics for the requested period in days.
		If days is None, uses configured history_retention_days.
		"""
		if days is None:
			days = int(self.data.get("history_retention_days", 30))
		else:
			days = int(days)
			
		cutoff = (time.time() - (days * 86400)) if days > 0 else 0
		hist = self.data.get("separation_history", [])
		items = [x for x in hist if x.get("timestamp", 0) >= cutoff]
		
		total_seconds = sum(int(x.get("duration_seconds", 0)) for x in items)
		total_count = len(items)
		total_spent = sum(int(x.get("credits_spent", 0)) for x in items)
		balance = self.data.get("last_known_credits", "active_free")
		
		return {
			"days": days,
			"total_seconds": total_seconds,
			"total_count": total_count,
			"total_spent": total_spent,
			"balance": balance,
			"items": items
		}

	def sync_history_file(self):
		"""
		Writes the current separation history to Downloads/MVSEP_Minus/mvsep_history.txt.
		Pruned according to history_retention_days.
		"""
		try:
			history_path = get_history_file_path()
			os.makedirs(os.path.dirname(history_path), exist_ok=True)
			
			stats = self.get_history_stats()
			days = stats["days"]
			retention_title = f"So'nggi {days} kun / Последние {days} дней / Last {days} days" if days > 0 else "Cheksiz / Все время / All time"
			
			lines = [
				"===================================================================",
				"   MVSEP MINUS - AJRATISHLAR TARIXI / ИСТОРИЯ РАЗДЕЛЕНИЙ / HISTORY  ",
				"===================================================================",
				f"Davr / Период / Period: {retention_title}",
				f"Yangilangan / Обновлено / Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
				f"Jami treklar / Всего треков / Total tracks: {stats['total_count']}",
				f"Umumiy ketgan vaqt / Общее время / Total time: {format_duration_simple(stats['total_seconds'])}",
				f"Sarflangan kreditlar / Потрачено кредитов / Credits spent: {stats['total_spent']}",
				f"Hisob balansi / Баланс / Current balance: {stats['balance']}",
				"===================================================================",
				"",
				"[Treklar ro'yxati / Список треков / Tracks List]:",
				""
			]
			
			items = stats["items"]
			if not items:
				lines.append("Hozircha saqlangan ajratishlar yo'q / Пока нет записей / No entries yet.")
			else:
				for i, item in enumerate(reversed(items), 1):
					date_str = item.get("date_str", "-")
					fname = item.get("filename", "-")
					mname = item.get("model_name", "-")
					dur = format_duration_simple(item.get("duration_seconds", 0))
					spent = item.get("credits_spent", 0)
					spent_str = f"{spent} (Kredit)" if spent > 0 else "0 (Bepul / Бесплатно / Free)"
					rem = item.get("credits_remaining", "-")
					
					lines.append(f"[{i}] {date_str} | {fname}")
					lines.append(f"    Model: {mname}")
					lines.append(f"    Vaqt / Время / Duration: {dur} ({item.get('duration_seconds', 0)} soniya)")
					lines.append(f"    Kredit / Кредит / Credits: {spent_str} | Qoldiq / Остаток: {rem}")
					lines.append("-------------------------------------------------------------------")
					
			lines.append("")
			lines.append("Rasmiy sayt / Official site: https://mvsep.com")
			lines.append("===================================================================")
			
			with open(history_path, "w", encoding="utf-8") as f:
				f.write("\n".join(lines) + "\n")
		except Exception:
			pass

	def increment_separation_count(self, spent=0, remaining=None):
		count = self.data.get("total_separations_count", 0) + 1
		self.data["total_separations_count"] = count
		if spent > 0:
			self.data["last_spent_credits"] = spent
		if remaining is not None:
			self.data["last_known_credits"] = str(remaining)
		self.save()

	def get_accounts(self):
		accs = self.data.get("accounts", [])
		cur_tok = self.data.get("api_token", "").strip()
		if not accs and cur_tok:
			accs = [{
				"id": "default",
				"name": "Asosiy hisob",
				"email": "user",
				"api_token": cur_tok,
				"credits": self.data.get("last_known_credits", "active_free"),
				"is_active": True
			}]
			self.data["accounts"] = accs
			self.save()
		return accs

	def get_active_account(self):
		accs = self.get_accounts()
		for acc in accs:
			if acc.get("is_active"):
				return acc
		if accs:
			return accs[0]
		return None

	def set_active_account(self, account_id):
		accs = self.get_accounts()
		target_token = ""
		for acc in accs:
			if acc.get("id") == account_id or acc.get("api_token") == account_id:
				acc["is_active"] = True
				target_token = acc.get("api_token", "")
			else:
				acc["is_active"] = False
		if target_token:
			self.data["api_token"] = target_token
		self.data["accounts"] = accs
		self.save()
		self.sync_accounts_file()

	def add_or_update_account(self, email, api_token, name="", credits="active_free"):
		token_clean = api_token.strip()
		if not token_clean:
			return
		email_clean = email.strip() or "user"
		accs = self.get_accounts()
		found = False
		for acc in accs:
			if acc.get("api_token") == token_clean or (email_clean != "user" and acc.get("email") == email_clean):
				acc["email"] = email_clean
				acc["api_token"] = token_clean
				if name:
					acc["name"] = name
				if credits:
					acc["credits"] = str(credits)
				acc["is_active"] = True
				found = True
			else:
				acc["is_active"] = False
				
		if not found:
			import uuid
			new_acc = {
				"id": str(uuid.uuid4())[:8],
				"name": name or email_clean,
				"email": email_clean,
				"api_token": token_clean,
				"credits": str(credits),
				"is_active": True
			}
			accs.append(new_acc)
			ret_acc = new_acc
		else:
			ret_acc = next((a for a in accs if a.get("api_token") == token_clean), None)
			
		self.data["accounts"] = accs
		self.data["api_token"] = token_clean
		self.save()
		self.sync_accounts_file()
		return ret_acc

	def get_next_account(self, current_token=None):
		accs = self.get_accounts()
		if not accs or len(accs) <= 1:
			return None
		cur = current_token or self.data.get("api_token", "")
		for acc in accs:
			if acc.get("api_token") != cur:
				return acc
		return None

	def remove_account(self, account_id):
		accs = self.get_accounts()
		accs = [a for a in accs if a.get("id") != account_id and a.get("api_token") != account_id]
		if accs and not any(a.get("is_active") for a in accs):
			accs[0]["is_active"] = True
			self.data["api_token"] = accs[0].get("api_token", "")
		self.data["accounts"] = accs
		self.save()
		self.sync_accounts_file()

	def log_api_error(self, stage, error_type, error_message, file_path="", model_id="", account_email="", action_taken=""):
		return log_api_error(stage, error_type, error_message, file_path=file_path, model_id=model_id, account_email=account_email, action_taken=action_taken)

	def sync_accounts_file(self):
		try:
			user_profile = os.environ.get('USERPROFILE', os.path.expanduser('~'))
			path = os.path.join(user_profile, 'Downloads', 'MVSEP_Minus', 'mvsep_account.txt')
			os.makedirs(os.path.dirname(path), exist_ok=True)
			accs = self.get_accounts()
			now_str = time.strftime('%Y-%m-%d %H:%M:%S')
			lines = [
				"===================================================================",
				"       MVSEP MINUS - HISOB VA API MA'LUMOTLARI / ACCOUNTS LIST    ",
				"===================================================================",
				f"Yangilangan / Обновлено / Updated: {now_str}",
				f"Jami hisoblar soni / Всего аккаунтов / Total accounts: {len(accs)}",
				"===================================================================",
				""
			]
			if not accs:
				lines.append("Hozircha saqlangan hisoblar yo'q / Пока нет сохраненных аккаунтов.")
			else:
				for i, acc in enumerate(accs, 1):
					status = "FAOL / АКТИВЕН / ACTIVE" if acc.get("is_active") else "Zaxira / Запасной / Standby"
					lines.append(f"[{i}] Hisob / Аккаунт: {acc.get('name', '')} ({acc.get('email', '-')})")
					lines.append(f"    Holat / Статус: {status}")
					lines.append(f"    API Token: {acc.get('api_token', '-')}")
					lines.append(f"    Balans / Баланс: {acc.get('credits', '-')}")
					lines.append("-------------------------------------------------------------------")
			lines.extend([
				"",
				"Rasmiy sayt / Website: https://mvsep.com",
				"API sahifasi / API page: https://mvsep.com/full_api",
				"Dasturchi / Developer: hamzayevkomil52@gmail.com",
				"==================================================================="
			])
			with open(path, "w", encoding="utf-8") as f:
				f.write("\n".join(lines) + "\n")
		except Exception:
			pass



config = ConfigManager()
