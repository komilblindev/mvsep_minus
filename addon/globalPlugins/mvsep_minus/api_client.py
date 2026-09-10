# -*- coding: utf-8 -*-
"""
Official MVSEP Full API Client for NVDA Add-on (https://mvsep.com/full_api).
Requires NO external dependencies and NO FFmpeg.
Endpoints implemented:
- POST https://mvsep.com/api/separation/create (Multipart audio upload)
- GET https://mvsep.com/api/separation/get (Task status polling & results)
- GET https://mvsep.com/api/app/user (Official live user details & premium_minutes credits)
- POST https://mvsep.com/api/separation/cancel (Task cancellation)
Compatible with Python 3.7+ (NVDA 2019.3 - 2026.1+).
"""

import os
import sys
import time
import json
import uuid
import ssl
import re
import urllib.request
import urllib.error
import urllib.parse

MVSEP_CREATE_URL = "https://mvsep.com/api/separation/create"
MVSEP_GET_URL = "https://mvsep.com/api/separation/get"
MVSEP_USER_URL = "https://mvsep.com/api/app/user"
MVSEP_CANCEL_URL = "https://mvsep.com/api/separation/cancel"
MVSEP_LOGIN_URL = "https://mvsep.com/api/app/login"
MVSEP_REGISTER_URL = "https://mvsep.com/api/app/register"
MVSEP_QUEUE_URL = "https://mvsep.com/api/app/queue"
MVSEP_HISTORY_URL = "https://mvsep.com/api/app/separation_history"


def _create_ssl_context():
	"""Create SSL context compatible with various Windows/NVDA Python environments."""
	try:
		return ssl.create_default_context()
	except Exception:
		try:
			return ssl._create_unverified_context()
		except Exception:
			return None


def get_user_account_info(api_token):
	"""
	Calls official https://mvsep.com/api/app/user endpoint.
	Returns (True, user_data_dict) or (False, error_message).
	"""
	if not api_token or not api_token.strip():
		return False, "API token is empty"
	
	token = api_token.strip()
	url = f"{MVSEP_USER_URL}?api_token={urllib.parse.quote(token)}"
	
	try:
		ctx = _create_ssl_context()
		req = urllib.request.Request(url, headers={"User-Agent": "NVDA-MVSEP-Minus/1.0"})
		with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
			body = resp.read().decode('utf-8', errors='ignore')
			data = json.loads(body)
			
			if data.get("success") and isinstance(data.get("data"), dict):
				return True, data["data"]
			elif data.get("error"):
				return False, data["error"]
			elif data.get("message"):
				return False, data["message"]
			return True, data
	except urllib.error.HTTPError as e:
		if e.code in [401, 403]:
			return False, "Unauthorized (Invalid API token)"
		return False, f"HTTP Error {e.code}"
	except Exception as e:
		return False, str(e)


def test_api_token(api_token):
	"""
	Validates the MVSEP API token using official /api/app/user.
	Returns (True, user_dict_or_msg) or (False, error_msg).
	"""
	ok, res = get_user_account_info(api_token)
	if ok:
		name = res.get("name", "")
		email = res.get("email", "")
		mins = res.get("premium_minutes", 0)
		desc = f"{name} ({email}) - {mins} min" if name else "Token valid"
		return True, desc
	return False, res


