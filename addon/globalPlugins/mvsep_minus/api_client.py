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


def create_separation(api_token, file_path, sep_type="40", output_format="0", progress_callback=None, cancel_event=None):
    """
    Uploads audiofile directly to MVSEP separation API using multipart/form-data.
    Reports upload progress via progress_callback(percentage).
    Returns {"hash": hash_string} or raises Exception.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    
    fields = [
        ("api_token", api_token.strip()),
        ("sep_type", str(sep_type)),
        ("output_format", str(output_format)),
        ("is_algo", "0")
    ]
    
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
            
            err = result.get("error") or result.get("message") or str(result)
            if "credit" in str(err).lower() or "quota" in str(err).lower():
                raise PermissionError("MVSEP_QUOTA_EXCEEDED")
            raise ValueError(f"Server error: {err}")
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
