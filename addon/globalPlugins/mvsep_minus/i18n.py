# -*- coding: utf-8 -*-
"""
MVSEP Minus Creator - Localization (i18n) Module
Supports Uzbek (uz), Russian (ru), and English (en).
Compatible with Python 3.7+ (NVDA 2019.3 - 2026.1+).
"""

MESSAGES = {
    "uz": {
        "addon_name": "MVSEP Minus Yaratuvchi",
        "menu_create_minus": "MVSEP: Musiqani minus qilish...",
        "menu_create_minus_desc": "Audio faylni vokal va instrumentalga ajratib minus yaratish",
        "menu_check_credits": "MVSEP: Qolgan kreditlarni tekshirish...",
        "menu_check_credits_desc": "MVSEP hisobidagi qolgan kreditlar va balansni tekshirish",
        "menu_settings": "MVSEP: Sozlamalar...",
        "menu_settings_desc": "MVSEP API kaliti va minus parametrlarini sozlash",
        "settings_category": "MVSEP Minus",
        
        # Dialog
        "dialog_title": "MVSEP Musiqani Minus Qilish",
        "file_label": "Audio fayl:",
        "browse": "Ko'rib chiqish...",
        "model_category": "Model toifasi:",
        "cat_favorites": "Sevimli modellar",
        "cat_minus": "Minus va Vokal modellar",
        "cat_all": "Barcha modellar",
        "model_label": "Modelni tanlang:",
        "btn_toggle_fav": "Sevimliga qo'shish / O'chirish",
        "fav_added": "Model sevimlilarga qo'shildi.",
        "fav_removed": "Model sevimlilardan olib tashlandi.",
        "download_options": "Yuklab olish:",
        "opt_minus_only": "Faqat minus (Instrumental)",
        "opt_minus_and_vocal": "Minus va Vokal (2 ta fayl)",
        "opt_all_stems": "Barcha ajratilgan treklar",
        "output_format": "Chiqish formati:",
        "btn_start": "Minus qilishni boshlash",
        "btn_cancel": "Bekor qilish",
        "btn_close": "Yopish",
        "credit_status_badge": "Hisob holati: {status}",
        
        # Statuses
        "status_idle": "Tayyor.",
        "status_reading_file": "Audio fayl o'qilmoqda...",
        "status_uploading": "Serverga yuklanmoqda ({percent}%)...",
        "status_processing": "Serverda ishlanmoqda: {percent}%",
        "status_downloading": "Minus yuklab olinmoqda: {filename}...",
        "status_completed": "Tayyor! Minus muvaffaqiyatli saqlandi.",
        "status_cancelled": "Jarayon bekor qilindi.",
        "status_error": "Xatolik yuz berdi: {error}",
        
        # Credit states
        "status_active": "Faol",
        "status_free": "Bepul",
        "status_active_free": "Faol (Bepul)",
        "status_unlimited": "Cheksiz",
        "credits_unit": "{count} daqiqa",
        
        # Notifications & Credits
        "msg_no_api_token": "MVSEP API kaliti kiritilmagan! Iltimos, 'API kalit olish' tugmasi orqali kalitingizni oling va sozlamalarga kiriting.",
        "msg_no_file_selected": "Iltimos, audio faylni tanlang!",
        "msg_file_not_found": "Fayl topilmadi: {file}",
        "msg_starting_separation": "{model} modeli orqali minus qilish boshlandi...",
        "msg_done_saved": "Minus tayyor! Saqlandi: {path}",
        "credit_deducted_notice": "Minus tayyor! Sarflangan kredit: {spent}. Qolgan kredit: {left}.",
        "credit_balance_speech": "MVSEP hisobingizdagi qolgan kreditlar: {left}. Jami bajarilgan minuslar: {total}.",
        "credit_info_dialog_title": "MVSEP Kredit Ma'lumotlari",
        "credit_info_dialog_body": "MVSEP Hisob Ma'lumotlari:\n\n• Qolgan kreditlar: {left}\n• Oxirgi sarflangan kredit: {spent}\n• Jami tayyorlangan minuslar: {total}\n• API Kalit holati: Faol\n\nBatafsil ma'lumot: https://mvsep.com/uz/full_api",
        "credit_checking": "Kreditlar tekshirilmoqda...",
        
        "msg_upload_failed": "Faylni serverga yuklashda xatolik yuz berdi: {error}",
        "msg_poll_timeout": "Server javob berish vaqti tugadi.",
        "msg_invalid_token": "API kalit yaroqsiz yoki ruxsat berilmagan. Sozlamalardan kalitni tekshiring.",
        "msg_quota_exceeded": "Kreditlar tugagan yoki limit oshib ketgan. Iltimos, mvsep.com saytida hisobingizni to'ldiring.",
        
        # Settings Panel
        "api_token_label": "MVSEP API Kaliti (Token):",
        "api_token_help": "API kalitni olish uchun 'API kalit olish' tugmasini bosing yoki https://mvsep.com/uz/full_api sahifasiga kiring.",
        "btn_get_api_token": "API kalit olish (Saytni ochish)",
        "btn_test_token": "API kalitni tekshirish",
        "btn_check_credits": "Kreditlarni tekshirish",
        "show_key_label": "Kalitni ko'rsatish",
        "api_key_dialog_title": "MVSEP API Kaliti",
        "api_key_display_text": "Sizning API kalitingiz:\n{key}",
        "token_testing": "API kalit tekshirilmoqda...",
        "token_valid": "API kalit to'g'ri va faol!",
        "token_invalid": "API kalit xato: {error}",
        "default_model_label": "Standart model:",
        "output_dir_label": "Natijalarni saqlash papkasi (bo'sh qolsa, asl fayl yoniga saqlanadi):",
        "announce_progress_label": "Jarayon foizlarini ovozli aytib turish",
        "play_sound_label": "Jarayon yakunlanganda tovush chiqarish",
        "language_label": "Addon tili:",
        "lang_auto": "Avtomatik (NVDA tili bo'yicha)",
        "lang_uz": "O'zbekcha",
        "lang_ru": "Русский",
        "lang_en": "English",
        
        # Explorer integration
        "explorer_file_detected": "Fayl aniqlandi: {name}. Minus qilish boshlanmoqda...",
        "open_result_folder": "Natija papkasini ochish",
        "open_result_file": "Minusni tinglash"
    },
    "ru": {
        "addon_name": "MVSEP Создатель Минусов",
        "menu_create_minus": "MVSEP: Создать минус...",
        "menu_create_minus_desc": "Разделить аудиофайл на вокал и инструментал (минусовку)",
        "menu_check_credits": "MVSEP: Проверить остаток кредитов...",
        "menu_check_credits_desc": "Проверить баланс и остаток кредитов MVSEP",
        "menu_settings": "MVSEP: Настройки...",
        "menu_settings_desc": "Настройка API ключа MVSEP и параметров минусовок",
        "settings_category": "MVSEP Минус",
        
        # Dialog
        "dialog_title": "MVSEP Создание Минуса",
        "file_label": "Аудиофайл:",
        "browse": "Обзор...",
        "model_category": "Категория моделей:",
        "cat_favorites": "Избранные модели",
        "cat_minus": "Минус и Вокал модели",
        "cat_all": "Все модели",
        "model_label": "Выберите модель:",
        "btn_toggle_fav": "Добавить / Удалить из избранного",
        "fav_added": "Модель добавлена в избранное.",
        "fav_removed": "Модель удалена из избранного.",
        "download_options": "Скачивание:",
        "opt_minus_only": "Только минус (Инструментал)",
        "opt_minus_and_vocal": "Минус и Вокал (2 файла)",
        "opt_all_stems": "Все разделенные дорожки",
        "output_format": "Формат вывода:",
        "btn_start": "Начать создание минуса",
        "btn_cancel": "Отмена",
        "btn_close": "Закрыть",
        "credit_status_badge": "Статус аккаунта: {status}",
        
        # Statuses
        "status_idle": "Готов.",
        "status_reading_file": "Чтение аудиофайла...",
        "status_uploading": "Загрузка на сервер ({percent}%)...",
        "status_processing": "Обработка на сервере: {percent}%",
        "status_downloading": "Скачивание минуса: {filename}...",
        "status_completed": "Готово! Минус успешно сохранен.",
        "status_cancelled": "Процесс отменен.",
        "status_error": "Ошибка: {error}",
        
        # Credit states
        "status_active": "Активен",
        "status_free": "Бесплатно",
        "status_active_free": "Активен (Бесплатно)",
        "status_unlimited": "Неограниченно",
        "credits_unit": "{count} мин",
        
        # Notifications & Credits
        "msg_no_api_token": "API ключ MVSEP не указан! Нажмите 'Получить API ключ' чтобы скопировать ключ и вставить в настройки.",
        "msg_no_file_selected": "Пожалуйста, выберите аудиофайл!",
        "msg_file_not_found": "Файл не найден: {file}",
        "msg_starting_separation": "Запуск создания минуса с моделью {model}...",
        "msg_done_saved": "Минус готов! Сохранен в: {path}",
        "credit_deducted_notice": "Минус готов! Списано кредитов: {spent}. Остаток кредитов: {left}.",
        "credit_balance_speech": "Остаток кредитов на аккаунте MVSEP: {left}. Всего создано минусов: {total}.",
        "credit_info_dialog_title": "Информация о кредитах MVSEP",
        "credit_info_dialog_body": "Информация об аккаунте MVSEP:\n\n• Остаток кредитов: {left}\n• Последнее списание: {spent}\n• Всего создано минусов: {total}\n• Статус API ключа: Активен\n\nПодробнее: https://mvsep.com/ru/full_api",
        "credit_checking": "Проверка кредитов...",
        
        "msg_upload_failed": "Ошибка при загрузке файла на сервер: {error}",
        "msg_poll_timeout": "Время ожидания ответа сервера истекло.",
        "msg_invalid_token": "Неверный API ключ или доступ запрещен. Проверьте ключ в настройках.",
        "msg_quota_exceeded": "Закончились кредиты или превышен лимит. Пожалуйста, пополните баланс на https://mvsep.com",
        
        # Settings Panel
        "api_token_label": "API Ключ MVSEP (Токен):",
        "api_token_help": "Чтобы получить API ключ, нажмите 'Получить API ключ' или перейдите на https://mvsep.com/ru/full_api",
        "btn_get_api_token": "Получить API ключ (Открыть сайт)",
        "btn_test_token": "Проверить API ключ",
        "btn_check_credits": "Проверить кредиты",
        "show_key_label": "Показать ключ",
        "api_key_dialog_title": "API Ключ MVSEP",
        "api_key_display_text": "Ваш API ключ:\n{key}",
        "token_testing": "Проверка ключа...",
        "token_valid": "API ключ верный и активен!",
        "token_invalid": "Ошибка ключа: {error}",
        "default_model_label": "Модель по умолчанию:",
        "output_dir_label": "Папка для сохранения (если пусто, сохранять рядом с оригиналом):",
        "announce_progress_label": "Озвучивать проценты обработки",
        "play_sound_label": "Воспроизводить сигнал по завершении",
        "language_label": "Язык дополнения:",
        "lang_auto": "Автоматически (по языку NVDA)",
        "lang_uz": "O'zbekcha",
        "lang_ru": "Русский",
        "lang_en": "English",
        
        # Explorer integration
        "explorer_file_detected": "Файл обнаружен: {name}. Начинается создание минуса...",
        "open_result_folder": "Открыть папку с результатом",
        "open_result_file": "Прослушать минус"
    },
    "en": {
        "addon_name": "MVSEP Minus Creator",
        "menu_create_minus": "MVSEP: Create Minus / Instrumental...",
        "menu_create_minus_desc": "Separate audio file into vocals and instrumental (minus)",
        "menu_check_credits": "MVSEP: Check Remaining Credits...",
        "menu_check_credits_desc": "Check MVSEP account balance and remaining credits",
        "menu_settings": "MVSEP: Settings...",
        "menu_settings_desc": "Configure MVSEP API key and minus options",
        "settings_category": "MVSEP Minus",
        
        # Dialog
        "dialog_title": "MVSEP Minus Creator",
        "file_label": "Audio file:",
        "browse": "Browse...",
        "model_category": "Model category:",
        "cat_favorites": "Favorite models",
        "cat_minus": "Minus & Vocal models",
        "cat_all": "All models",
        "model_label": "Select model:",
        "btn_toggle_fav": "Add to / Remove from Favorites",
        "fav_added": "Model added to favorites.",
        "fav_removed": "Model removed from favorites.",
        "download_options": "Download option:",
        "opt_minus_only": "Minus only (Instrumental)",
        "opt_minus_and_vocal": "Minus and Vocals (2 files)",
        "opt_all_stems": "All separated stems",
        "output_format": "Output format:",
        "btn_start": "Start Separation",
        "btn_cancel": "Cancel",
        "btn_close": "Close",
        "credit_status_badge": "Account status: {status}",
        
        # Statuses
        "status_idle": "Ready.",
        "status_reading_file": "Reading audio file...",
        "status_uploading": "Uploading to server ({percent}%)...",
        "status_processing": "Processing on server: {percent}%",
        "status_downloading": "Downloading minus: {filename}...",
        "status_completed": "Done! Minus track successfully saved.",
        "status_cancelled": "Process cancelled.",
        "status_error": "Error: {error}",
        
        # Credit states
        "status_active": "Active",
        "status_free": "Free",
        "status_active_free": "Active (Free)",
        "status_unlimited": "Unlimited",
        "credits_unit": "{count} min",
        
        # Notifications & Credits
        "msg_no_api_token": "MVSEP API key is not configured! Click 'Get API Token' to open website and copy your key into settings.",
        "msg_no_file_selected": "Please select an audio file!",
        "msg_file_not_found": "File not found: {file}",
        "msg_starting_separation": "Starting separation using {model}...",
        "msg_done_saved": "Minus is ready! Saved to: {path}",
        "credit_deducted_notice": "Minus is ready! Credits used: {spent}. Remaining credits: {left}.",
        "credit_balance_speech": "Remaining credits on MVSEP account: {left}. Total separations done: {total}.",
        "credit_info_dialog_title": "MVSEP Credits Information",
        "credit_info_dialog_body": "MVSEP Account Details:\n\n• Remaining credits: {left}\n• Last deduction: {spent}\n• Total separations: {total}\n• API Token Status: Active\n\nMore details: https://mvsep.com/full_api",
        "credit_checking": "Checking credits...",
        
        "msg_upload_failed": "Failed to upload audio file to server: {error}",
        "msg_poll_timeout": "Server processing timed out.",
        "msg_invalid_token": "Invalid API token or unauthorized. Please verify in settings.",
        "msg_quota_exceeded": "Credits exhausted or quota exceeded. Please top up at https://mvsep.com",
        
        # Settings Panel
        "api_token_label": "MVSEP API Token:",
        "api_token_help": "To get your API token, click 'Get API Token' or visit https://mvsep.com/full_api",
        "btn_get_api_token": "Get API Token (Open Website)",
        "btn_test_token": "Test API Token",
        "btn_check_credits": "Check Credits",
        "show_key_label": "Show key",
        "api_key_dialog_title": "MVSEP API Key",
        "api_key_display_text": "Your API key:\n{key}",
        "token_testing": "Testing API token...",
        "token_valid": "API token is valid and active!",
        "token_invalid": "API token error: {error}",
        "default_model_label": "Default model:",
        "output_dir_label": "Output folder (leave empty to save next to original file):",
        "announce_progress_label": "Announce progress percentages",
        "play_sound_label": "Play sound when finished",
        "language_label": "Add-on language:",
        "lang_auto": "Automatic (NVDA language)",
        "lang_uz": "O'zbekcha",
        "lang_ru": "Русский",
        "lang_en": "English",
        
        # Explorer integration
        "explorer_file_detected": "Selected file: {name}. Starting minus creation...",
        "open_result_folder": "Open output folder",
        "open_result_file": "Play minus track"
    }
}