def create_separation(api_token, file_path=None, audio_url=None, sep_type="40", output_format="0", progress_callback=None, cancel_event=None):
	"""
	Uploads audiofile directly to MVSEP separation API using multipart/form-data,
	OR provides remote audio URL via form-data.
	Reports upload progress via progress_callback(percentage).
	Returns {"hash": hash_string} or raises Exception.
	"""
	if not file_path and not audio_url:
		raise ValueError("Either file_path or audio_url must be provided.")
	
	boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
	fields = [
		("api_token", api_token.strip()),
		("sep_type", str(sep_type)),
		("output_format", str(output_format)),
		("is_algo", "0")
	]
	if audio_url:
		u_clean = audio_url.strip()
		fields.append(("url", u_clean))
		# Auto-detect remote_type
		u_lower = u_clean.lower()
		if "drive.google.com" in u_lower:
			fields.append(("remote_type", "drive"))
		elif "dropbox.com" in u_lower:
			fields.append(("remote_type", "dropbox"))
		elif "mega.nz" in u_lower:
			fields.append(("remote_type", "mega"))
		else:
			fields.append(("remote_type", "direct"))
	
	if audio_url and not file_path:
		# URL based separation without file upload
		body = []
		for k, v in fields:
			body.append(f"--{boundary}\r\n".encode("utf-8"))
			body.append(f'Content-Disposition: form-data; name="{k}"\r\n\r\n'.encode("utf-8"))
			body.append(f"{v}\r\n".encode("utf-8"))
		body.append(f"--{boundary}--\r\n".encode("utf-8"))
		body_bytes = b"".join(body)
		
		req = urllib.request.Request(
			MVSEP_CREATE_URL,
			data=body_bytes,
			headers={
				"Content-Type": f"multipart/form-data; boundary={boundary}",
				"Content-Length": str(len(body_bytes)),
				"User-Agent": "NVDA-MVSEP-Minus/1.0"
			},
			method="POST"
		)
		ctx = _create_ssl_context()
		try:
			with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
				resp_body = resp.read().decode("utf-8", errors="ignore")
				result = json.loads(resp_body)
				hash_val = result.get("hash") or (result.get("data", {}).get("hash") if isinstance(result.get("data"), dict) else None)
				if hash_val:
					return {"hash": hash_val}
				err = result.get("error") or result.get("message") or (result.get("data", {}).get("message") if isinstance(result.get("data"), dict) else str(result.get("data")))
				if any(k in str(err).lower() for k in ["credit", "quota", "limit", "payment"]):
					raise PermissionError(f"MVSEP_QUOTA_EXCEEDED: {err}")
				raise ValueError(f"Server error: {err}")
		except urllib.error.HTTPError as e:
			err_msg = ""
			try:
				err_body = e.read().decode("utf-8", errors="ignore")
				err_json = json.loads(err_body)
				err_msg = err_json.get("error") or err_json.get("message") or (err_json.get("data", {}).get("message") if isinstance(err_json.get("data"), dict) else str(err_json.get("data")))
			except Exception:
				err_msg = f"HTTP Error {e.code}: {e.reason}"
			if any(k in str(err_msg).lower() for k in ["credit", "quota", "limit", "payment"]) or e.code in [402, 429]:
				raise PermissionError(f"MVSEP_QUOTA_EXCEEDED: {err_msg}")
			raise ValueError(f"Server error ({e.code}): {err_msg}")

	if not os.path.isfile(file_path):
		raise FileNotFoundError(f"File not found: {file_path}")
	
	file_size = os.path.getsize(file_path)
	file_name = os.path.basename(file_path)
	
	body_pre = []
	for k, v in fields:
		body_pre.append(f"--{boundary}\r\n".encode("utf-8"))
		body_pre.append(f'Content-Disposition: form-data; name="{k}"\r\n\r\n'.encode("utf-8"))
		body_pre.append(f"{v}\r\n".encode("utf-8"))
		
	body_pre.append(f"--{boundary}\r\n".encode("utf-8"))
	body_pre.append(f'Content-Disposition: form-data; name="audiofile"; filename="{file_name}"\r\n'.encode("utf-8"))
	body_pre.append(b"Content-Type: application/octet-stream\r\n\r\n")
	
	body_pre_bytes = b"".join(body_pre)
	body_post_bytes = f"\r\n--{boundary}--\r\n".encode("utf-8")
	
	total_upload_size = len(body_pre_bytes) + file_size + len(body_post_bytes)
	
	class UploadProgressStream:
		def __init__(self, f_path, pre_bytes, post_bytes, total_size, cb, cancel_ev):
			self.file_obj = open(f_path, "rb")
			self.pre = pre_bytes
			self.post = post_bytes
			self.total = total_size
			self.cb = cb
			self.cancel_ev = cancel_ev
			self.sent = 0
			self.pre_done = False
			self.file_done = False
			self.post_done = False

		def read(self, chunk_size=262144):  # 256KB chunks
			if self.cancel_ev and self.cancel_ev.is_set():
				raise InterruptedError("Cancelled by user")
			
			chunk = b""
			if not self.pre_done:
				chunk += self.pre
				self.pre_done = True
			
			if not self.file_done and len(chunk) < chunk_size:
				need = chunk_size - len(chunk)
				f_chunk = self.file_obj.read(need)
				if not f_chunk:
					self.file_done = True
					self.file_obj.close()
				else:
					chunk += f_chunk
			
			if self.file_done and not self.post_done and len(chunk) < chunk_size:
				chunk += self.post
				self.post_done = True
			
			if chunk:
				self.sent += len(chunk)
				if self.cb and self.total > 0:
					pct = min(int((self.sent / self.total) * 100), 100)
					self.cb(pct)
			
			return chunk

		def __len__(self):
			return self.total

	stream = UploadProgressStream(file_path, body_pre_bytes, body_post_bytes, total_upload_size, progress_callback, cancel_event)
	
	req = urllib.request.Request(
		MVSEP_CREATE_URL,
		data=stream,
		headers={
			"Content-Type": f"multipart/form-data; boundary={boundary}",
			"Content-Length": str(total_upload_size),
			"User-Agent": "NVDA-MVSEP-Minus/1.0"
		},
		method="POST"
	)
	
	ctx = _create_ssl_context()
	try:
		with urllib.request.urlopen(req, context=ctx, timeout=300) as resp:
			resp_body = resp.read().decode("utf-8", errors="ignore")
			result = json.loads(resp_body)
			
			hash_val = result.get("hash") or (result.get("data", {}).get("hash") if isinstance(result.get("data"), dict) else None)
			if hash_val:
				return {"hash": hash_val}
			
			if result.get("success") and isinstance(result.get("data"), dict) and result["data"].get("hash"):
				return {"hash": result["data"]["hash"]}
			
			err = result.get("error") or result.get("message") or (result.get("data", {}).get("message") if isinstance(result.get("data"), dict) else str(result.get("data"))) or str(result)
			if any(k in str(err).lower() for k in ["credit", "quota", "limit", "payment"]):
				raise PermissionError(f"MVSEP_QUOTA_EXCEEDED: {err}")
			raise ValueError(f"Server error: {err}")
	except urllib.error.HTTPError as e:
		err_msg = ""
		try:
			body_text = e.read().decode("utf-8", errors="ignore")
			err_json = json.loads(body_text)
			err_msg = err_json.get("error") or err_json.get("message") or (err_json.get("data", {}).get("message") if isinstance(err_json.get("data"), dict) else str(err_json.get("data")))
		except Exception:
			err_msg = f"HTTP Error {e.code}: {e.reason}"
		if any(k in str(err_msg).lower() for k in ["credit", "quota", "limit", "payment"]) or e.code in [402, 429]:
			raise PermissionError(f"MVSEP_QUOTA_EXCEEDED: {err_msg}")
		raise ValueError(f"Server error ({e.code}): {err_msg}")
	finally:
		try:
			if not stream.file_obj.closed:
				stream.file_obj.close()
		except Exception:
			pass


