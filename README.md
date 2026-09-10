# MVSEP Minus Yaratuvchi / MVSEP Minus Maker (NVDA Add-on)

[![NVDA Compatibility](https://img.shields.io/badge/NVDA-2019.3%20--%202026.2-blue.svg)](https://www.nvaccess.org/)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-green.svg)](https://www.gnu.org/licenses/gpl-2.0)
[![Python: 3.7 - 3.13+](https://img.shields.io/badge/Python-3.7%20--%203.13+-brightgreen.svg)](https://www.python.org/)
[![API: MVSEP.com](https://img.shields.io/badge/API-MVSEP.com%20Live-orange.svg)](https://mvsep.com/full_api)

[O'zbekcha](#ozbekcha) | [Русский](#русский) | [English](#english)

---

## O'zbekcha

Audio fayllardan vokalni tozalash va professional sifatli **minus / instrumental** yaratish uchun mo'ljallangan maxsus NVDA plagini. Ushbu plagin rasmiy [MVSEP.com](https://mvsep.com/full_api) bulutli sun'iy intellekt API tizimi bilan to'liq integratsiya qilingan.

### 📖 Foydalanish Qo'llanmasi
1. **API Kalit olish**:
   - `NVDA menyusi -> Parametrlar -> Sozlamalar -> MVSEP Minus` bo'limiga kiring;
   - "Tizimga kirish..." oynasidagi **"Google / Sayt orqali olish (Brauzerda ochish)"** tugmasini bosing;
   - Saytda **"Sign in with Google"** ni bosib kiring va tayyor API Tokenni plaginga qo'ying.
   > ⚠️ *Eslatma: Oddiy email bilan ro'yxatdan o'tganda MVSEP xati kechikishi yoki kelmasligi mumkin (`Pending email verification`). Shuning uchun Google orqali kirish tavsiya etiladi.*
2. **Musiqani minus qilish**:
   - `NVDA menyusi -> Vositalar (Servis) -> MVSEP: Musiqani minus qilish...` ni oching;
   - Faylni tanlang yoki URL havolani kiriting;
   - Modelni tanlang (`BS Roformer` tavsiya etiladi);
   - "Minus qilishni boshlash" tugmasini bosing. Natija `Downloads/MVSEP_Minus` jildiga tushadi.
3. **Fon rejimida tezkor minus qilish**:
   - Audio faylni belgilab, tezkor tugmani bosing.
   > ⚠️ *Eslatma: Tezkor minus qilish jarayonida `Escape` (Esc) tugmasi bosilmasin, aks holda jarayon bekor bo'ladi.*

### 🌟 Imkoniyatlar
- **Ko'p Akkauntlar Boshqaruvi (Multi-Account)** va avtomatik zaxira akkauntga o'tish (Failover);
- **Saytdagi Tarix**: Oldingi treklarni ko'rish va bip progress signallari bilan yuklab olish;
- **Jonli Navbat**: Server yuklamasini tekshirish;
- **URL orqali Ajratish**: Google Drive, Dropbox, MEGA va Direct audio;
- **Xatoliklar Jurnali**: `mvsep_errors.txt` va dasturchiga xabar berish;
- **35+ Model va 119 Algoritm**: `BS Roformer`, `MelBand`, `SCNet`, `Demucs v4 HT`, `Karaoke`, `Reverb Removal`, `AudioSR` va h.k.

---

## Русский

Специализированное дополнение для программы экранного доступа NVDA, предназначенное для качественного удаления вокала из аудиофайлов и создания **минусовок / инструменталов** профессионального уровня. Дополнение полностью интегрировано с официальным облачным API [MVSEP.com](https://mvsep.com/full_api).

### 📖 Руководство пользователя
1. **Получение API-ключа**:
   - Откройте `Меню NVDA -> Параметры -> Настройки -> MVSEP Minus`;
   - В диалоге входа нажмите кнопку **«Получить через Google / Сайт (Открыть в браузере)»**;
   - Нажмите **«Sign in with Google»** и скопируйте полученный API Token в настройки дополнения.
   > ⚠️ *Примечание: При обычной регистрации по email письмо подтверждения может задерживаться почтовыми сервисами (`Pending email verification`). Рекомендуется вход через Google.*
2. **Создание минусовки**:
   - Откройте `Меню NVDA -> Сервис -> MVSEP: Разделение музыки (Создание минуса)...`;
   - Выберите файл или укажите ссылку;
   - Выберите модель (`BS Roformer` рекомендуется);
   - Нажмите «Начать разделение». Результат сохранится в `Загрузки/MVSEP_Minus`.
3. **Быстрое разделение**:
   - Выделите файл в Проводнике и нажмите назначенную клавишу.
   > ⚠️ *Примечание: Не нажимайте клавишу `Escape` (Esc) во время быстрого разделения, чтобы не отменить процесс.*

### 🌟 Возможности
- **Multi-Account** и автоматическое переключение на резервный аккаунт (Failover);
- **История на сайте**: Просмотр и скачивание треков со звуковыми сигналами прогресса;
- **Очередь сервера**: Проверка загрузки серверов;
- **Разделение по URL**: Google Drive, Dropbox, MEGA и прямые аудио-ссылки;
- **Журнал ошибок**: Запись в `mvsep_errors.txt` и отправка разработчику;
- **Более 35 моделей и 119 алгоритмов**.

---

## English

A specialized screen reader add-on for NVDA designed to cleanly isolate or remove vocals from audio files and generate studio-grade **minus / instrumental** backing tracks. Fully integrated with the official [MVSEP.com](https://mvsep.com/full_api) cloud AI separation API.

### 📖 User Guide
1. **Obtaining API Key**:
   - Open `NVDA Menu -> Preferences -> Settings -> MVSEP Minus`;
   - In login dialog, click **"Get via Google / Website (Open in Browser)"**;
   - Click **"Sign in with Google"** and paste the API Token into add-on settings.
   > ⚠️ *Note: Standard email registration may suffer from mail delivery delays (`Pending email verification`). Sign in with Google is recommended.*
2. **Separating Music**:
   - Open `NVDA Menu -> Tools -> MVSEP: Music Separation (Create Minus)...`;
   - Select file or paste URL;
   - Choose AI model (`BS Roformer` recommended);
   - Click "Start Separation". Saved to `Downloads/MVSEP_Minus`.
3. **Quick Separation**:
   - Select file in Explorer and press hotkey.
   > ⚠️ *Note: Do not press `Escape` (Esc) during quick separation to avoid accidental cancellation.*

---

## 📄 Contacts & License
- **Author**: Komil Hamzayev (<hamzayevkomil52@gmail.com>)
- **Telegram**: [@it_help_uz](https://t.me/it_help_uz)
- **GitHub**: [github.com/komilblindev/mvsep_minus](https://github.com/komilblindev/mvsep_minus)
- **License**: GNU GPL v2.0