_current_lang = "auto"


def set_language(lang_code):
    global _current_lang
    _current_lang = lang_code


def get_current_language():
    global _current_lang
    if _current_lang and _current_lang != "auto" and _current_lang in MESSAGES:
        return _current_lang
    
    try:
        import languageHandler
        nvda_lang = languageHandler.getLanguage()
        if nvda_lang:
            lang_prefix = nvda_lang.split("_")[0].lower()
            if lang_prefix in MESSAGES:
                return lang_prefix
    except Exception:
        pass
    
    return "uz"


def _t(key, **kwargs):
    """Get localized string by key with keyword formatting."""
    lang = get_current_language()
    table = MESSAGES.get(lang, MESSAGES["uz"])
    template = table.get(key, MESSAGES["en"].get(key, key))
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            return template
    return template


def format_credit_display(raw_val):
    """
    Format credit value accurately into current language:
    - 0 or "active" or "free" -> "Faol (Bepul)" / "Активен (Бесплатно)" / "Active (Free)"
    - positive number -> "10 daqiqa" / "10 мин" / "10 min"
    - "unlimited" -> "Cheksiz" / "Неограниченно" / "Unlimited"
    """
    if raw_val is None:
        return _t("status_active_free")
        
    s_val = str(raw_val).strip().lower()
    
    if s_val in ["0", "faol", "mavjud", "bepul", "free", "active", "active_free", "bepul / faol"]:
        return _t("status_active_free")
        
    if s_val in ["unlimited", "cheksiz", "неограниченно"]:
        return _t("status_unlimited")
        
    # Check if number (e.g. 15, 20.5)
    try:
        num = float(s_val)
        if num == 0:
            return _t("status_active_free")
        int_num = int(num) if num.is_integer() else num
        return _t("credits_unit", count=int_num)
    except ValueError:
        pass
        
    return str(raw_val)