def poll_separation(api_token, hash_val, progress_callback=None, cancel_event=None, max_retries=120, interval=6):
	"""
	Polls MVSEP status using official https://mvsep.com/api/separation/get.
	Returns (files_list, credits_dict).
	"""
	url = f"{MVSEP_GET_URL}?hash={hash_val}&api_token={api_token.strip()}"
	ctx = _create_ssl_context()
	
	for step in range(max_retries):
		if cancel_event and cancel_event.is_set():
			# Try to cancel on server as well
			try:
				cancel_req = urllib.request.Request(
					MVSEP_CANCEL_URL,
					data=urllib.parse.urlencode({"api_token": api_token.strip(), "hash": hash_val}).encode("utf-8"),
					headers={"User-Agent": "NVDA-MVSEP-Minus/1.0"},
					method="POST"
				)
				urllib.request.urlopen(cancel_req, context=ctx, timeout=5)
			except Exception:
				pass
			raise InterruptedError("Cancelled by user")
		
		percent = min(int(step * 2.5 + 5), 98)
		if progress_callback:
			progress_callback(percent, "processing")
		
		try:
			req = urllib.request.Request(url, headers={"User-Agent": "NVDA-MVSEP-Minus/1.0"})
			with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
				resp_text = resp.read().decode("utf-8", errors="ignore")
				result = json.loads(resp_text)
				
				status = result.get("status")
				files = result.get("files")
				
				if isinstance(result.get("data"), dict):
					data_block = result["data"]
					status = status or data_block.get("status")
					files = files or data_block.get("files") or data_block.get("result_url") or data_block.get("urls") or data_block.get("output")
				
				if not files:
					files = result.get("result_url") or result.get("urls") or result.get("output")
				
				if isinstance(files, dict):
					files = list(files.values())
				elif isinstance(files, str):
					files = [files]
				
				if (result.get("success") and files) or (status in ("done", "success", "completed") and files):
					if progress_callback:
						progress_callback(100, "done")
					return files, {"credits_spent": 0}
				
				if status in ("error", "failed"):
					err_txt = result.get("error", status)
					if "credit" in str(err_txt).lower():
						raise PermissionError("MVSEP_QUOTA_EXCEEDED")
					raise RuntimeError(f"Separation failed on server: {err_txt}")
				
				if status == "not_found":
					raise RuntimeError("Task hash not found on MVSEP server.")
					
		except urllib.error.HTTPError as e:
			if e.code in (401, 403):
				raise PermissionError("MVSEP API Error: Invalid token or quota reached.")
		except InterruptedError:
			raise
		except Exception:
			pass
		
		time.sleep(interval)
		
	raise TimeoutError("Separation timed out on server after max attempts.")


