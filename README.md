# MVSEP Minus Creator (NVDA Add-on)

NVDA screen reader add-on for high-quality vocal removal, instrumental separation, and minus track creation using the official [MVSEP.com](https://mvsep.com/full_api) API.

---

## 🌟 Key Features

- **35+ AI Separation Models**: Direct access to state-of-the-art separation models including:
  - `BS Roformer (Vocal / Instrumental)` ⭐
  - `MelBand Roformer`
  - `SCNet Large`
  - `Demucs v4`
  - `MDX23C`
  - `Karaoke (Backing vocals)`
  - `Reverb Removal`
- **Zero FFmpeg Dependency**: 100% pure Python standard library HTTP client. All heavy audio processing occurs on MVSEP's cloud GPU servers.
- **Multilingual UI (3 Languages)**: Full native support for **O'zbekcha (Uzbek)**, **Русский (Russian)**, and **English**, automatically matching your NVDA display language.
- **Credit & Balance Monitoring**: Real-time announcement and display of deducted credits and remaining balance (works seamlessly on free and paid tiers).
- **Audio Feedback**: Dynamic rising tone pitch beeps (220 Hz to 1760 Hz) reflecting upload and download progress.
- **Customizable Gestures**: Fully configurable via NVDA Menu -> Preferences -> Input Gestures.

---

## ⌨️ Default Shortcuts

| Shortcut | Action |
| :--- | :--- |
| **`NVDA + Alt + M`** | Open Minus Creation Dialog |
| **`NVDA + Alt + K`** | Announce remaining credits / balance on MVSEP account |
| **`NVDA + Alt + Shift + M`** | Open MVSEP Minus Settings panel |

---

## 📥 Installation

1. Download the latest **`mvsep_minus-1.0.0.nvda-addon`** from the [Releases](https://github.com/komilblindev/mvsep_minus/releases) page.
2. Open or press `Enter` on the downloaded file.
3. Confirm installation in NVDA and restart NVDA when prompted.
4. Obtain a free API key from [MVSEP API](https://mvsep.com/full_api) and paste it into **NVDA Menu -> Preferences -> Settings -> MVSEP Minus**.

---

## 👨‍💻 Developer & Support

- **Developer**: Komil Hamzayev ([hamzayevkomil52@gmail.com](mailto:hamzayevkomil52@gmail.com))
- **Telegram Channel**: [@it_help_uz](https://t.me/it_help_uz)
- **Official API**: [https://mvsep.com/full_api](https://mvsep.com/full_api)
