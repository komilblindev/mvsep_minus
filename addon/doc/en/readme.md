# MVSEP Minus Maker - NVDA Add-on

A specialized screen reader add-on for NVDA designed to cleanly isolate or remove vocals from audio files and generate studio-grade **minus / instrumental** backing tracks. Fully integrated with the official [MVSEP.com](https://mvsep.com/full_api) cloud AI separation API.

---

## 📖 User Guide (Step-by-Step)

### Step 1: Connect Account & Obtain API Key
A free personal MVSEP API key is required to use this add-on.

> ⚠️ **IMPORTANT: Known Email Verification Delivery Issues!**  
> Due to third-party spam filtering policies on MVSEP's mail delivery servers, confirmation emails often get delayed or fail to arrive when registering via basic email (`Pending email verification` status).  
> **The Recommended, 100% Reliable Method (Takes 1 minute):**
> 1. Open `NVDA Menu -> Preferences -> Settings -> MVSEP Minus`;
> 2. Click "Log in..." or "Register...";
> 3. Click the **"Get via Google / Website (Open in Browser)"** button;
> 4. On the MVSEP webpage, click **"Sign in with Google"**;
> 5. On the API page (`https://mvsep.com/full_api`), your **API Token** will be ready immediately. Copy it (`Ctrl + C`);
> 6. Paste it into the **"MVSEP API Key"** field in add-on settings and click **"Check API Key"**.

---

### Step 2: Separate Audio (Main Separation Dialog)
1. Navigate to: `NVDA Menu -> Tools -> MVSEP: Music Separation (Create Minus)...` (or press your configured hotkey);
2. In the dialog:
   - **Local File**: Click "Browse..." to select an audio file (MP3, WAV, FLAC, M4A, OGG);
   - **Remote URL**: Or paste a link (Google Drive, Dropbox, MEGA, or direct audio link);
3. **Select AI Model**: `BS Roformer (vocals, instrumental)` ⭐ is selected by default for maximum vocal separation clarity;
4. **Output Stems**: Instrumental only, Vocal only, or Both stems;
5. **Format**: MP3 (320 kbps), WAV (lossless), or FLAC;
6. Click **"Start Separation"** (`Alt+S` or `S`).
7. Rising tone beeps indicate upload and download progress. The processed audio is saved automatically to **`Downloads/MVSEP_Minus`**.

---

### Step 3: Quick Background Separation (Quick Mode)
1. Select any audio file in Windows File Explorer;
2. Press your assigned quick separation hotkey;
3. The add-on processes the file in the background using your last saved preferences without opening any dialogs.

---

### Step 4: Cloud Separation History & Re-downloading
1. Open add-on settings in NVDA;
2. Click **"Separation history on site..."**;
3. Browse previously separated tracks and click **"Download"** to download them directly to your PC.

---

## 🌟 Key Features

- **Multi-Account Management**: Store multiple accounts with visible quota balances and switch seamlessly.
- **Automated Failover**: Automatically switches to the next configured backup account when limits expire.
- **Live Server Queue Inspection**: Real-time server workload and queue status.
- **Remote Audio URL Separation**: Google Drive, Dropbox, MEGA, and direct URLs.
- **Error Logging**: Traceback recorded in `mvsep_errors.txt` with one-click developer reporting.
- **No FFmpeg Required**: Pure cloud GPU processing.
- **Full Tri-Lingual Support**: Uzbek, Russian, and English.

---

## 🎧 AI Separation Models & Categories

Features over 35 curated models and support for all **119 official MVSEP algorithms**:
- **Minus & Vocals**: `BS Roformer` ⭐, `MelBand Roformer`, `SCNet Large`, `MDX23C`, `Demucs v4 HT`, `Karaoke (Backing vocals)`, `Medley Vox`, `Choir & SATB`;
- **Premium Ensembles**: `Ensemble 2x/4x/6x`, `BS Roformer SW (6 stems)`, `Mega 53-stem`;
- **Audio Enhancement & Restoration**: `Reverb Removal`, `DeNoise`, `Apollo Enhancers`, `AudioSR / FlashSR`, `Crowd Removal`, `BandIt Plus & DnR v3`;
- **Instruments**: Drums, Piano, Bass, Guitar, Strings, Brass, Woodwinds, Percussion.

---

## ⌨️ Input Gestures

No default global gestures are assigned to prevent collisions. Configure them under:  
`NVDA Menu -> Preferences -> Input Gestures -> MVSEP Minus Maker`.

---

## ⚙️ Requirements & Compatibility

- **NVDA Compatibility**: NVDA 2019.3 through 2026.2;
- **Python**: Python 3.7 — Python 3.13+;
- **Dependencies**: None.

---

## 📄 License & Author Info

- **License**: GNU General Public License v2.0 (GPL-2.0);
- **Developer**: Komil Hamzayev (<a href="mailto:hamzayevkomil52@gmail.com">hamzayevkomil52@gmail.com</a>);
- **Telegram**: <a href="https://t.me/it_help_uz">@it_help_uz</a>;
- **GitHub**: <a href="https://github.com/komilblindev/mvsep_minus">github.com/komilblindev/mvsep_minus</a>.