def download_file(file_url, target_path, progress_callback=None, cancel_event=None):
	"""
	Downloads file from URL to local target_path in 128KB chunks.
	"""
	if not file_url.startswith("http"):
		if file_url.startswith("/"):
			file_url = "https://mvsep.com" + file_url
		else:
			file_url = "https://mvsep.com/" + file_url
			
	ctx = _create_ssl_context()
	req = urllib.request.Request(file_url, headers={"User-Agent": "NVDA-MVSEP-Minus/1.0"})
	
	os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)
	
	with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
		total_len = resp.getheader("Content-Length")
		total_bytes = int(total_len) if total_len and total_len.isdigit() else 0
		downloaded = 0
		
		with open(target_path, "wb") as f_out:
			while True:
				if cancel_event and cancel_event.is_set():
					try:
						f_out.close()
						if os.path.exists(target_path):
							os.remove(target_path)
					except Exception:
						pass
					raise InterruptedError("Download cancelled")
				
				chunk = resp.read(131072)  # 128KB
				if not chunk:
					break
				f_out.write(chunk)
				downloaded += len(chunk)
				if progress_callback and total_bytes > 0:
					pct = min(int((downloaded / total_bytes) * 100), 100)
					progress_callback(pct)
					
	return target_path


def clean_output_filename(url_or_name, source_song_path, track_role="minus"):
	"""
	Creates clean, accessible filenames: e.g. "Song Name - Minus.mp3" or "Song Name - Vocals.mp3".
	"""
	base_name = os.path.splitext(os.path.basename(source_song_path))[0]
	base_name = re.sub(r'^[\d_\-\s]+', '', base_name).strip("_- ") or "track"
	
	raw_name = url_or_name.split("/")[-1].split("?")[0].lower()
	ext = os.path.splitext(raw_name)[1] or ".mp3"
	
	if "vocal" in raw_name and "back" not in raw_name and "karaoke" not in raw_name and "instr" not in raw_name:
		return f"{base_name} - Vocals{ext}"
	elif "back" in raw_name:
		return f"{base_name} - Backing Vocals{ext}"
	elif "main" in raw_name and "vocal" in raw_name:
		return f"{base_name} - Lead Vocals{ext}"
	elif "instr" in raw_name or "minus" in raw_name or "music" in raw_name or "accompaniment" in raw_name or "other" in raw_name:
		return f"{base_name} - Minus{ext}"
	elif "drum" in raw_name:
		return f"{base_name} - Drums{ext}"
	elif "bass" in raw_name:
		return f"{base_name} - Bass{ext}"
	elif "guitar" in raw_name:
		return f"{base_name} - Guitar{ext}"
	elif "piano" in raw_name:
		return f"{base_name} - Piano{ext}"
	else:
		cleaned = re.sub(r'mvsep(\.com)?', '', raw_name, flags=re.I)
		cleaned = re.sub(r'^[\d_\-\s]+', '', cleaned).strip("_- ")
		if cleaned:
			return f"{base_name} - {cleaned}"
		return f"{base_name} - {track_role}{ext}"


