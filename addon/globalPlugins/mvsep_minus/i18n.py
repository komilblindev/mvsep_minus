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
		"menu_direct_minus_desc": "Audio faylni oynasiz, to'g'ridan-to'g'ri minus qilish (Tezkor)",
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
		"cat_premium": "💎 Premium va Ansamble modellar",
		"cat_instruments": "🎸 Cholg'u asboblari",
		"cat_enhance": "🧹 Tozalash va Yaxshilash",
		"btn_add_fav": "⭐ Sevimlilarga qo'shish",
		"btn_remove_fav": "☆ Sevimlilardan chiqarish",
		"elapsed_time_notice": "Ajratish vaqti: {duration}.",
		"history_retention_label": "Tarix va statistika davri:",
		"period_1week": "1 hafta (7 kun)",
		"period_1month": "1 oy (30 kun)",
		"period_3months": "3 oy (90 kun)",
		"period_all": "Doimiy (Barchasi)",
		"history_stats_title": "Ajratishlar statistikasi:",
		"history_stats_summary": "Davr ({period}): Sarflangan vaqt: {total_time} | Minuslar soni: {count} ta | Sarflangan kredit: {spent} | Joriy balans: {balance}",
		"btn_open_history_file": "Tarix faylini ochish (Downloads)",
		"msg_history_file_not_found": "Tarix fayli hali mavjud emas. Birinchi minus qilingandan so'ng yaratiladi.",

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
		"status_active_free": "Bepul",
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
				"translate_models_label": "Model nomlarini tarjima qilingan holda ko'rsatish",
		"translate_models_help": "Yoqilsa, model nomlari va ularning vazifalari tanlangan tilda ko'rsatiladi.",
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
		"open_result_file": "Minusni tinglash",
		
		# In-Addon Account & Token Retrieval
						"account_selector_label": "Hisoblar ro'yxati:",
		"btn_delete_account": "Ro'yxatdan olib tashlash",
		"auto_switch_account_label": "Kredit yoki limit tugaganda keyingi hisobga avtomatik o'tish",
		"btn_open_errors_file": "Xatoliklar jurnalini ochish (txt)",
		"btn_send_error_dev": "Xatolikni dasturchiga jo'natish (hamzayevkomil52@gmail.com)",
		"msg_error_sent_opened": "Xatolik hisoboti buferga nusxalandi va dasturchiga ({email}) yuborish uchun pochta ochildi.",
		"msg_switching_account": "Hozirgi hisobda limit tugadi. Zaxira hisobga ({email}) o'tilmoqda va minus qilish davom ettirilmoqda...",
		"msg_all_accounts_exhausted": "Barcha MVSEP hisoblaringizda limit tugagan yoki kredit yetarli emas!",
		"msg_errors_file_not_found": "Xatoliklar jurnali bo'sh yoki hali yaratilmagan.",
		"msg_account_deleted": "Hisob ro'yxatdan olib tashlandi.",
		"btn_open_login": "Tizimga kirish...",
		"btn_open_register": "Ro'yxatdan o'tish...",
		"dialog_login_title": "MVSEP Tizimiga Kirish",
		"dialog_register_title": "MVSEP da Ro'yxatdan O'tish",
		"btn_login_account": "Hisob orqali kalitni olish...",
		"btn_copy_token": "API kalitni buferga nusxalash",
		"msg_token_copied": "API kaliti buferga nusxalandi.",
		"btn_open_account_file": "Hisob faylini ochish (Downloads)",
		"msg_account_file_not_found": "Hisob fayli topilmadi: {path}",
		"login_dialog_title": "MVSEP Hisob va API Kalit Olish",
		"mode_login": "Mavjud hisobga kirish",
		"mode_register": "Yangi hisob ochish",
		"name_label": "Ismingiz:",
		"email_label": "Email pochtangiz:",
		"password_label": "MVSEP paroli (kamida 6 ta belgi):",
		"password_confirm_label": "Parolni takrorlang:",
		"show_password_label": "Parolni ko'rsatish",
		"save_account_label": "Hisob ma'lumotlarini Yuklanmalar (Downloads) papkasiga saqlash",
		"btn_do_login": "Kirish va API kalitni olish",
		"btn_do_register": "Ro'yxatdan o'tish va API kalitni olish",
		"btn_open_browser_api": "Google / Sayt orqali olish (Brauzerda ochish)",
		"login_in_progress": "MVSEP tizimiga kirilmoqda...",
		"register_in_progress": "MVSEP tizimida ro'yxatdan o'tilmoqda...",
		"login_success": "Muvaffaqiyatli kirildi! API kalit olindi va saqlandi. Balans: {credits}.",
		"register_success": "Ro'yxatdan muvaffaqiyatli o'tildi! MVSEP pochtangizga tasdiqlash xati yubordi. Pochtadagi havolani tasdiqlab, so'ng tizimga kiring.",
		"account_saved_to_path": "Hisob ma'lumotlari Yuklanmalar papkasidagi mvsep_account.txt fayliga saqlandi.",
		"err_fill_all_fields": "Iltimos, barcha majburiy maydonlarni to'ldiring!",
		"err_pwd_short": "Parol kamida 6 ta belgidan iborat bo'lishi kerak!",
		"err_pwd_mismatch": "Kiritilgan parollar bir-biriga mos kelmadi!",
		"audio_url_label": "Yoki audio havolasi (URL):",
		"btn_check_queue": "Server navbatini tekshirish",
		"msg_queue_status": "Server navbati: {proc} ta bajarilmoqda, {prem} ta premium, {free} ta bepul kutmoqda.",
		"btn_open_site_history": "Saytdagi ajratishlar tarixi...",
		"dialog_site_history_title": "Saytdagi Ajratishlar Tarixi (MVSEP)",
		"msg_total_tracks_count": "Jami: {count} ta trek",
		"history_list_label": "Oldin ajratilgan treklar:",
		"btn_download_selected": "Tanlangan trekni yuklab olish",
		"btn_refresh_history": "Tarixni yangilash",
		"msg_loading_history": "Saytdan ajratishlar tarixi yuklanmoqda...",
		"msg_no_history_found": "Saytda hech qanday ajratish tarixi topilmadi.",
		"msg_history_file_expired": "Ushbu trek serverda muddati o'tganligi sababli o'chirilgan.",
		"msg_downloading_history_track": "{name} treki yuklab olinmoqda...",
		"msg_history_download_success": "Trek muvaffaqiyatli yuklab olindi!",
	},
	"ru": {
		"addon_name": "MVSEP Создатель Минусов",
		"menu_create_minus": "MVSEP: Создать минус...",
		"menu_create_minus_desc": "Разделить аудиофайл на вокал и инструментал (минусовку)",
		"menu_direct_minus_desc": "Быстро разделить аудиофайл (без открытия диалога)",
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
		"cat_premium": "💎 Премиум и Ансамбли",
		"cat_instruments": "🎸 Музыкальные инструменты",
		"cat_enhance": "🧹 Очистка и Улучшение",
		"btn_add_fav": "⭐ В избранное",
		"btn_remove_fav": "☆ Удалить из избранного",
		"elapsed_time_notice": "Время разделения: {duration}.",
		"history_retention_label": "Срок хранения истории и статистики:",
		"period_1week": "1 неделя (7 дней)",
		"period_1month": "1 месяц (30 дней)",
		"period_3months": "3 месяца (90 дней)",
		"period_all": "Все время (Без ограничений)",
		"history_stats_title": "Статистика разделений:",
		"history_stats_summary": "Период ({period}): Затрачено времени: {total_time} | Всего минусов: {count} | Потрачено кредитов: {spent} | Текущий баланс: {balance}",
		"btn_open_history_file": "Открыть файл истории (Downloads)",
		"msg_history_file_not_found": "Файл истории еще не создан. Он появится после первого разделения.",

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
		"status_active_free": "Бесплатно",
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
				"translate_models_label": "Отображать названия моделей с переводом",
		"translate_models_help": "Если включено, названия и назначения моделей отображаются на выбранном языке.",
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
		"open_result_file": "Прослушать минус",
		
		# In-Addon Account & Token Retrieval
						"account_selector_label": "Список аккаунтов:",
		"btn_delete_account": "Удалить из списка",
		"auto_switch_account_label": "Автоматически переключаться на следующий аккаунт при исчерпании лимита",
		"btn_open_errors_file": "Открыть журнал ошибок (txt)",
		"btn_send_error_dev": "Отправить отчет об ошибке разработчику (hamzayevkomil52@gmail.com)",
		"msg_error_sent_opened": "Отчет об ошибке скопирован в буфер и открыта почта для отправки разработчику ({email}).",
		"msg_switching_account": "На текущем аккаунте исчерпан лимит. Переключение на запасной аккаунт ({email}) и продолжение разделения...",
		"msg_all_accounts_exhausted": "На всех ваших аккаунтах MVSEP исчерпан лимит или недостаточно кредитов!",
		"msg_errors_file_not_found": "Журнал ошибок пуст или еще не создан.",
		"msg_account_deleted": "Аккаунт удален из списка.",
		"btn_open_login": "Войти в аккаунт...",
		"btn_open_register": "Регистрация...",
		"dialog_login_title": "Вход в аккаунт MVSEP",
		"dialog_register_title": "Регистрация в MVSEP",
		"btn_login_account": "Получить ключ через аккаунт...",
		"btn_copy_token": "Копировать API ключ в буфер",
		"msg_token_copied": "API ключ скопирован в буфер обмена.",
		"btn_open_account_file": "Открыть файл аккаунта (Downloads)",
		"msg_account_file_not_found": "Файл аккаунта не найден: {path}",
		"login_dialog_title": "Аккаунт MVSEP и получение API ключа",
		"mode_login": "Войти в существующий аккаунт",
		"mode_register": "Создать новый аккаунт",
		"name_label": "Ваше имя:",
		"email_label": "Ваш email:",
		"password_label": "Пароль MVSEP (минимум 6 символов):",
		"password_confirm_label": "Повторите пароль:",
		"show_password_label": "Показать пароль",
		"save_account_label": "Сохранить данные аккаунта в папку Загрузки (Downloads)",
		"btn_do_login": "Войти и получить API ключ",
		"btn_do_register": "Зарегистрироваться и получить API ключ",
		"btn_open_browser_api": "Получить через Google / Сайт (Открыть браузер)",
		"login_in_progress": "Выполняется вход в MVSEP...",
		"register_in_progress": "Выполняется регистрация в MVSEP...",
		"login_success": "Успешный вход! API ключ получен и сохранен. Баланс: {credits}.",
		"register_success": "Регистрация прошла успешно! MVSEP отправил письмо с подтверждением на вашу почту. Подтвердите ссылку в письме и затем войдите в аккаунт.",
		"account_saved_to_path": "Данные аккаунта сохранены в файл mvsep_account.txt в папке Загрузки.",
		"err_fill_all_fields": "Пожалуйста, заполните все обязательные поля!",
		"err_pwd_short": "Пароль должен содержать не менее 6 символов!",
		"err_pwd_mismatch": "Введенные пароли не совпадают!",
		"audio_url_label": "Или ссылка на аудио (URL):",
		"btn_check_queue": "Проверить очередь сервера",
		"msg_queue_status": "Очередь сервера: {proc} выполняется, {prem} премиум, {free} бесплатно в очереди.",
		"btn_open_site_history": "История разделений на сайте...",
		"dialog_site_history_title": "История Разделений на Сайте (MVSEP)",
		"msg_total_tracks_count": "Всего: {count} треков",
		"history_list_label": "Ранее разделенные треки:",
		"btn_download_selected": "Скачать выбранный трек",
		"btn_refresh_history": "Обновить историю",
		"msg_loading_history": "Загрузка истории разделений с сайта...",
		"msg_no_history_found": "На сайте не найдено истории разделений.",
		"msg_history_file_expired": "Файлы этого трека уже удалены с сервера по истечении срока хранения.",
		"msg_downloading_history_track": "Скачивание трека {name}...",
		"msg_history_download_success": "Трек успешно скачан!",
	},
	"en": {
		"addon_name": "MVSEP Minus Creator",
		"menu_create_minus": "MVSEP: Create Minus / Instrumental...",
		"menu_create_minus_desc": "Separate audio file into vocals and instrumental (minus)",
		"menu_direct_minus_desc": "Directly separate audio file without opening dialog (Quick)",
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
		"cat_premium": "💎 Premium & Ensemble Models",
		"cat_instruments": "🎸 Musical Instruments",
		"cat_enhance": "🧹 Clean & Enhancement",
		"btn_add_fav": "⭐ Add to favorites",
		"btn_remove_fav": "☆ Remove from favorites",
		"elapsed_time_notice": "Separation time: {duration}.",
		"history_retention_label": "History & statistics period:",
		"period_1week": "1 week (7 days)",
		"period_1month": "1 month (30 days)",
		"period_3months": "3 months (90 days)",
		"period_all": "All time (Unlimited)",
		"history_stats_title": "Separation statistics:",
		"history_stats_summary": "Period ({period}): Time spent: {total_time} | Total tracks: {count} | Credits spent: {spent} | Current balance: {balance}",
		"btn_open_history_file": "Open history file (Downloads)",
		"msg_history_file_not_found": "History file does not exist yet. It will be created after the first separation.",

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
		"status_active_free": "Free",
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
				"translate_models_label": "Display translated model names",
		"translate_models_help": "If enabled, model names and purposes will be displayed in the selected language.",
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
		"open_result_file": "Play minus track",
		
		# In-Addon Account & Token Retrieval
				"account_selector_label": "Accounts list:",
		"btn_delete_account": "Remove from list",
		"auto_switch_account_label": "Automatically switch to next account when quota/credits exhausted",
		"btn_open_errors_file": "Open error log (txt)",
		"btn_send_error_dev": "Send error report to developer (hamzayevkomil52@gmail.com)",
		"msg_error_sent_opened": "Error report copied to clipboard and email client opened to send to {email}.",
		"msg_switching_account": "Quota exceeded on current account. Switching to backup account ({email}) and continuing separation...",
		"msg_all_accounts_exhausted": "Quota exceeded or insufficient credits on all of your MVSEP accounts!",
		"msg_errors_file_not_found": "Error log is empty or does not exist yet.",
		"msg_account_deleted": "Account removed from list.",
		"btn_open_login": "Sign in...",
		"btn_open_register": "Register...",
		"dialog_login_title": "Sign in to MVSEP",
		"dialog_register_title": "Register on MVSEP",
		"btn_login_account": "Get key via account...",
		"btn_copy_token": "Copy API key to clipboard",
		"msg_token_copied": "API key copied to clipboard.",
		"btn_open_account_file": "Open account file (Downloads)",
		"msg_account_file_not_found": "Account file not found: {path}",
		"login_dialog_title": "MVSEP Account & Get API Key",
		"mode_login": "Sign in to existing account",
		"mode_register": "Create new account",
		"name_label": "Your name:",
		"email_label": "Your email:",
		"password_label": "MVSEP password (min 6 characters):",
		"password_confirm_label": "Confirm password:",
		"show_password_label": "Show password",
		"save_account_label": "Save account details to Downloads folder",
		"btn_do_login": "Sign In & Get API Key",
		"btn_do_register": "Register & Get API Key",
		"btn_open_browser_api": "Get via Google / Website (Open browser)",
		"login_in_progress": "Signing in to MVSEP...",
		"register_in_progress": "Registering in MVSEP...",
		"login_success": "Successfully signed in! API key obtained and saved. Balance: {credits}.",
		"register_success": "Registration successful! MVSEP sent a verification email to your address. Please verify the link in your email and then sign in.",
		"account_saved_to_path": "Account details saved to mvsep_account.txt in Downloads folder.",
		"err_fill_all_fields": "Please fill in all required fields!",
		"err_pwd_short": "Password must be at least 6 characters!",
		"err_pwd_mismatch": "Entered passwords do not match!",
		"audio_url_label": "Or audio URL:",
		"btn_check_queue": "Check server queue",
		"msg_queue_status": "Server queue: {proc} processing, {prem} premium, {free} free in queue.",
		"btn_open_site_history": "Site separation history...",
		"dialog_site_history_title": "Site Separation History (MVSEP)",
		"msg_total_tracks_count": "Total: {count} tracks",
		"history_list_label": "Previously separated tracks:",
		"btn_download_selected": "Download selected track",
		"btn_refresh_history": "Refresh history",
		"msg_loading_history": "Loading separation history from site...",
		"msg_no_history_found": "No separation history found on site.",
		"msg_history_file_expired": "Files for this track have expired and been removed from server.",
		"msg_downloading_history_track": "Downloading track {name}...",
		"msg_history_download_success": "Track successfully downloaded!",
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


def format_duration(seconds, lang=None):
	"""Format seconds into readable string according to language."""
	if lang is None:
		lang = get_current_language()
	s = int(seconds)
	m, s = divmod(s, 60)
	if lang == "uz":
		if m > 0:
			return f"{m} daqiqa {s} soniya"
		return f"{s} soniya"
	elif lang == "ru":
		if m > 0:
			return f"{m} мин. {s} сек."
		return f"{s} сек."
	else:
		if m > 0:
			return f"{m} min {s} sec"
		return f"{s} sec"
