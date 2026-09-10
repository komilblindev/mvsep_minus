# MVSEP Minus Yaratuvchi - NVDA Plagini

Audio fayllardan vokalni tozalash va professional sifatli **minus / instrumental** yaratish uchun mo'ljallangan maxsus NVDA ekranni o'qish dasturi plagini. Ushbu plagin rasmiy [MVSEP.com](https://mvsep.com/full_api) bulutli sun'iy intellekt API tizimi bilan to'liq integratsiya qilingan.

---

## 📖 Foydalanish Qo'llanmasi (Qadamma-qadam)

### 1-qadam: Akkaunt ulash va API kalit olish
Plagindan foydalanish uchun bir martalik bepul MVSEP API kaliti kerak bo'ladi.

> ⚠️ **DIQQAT: Pochta orqali tasdiqlash xati kechikishi yoki kelmasligi mumkin!**  
> MVSEP xalqaro xizmati bo'lgani sababli, email orqali yangi hisob ochganda tasdiqlash xatlari pochtaga (Gmail, Mail.ru va h.k.) yetib bormasligi yoki qattiq kechikishi mumkin (`Pending email verification` xatosi).  
> **Eng to'g'ri, xatosiz va 100% tezkor yo'l**:
> 1. `NVDA menyusi -> Parametrlar -> Sozlamalar -> MVSEP Minus` bo'limiga kiring;
> 2. "Tizimga kirish..." yoki "Ro'yxatdan o'tish..." tugmasini bosing;
> 3. Ochilgan oynada **`Google / Sayt orqali olish (Brauzerda ochish)`** tugmasini bosing;
> 4. Brauzeringizda MVSEP ochilganda **"Sign in with Google"** (Google orqali kirish) tugmasini bosing;
> 5. Sahifada (`https://mvsep.com/full_api`) tayyor **API Token** chiqadi, uni nusxalab oling (`Ctrl + C`);
> 6. Plagin sozlamalaridagi **"MVSEP API Kaliti"** maydoniga qo'ying va **"API kalitini tekshirish"** tugmasini bosing.

---

### 2-qadam: Musiqani minus qilish (Asosiy rejim)
1. Klaviaturada `NVDA menyusi -> Vositalar (Servis) -> MVSEP: Musiqani minus qilish...` bandini tanlang (yoki o'zingiz biriktirgan tezkor tugmani bosing);
2. Ochilgan oynada:
   - **Fayl orqali**: "Faylni tanlash..." tugmasini bosib, kompyuteringizdagi audio faylni (MP3, WAV, FLAC, M4A, OGG) tanlang;
   - **URL orqali**: Agar fayl internetda bo'lsa, havolani (Google Drive, Dropbox, MEGA yoki to'g'ridan-to'g'ri audio linkini) maxsus qatorga kiriting;
3. **Modelni tanlash**: Standart holatda `BS Roformer (vocals, instrumental)` tavsiya etiladi (eng toza sifat);
4. **Natija turi**: Vokalni olib tashlash (Faqat instrumental), Faqat vokal yoki Ikkalasini ham yuklab olish;
5. **Format**: MP3 (320 kbps), WAV (asl sifat) yoki FLAC;
6. **"Minus qilishni boshlash"** (`B` yoki `Alt+S`) tugmasini bosing.
7. Jarayon davomida NVDA progress signallari (bip tovushlari) eshitilib turadi. Ish yakunlangach, tayyor audio fayl **`Downloads/MVSEP_Minus`** jildiga avtomatik yuklab olinadi va ovozli e'lon qilinadi.

---

### 3-qadam: Fon rejimida tezkor minus qilish (Tezkor rejim)
1. Windows Explorer (Fayl boshqaruvchisi)da istalgan audio faylni belgilang;
2. Plagin uchun biriktirilgan tezkor tugmani bosing;
3. Plagin hech qanday oyna ochmasdan, fon rejimida oxirgi saqlangan parametrlar asosida faylni serverga yuboradi va natijani tayyorlab beradi.

---

### 4-qadam: Saytdagi ajratishlar tarixi va qayta yuklab olish
1. `NVDA menyusi -> Parametrlar -> Sozlamalar -> MVSEP Minus` bo'limiga kiring;
2. **"Saytdagi ajratishlar tarixi..."** tugmasini bosing;
3. Hisobingizda oldin ajratilgan barcha treklarning ro'yxati (fayl nomi, model, sanasi) chiqadi;
4. Xohlagan trekni tanlab, **"Yuklab olish"** tugmasini bossangiz, fayl darhol kompyuteringizga yuklanadi.

---

## 🌟 Asosiy Imkoniyatlar

- **Ko'p Akkauntlar Boshqaruvi (Multi-Account)**:
  - Bir nechta hisob yoki API kalitlarini saqlash va ular o'rtasida oson almashish;
  - Har bir hisobning qolgan balans va daqiqalari ro'yxatda aniq ko'rinadi;
  - "Ro'yxatdan olib tashlash" tugmasi orqali eskirgan hisobni o'chirish.
- **Avtomatik Zaxira Hisobiga O'tish (Failover)**:
  - Faol hisobda kredit tugasa yoki navbat limiti yetsa (`Not enough credits` / `Queue limit reached`), avtomatik navbatdagi hisobga o'tib, jarayonni to'xtatmasdan davom ettiradi.
- **Serverdagi Jonli Navbatni Tekshirish (Live Server Queue)**:
  - Serverdagi ish yuki va kutish navbatini ovozli bilish.
- **Masofaviy Audio Havolasi (URL) orqali Minus Qilish**:
  - Google Drive, Dropbox, MEGA va Direct audio linklaridan foydalanish.
- **Xatoliklar Jurnali va Dasturchiga Xabar Berish**:
  - Barcha jarayon xatoliklari `Downloads/MVSEP_Minus/mvsep_errors.txt` fayliga yoziladi va bir tugma orqali dasturchiga xat ochiladi.
- **FFmpeg Talab Qilinmaydi**:
  - Barcha hisob-kitoblar MVSEP bulutli serverlarida amalga oshiriladi.
- **3 Tilda Mukammal Interfeys**:
  - O'zbekcha, Ruscha va Inglizcha 100% to'liq qo'llab-quvvatlanadi.

---

## 🎧 Sun'iy Intellekt Modellari va Kategoriyalar

Plaginda 35 dan ortiq saralangan eng sara modellar va jami **119 ta rasmiy algoritm** mavjud:

### 1. Minus va Vokal Ajratish Modellari (Minus & Vocal Separation)
- `BS Roformer (vocals, instrumental)` ⭐ - Dunyo bo'yicha eng yuqori sifatli va toza vokal/minus ajratuvchi model (tavsiya etiladi);
- `MelBand Roformer (vocals, instrumental)` - Yuqori dinamik diapazon va tiniq vokal;
- `SCNet Large (vocals, instrumental)` - Murakkab va zich musiqiy aralashmalar uchun kuchli model;
- `MDX23C (vocals, instrumental)` - Zamonaviy tezkor gibrid arxitektura;
- `Demucs v4 HT (vocals, instrum)` - Meta AI tomonidan yaratilgan yuqori aniqlikdagi model;
- `BS PolarFormer (vocals, instrumental)` - Faza va stereo kenglikni saqlovchi yangi avlod modeli;
- `Ultimate Vocal Remover VR` - Klassik akustik va jonli yozuvlar uchun model;
- `Karaoke (Backing vocals)` - Asosiy yakkaxon vokalni olib tashlab, xordagi bek-vokallarni instrumental bilan birga saqlab qolish;
- `MDX-B Karaoke` - Bek-vokalni saqlab qoluvchi tezkor model;
- `MVSep Male/Female separation` - Erkak va ayol ovozlarini alohida yo'laklarga ajratish;
- `Medley Vox (Multi-singer separation)` - Bir nechta birga kuylayotgan ijrochilar ovozini alohida ajratish;
- `MVSep Choir & SATB Choir` - Xor guruhlari va klassik xor qismlarini (soprano, alto, tenor, bas) ajratish.

### 2. Premium va Ko'p Stemli Ansamble Modellari (Premium & Ensembles)
- `Ensemble (vocals, instrum)` [2x koeffitsiyent] - Eng sara modellarning birlashtirilgan eng yuqori sifatli miksi;
- `Ensemble (vocals, instrum, bass, drums, other)` [4x koeffitsiyent];
- `Ensemble All-In (vocals, bass, drums, piano, guitar, lead/back, other)` [6x koeffitsiyent];
- `BS Roformer SW (6 stems)` - Vokal, bas, baraban, gitara, pianino va boshqalar;
- `Demucs4 HT (4 stems)` - Klassik 4-stem ajratish;
- `Mega 53-stem Model` - Audioni 53 tagacha alohida yo'laklarga ajratish imkoniyati.

### 3. Audio Tozalash va Yaxshilash Modellari (Enhancement & Clean)
- `Reverb Removal (noreverb)` - Xonadagi aks-sado, xol va reverberatsiyani tozalash;
- `DeNoise (aufr33 & gabox)` - Fon shovqini, shovqinli g'uvillashlarni ketkazish;
- `Apollo Enhancers` - Eski va sifatsiz audio yozuvlar sifatini tiklash va yaxshilash;
- `AudioSR & FlashSR (Super Resolution)` - Siqilgan past sifatli audioni studiya darajasiga ko'tarish;
- `MVSep Crowd removal` - Olomon, konsert shovqinlarini musiqadan ajratish;
- `BandIt Plus & MVSep DnR v3` - Nutq, musiqa va tovush effektlarini (DNR) bir-biridan ajratish;
- `MVSep Braam, Risers, FX` - Kinematografik tovush effektlarini ajratish.

### 4. Alohida Musiqa Asboblari Modellari (Musical Instruments)
- **Zarbli**: `Drums`, `DrumSep` (kick, snare, cymbals, toms, ride, hi-hat, crash);
- **Klavishli**: `Piano`, `Digital Piano`, `Keys`, `Organ`, `Harpsichord`, `Accordion`, `Celesta`, `Rhodes`, `Clavinet`;
- **Torli**: `Bass`, `Guitar`, `Acoustic Guitar`, `Electric Guitar`, `Lead/Rhythm Guitar`, `Plucked Strings`, `Harp`, `Mandolin`, `Banjo`, `Sitar`, `Ukulele`;
- **Kamonli torli**: `Violin`, `Viola`, `Cello`, `Double Bass`, `Bowed Strings`;
- **Damli cholg'ular**: `Saxophone`, `Flute`, `Trumpet`, `Trombone`, `Clarinet`, `Oboe`, `French Horn`, `Harmonica`, `Tuba`, `Bassoon`, `Bagpipes`;
- **Perkussiya va boshqalar**: `Tambourine`, `Marimba`, `Glockenspiel`, `Timpani`, `Triangle`, `Congas`, `Bells`, `Xylophone`, `Vibraphone`, `Clap`, `Cowbell`.

---

## ⌨️ Boshqaruv Tugmalari (Input Gestures)

Boshqa plaginlar yoki tizim tugmalari bilan to'qnashuv bo'lmasligi uchun, **sukut bo'yicha global tezkor tugmalar biriktirilmagan**.

O'zingizga qulay tugmalarni `NVDA menyusi -> Parametrlar -> Boshqaruv tugmalari (Input Gestures) -> MVSEP Minus Yaratuvchi` bo'limidan biriktirishingiz mumkin:
- **Audio faylni vokal va instrumentalga ajratib minus yaratish**: Asosiy ajratish dialogini ochish.
- **Audio faylni oynasiz, to'g'ridan-to'g'ri minus qilish (Tezkor)**: Tanlangan fayl uchun fon rejimida ajratishni boshlash.
- **MVSEP hisobidagi qolgan kreditlar va balansni tekshirish**: Qolgan kredit va daqiqalarni ovozli eshitish.
- **MVSEP API kaliti va minus parametrlarini sozlash**: Plagin sozlamalari oynasini ochish.

---

## ⚙️ O'rnatish va Talablar

- **NVDA Versiyalari**: NVDA 2019.3 dan NVDA 2026.2 gacha to'liq mos keladi.
- **Python**: Python 3.7 — Python 3.13+.
- **Tashqi fayllar**: Hech qanday qo'shimcha binary yoki FFmpeg talab qilinmaydi.

---

## 📄 Litsenziya va Mualliflik Huquqi

- **Litsenziya**: GNU General Public License v2.0 (GPL-2.0).
- **Dasturchi**: Komil Hamzayev
- **Email**: [hamzayevkomil52@gmail.com](mailto:hamzayevkomil52@gmail.com)
- **Telegram Kanal**: [@it_help_uz](https://t.me/it_help_uz)
- **GitHub**: [github.com/komilblindev/mvsep_minus](https://github.com/komilblindev/mvsep_minus)
- **Rasmiy API**: [https://mvsep.com/full_api](https://mvsep.com/full_api)