def login_mvsep(email, password):
	"""
	Logs in to MVSEP via POST https://mvsep.com/api/app/login
	Returns (True, user_dict) or (False, error_message).
	user_dict contains 'api_token', 'name', 'email', 'premium_minutes', etc.
	"""
	if not email or not email.strip():
		return False, "email_empty"
	if not password:
		return False, "password_empty"

	url = MVSEP_LOGIN_URL
	payload = urllib.parse.urlencode({
		"email": email.strip(),
		"password": password
	}).encode('utf-8')

	headers = {
		"User-Agent": "NVDA-MVSEP-Minus/1.0",
		"Content-Type": "application/x-www-form-urlencoded"
	}

	try:
		ctx = _create_ssl_context()
		req = urllib.request.Request(url, data=payload, headers=headers)
		with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
			body = resp.read().decode('utf-8', errors='ignore')
			data = json.loads(body)
			if data.get("success") and isinstance(data.get("data"), dict):
				return True, data["data"]
			msg = data.get("message") or "Unknown error"
			return False, str(msg)
	except urllib.error.HTTPError as e:
		try:
			err_body = e.read().decode('utf-8', errors='ignore')
			err_data = json.loads(err_body)
			msg = err_data.get("message")
			if isinstance(msg, dict):
				lines = []
				for field_errs in msg.values():
					if isinstance(field_errs, list):
						lines.extend([str(x) for x in field_errs])
					else:
						lines.append(str(field_errs))
				return False, "; ".join(lines)
			elif msg:
				return False, str(msg)
		except Exception:
			pass
		return False, f"HTTP Error {e.code}"
	except Exception as e:
		return False, str(e)


def register_mvsep(name, email, password, password_confirmation):
	"""
	Registers a new MVSEP account via POST https://mvsep.com/api/app/register
	Returns (True, success_message) or (False, error_message).
	"""
	if not name or not name.strip():
		return False, "name_empty"
	if not email or not email.strip():
		return False, "email_empty"
	if not password or len(password) < 6:
		return False, "password_too_short"
	if password != password_confirmation:
		return False, "password_mismatch"

	url = MVSEP_REGISTER_URL
	payload = urllib.parse.urlencode({
		"name": name.strip(),
		"email": email.strip(),
		"password": password,
		"password_confirmation": password_confirmation
	}).encode('utf-8')

	headers = {
		"User-Agent": "NVDA-MVSEP-Minus/1.0",
		"Content-Type": "application/x-www-form-urlencoded"
	}

	try:
		ctx = _create_ssl_context()
		req = urllib.request.Request(url, data=payload, headers=headers)
		with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
			body = resp.read().decode('utf-8', errors='ignore')
			data = json.loads(body)
			if data.get("success"):
				msg = data.get("message") or "Account created successfully"
				return True, str(msg)
			msg = data.get("message") or "Registration failed"
			return False, str(msg)
	except urllib.error.HTTPError as e:
		try:
			err_body = e.read().decode('utf-8', errors='ignore')
			err_data = json.loads(err_body)
			msg = err_data.get("message")
			if isinstance(msg, dict):
				lines = []
				for field_errs in msg.values():
					if isinstance(field_errs, list):
						lines.extend([str(x) for x in field_errs])
					else:
						lines.append(str(field_errs))
				return False, "; ".join(lines)
			elif msg:
				return False, str(msg)
		except Exception:
			pass
		return False, f"HTTP Error {e.code}"
	except Exception as e:
		return False, str(e)


def get_account_file_path():
	"""Returns the path to Downloads/MVSEP_Minus/mvsep_account.txt"""
	user_profile = os.environ.get('USERPROFILE', os.path.expanduser('~'))
	downloads_dir = os.path.join(user_profile, 'Downloads')
	mvsep_dir = os.path.join(downloads_dir, 'MVSEP_Minus')
	return os.path.join(mvsep_dir, 'mvsep_account.txt')


def get_history_file_path():
	"""Returns the path to Downloads/MVSEP_Minus/mvsep_history.txt"""
	user_profile = os.environ.get('USERPROFILE', os.path.expanduser('~'))
	downloads_dir = os.path.join(user_profile, 'Downloads')
	mvsep_dir = os.path.join(downloads_dir, 'MVSEP_Minus')
	return os.path.join(mvsep_dir, 'mvsep_history.txt')


def save_account_to_downloads(email, password, api_token=None, credits_info=None):
	"""
	Saves user credentials to Downloads/MVSEP_Minus/mvsep_account.txt
	Returns the full path of the saved file, or None if failed.
	"""
	try:
		account_file = get_account_file_path()
		os.makedirs(os.path.dirname(account_file), exist_ok=True)

		now_str = time.strftime('%Y-%m-%d %H:%M:%S')

		content = [
			"===================================================================",
			"       MVSEP MINUS - HISOB VA API MA'LUMOTLARI / ACCOUNT DETAILS   ",
			"===================================================================",
			f"Sana / Date: {now_str}",
			f"Email: {email}",
			f"Parol / Password: {password}",
		]
		if api_token:
			content.append(f"API Token: {api_token}")
		if credits_info is not None:
			content.append(f"Balans / Credits: {credits_info}")
		content.extend([
			"",
			"Rasmiy havolalar / Official Links:",
			"- Rasmiy sayt / Website: https://mvsep.com",
			"- API sahifasi / API Page: https://mvsep.com/full_api",
			"==================================================================="
		])

		with open(account_file, 'w', encoding='utf-8') as f:
			f.write("\n".join(content) + "\n")

		return account_file
	except Exception:
		return None



def send_error_to_developer(parent_window=None):
	"""
	Reads the last error from mvsep_errors.txt, copies it to clipboard,
	and opens default email client addressed to hamzayevkomil52@gmail.com.
	"""
	from .config_manager import get_errors_file_path
	from .i18n import _t
	try:
		import ui
	except ImportError:
		ui = None
	try:
		import wx
	except ImportError:
		wx = None
		
	err_path = get_errors_file_path()
	err_text = ""
	if os.path.isfile(err_path):
		try:
			with open(err_path, "r", encoding="utf-8") as f:
				err_lines = f.readlines()
				err_text = "".join(err_lines[-35:])
		except Exception:
			pass
			
	if not err_text:
		err_text = "MVSEP Minus Error Log: No errors recorded yet."
		
	if wx:
		try:
			if wx.TheClipboard.Open():
				wx.TheClipboard.SetData(wx.TextDataObject(err_text))
				wx.TheClipboard.Close()
		except Exception:
			pass
			
	dev_email = "hamzayevkomil52@gmail.com"
	subject = urllib.parse.quote("MVSEP Minus - Error Report")
	body_sample = urllib.parse.quote(err_text[:1000])
	mailto_url = f"mailto:{dev_email}?subject={subject}&body={body_sample}"
	
	try:
		webbrowser.open(mailto_url)
	except Exception:
		try:
			os.system(f'start "" "{mailto_url}"')
		except Exception:
			pass
			
	msg = _t("msg_error_sent_opened", email=dev_email)
	if ui and hasattr(ui, 'message'):
		ui.message(msg)
	if parent_window and wx:
		wx.MessageBox(msg, _t("addon_name"), wx.OK | wx.ICON_INFORMATION, parent_window)


def get_server_queue():
	"""
	Calls https://mvsep.com/api/app/queue.
	Returns (True, dict) or (False, error_str).
	dict structure: {"in_process": int, "premium": int, "free": int, "total": int}
	"""
	try:
		ctx = _create_ssl_context()
		req = urllib.request.Request(MVSEP_QUEUE_URL, headers={"User-Agent": "NVDA-MVSEP-Minus/1.0"})
		with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
			data = json.loads(resp.read().decode("utf-8", errors="ignore"))
			q = data.get("queue", {})
			proc = q.get("in_process", 0)
			prem = q.get("premium", 0)
			free = q.get("registered", 0) + q.get("unregistered", 0)
			return True, {
				"in_process": proc,
				"premium": prem,
				"free": free,
				"total": proc + prem + free
			}
	except Exception as e:
		return False, str(e)


def get_site_separation_history(api_token):
	"""
	Calls https://mvsep.com/api/app/separation_history?api_token=...
	Returns (True, list_of_items) or (False, error_str).
	"""
	if not api_token or not api_token.strip():
		return False, "API token is empty"
	
	url = f"{MVSEP_HISTORY_URL}?api_token={urllib.parse.quote(api_token.strip())}"
	try:
		ctx = _create_ssl_context()
		req = urllib.request.Request(url, headers={"User-Agent": "NVDA-MVSEP-Minus/1.0"})
		with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
			data = json.loads(resp.read().decode("utf-8", errors="ignore"))
			if data.get("success") and isinstance(data.get("data"), list):
				return True, data["data"]
			elif data.get("message"):
				return False, str(data["message"])
			return True, []
	except urllib.error.HTTPError as e:
		return False, f"HTTP Error {e.code}"
	except Exception as e:
		return False, str(e)

