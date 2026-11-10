import os, json, requests, time, telebot
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
FAL_KEY = os.getenv("FAL_KEY")
ADMIN_ID = 123456789
bot = telebot.TeleBot(BOT_TOKEN)
FILE = "users.json"
user_data = {}

def load_users():
    try:
        with open(FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return {}
def save_users(d):
    with open(FILE, "w", encoding="utf-8") as f: json.dump(d, f)

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "Привет! 📸 Отправь фото, сделаю видео!\n\n1-е видео - БЕСПЛАТНО 🎁\nДальше - 100 ⭐\nМузыку выберешь сам!")

@bot.message_handler(content_types=['photo'])
def photo(m):
    uid = str(m.chat.id)
    db = load_users()
    if db.get(uid, 0) >= 1:
        bot.send_message(m.chat.id, "Твоё бесплатное уже использовано! Напиши /buy для оплаты 100 ⭐")
        return
    file_info = bot.get_file(m.photo[-1].file_id)
    photo_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
    user_data[uid] = {"photo_url": photo_url}
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎵 Без музыки", callback_data="nomusic"))
    markup.add(types.InlineKeyboardButton("🕌 Нашид", callback_data="nashid"))
    markup.add(types.InlineKeyboardButton("📖 Сура", callback_data="sura"))
    markup.add(types.InlineKeyboardButton("🎤 Голос / Текст", callback_data="voice"))
    bot.send_message(m.chat.id, "Фото получил! 🔥 Что добавить? Выбери:", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: True)
def btn(c):
    uid = str(c.message.chat.id)
    choice = c.data
    user_data[uid]["choice"] = choice
    if choice == "nomusic":
        bot.send_message(c.message.chat.id, "Понял! Делаю видео без музыки... ⏳")
        make_video(c.message.chat.id, uid, "cinematic video, smooth motion, high quality")
    elif choice == "nashid":
        bot.send_message(c.message.chat.id, "🕌 Напиши название нашида, например: Я Расул Аллах")
        user_data[uid]["wait"] = "nashid_name"
    elif choice == "sura":
        bot.send_message(c.message.chat.id, "📖 Напиши какая сура, например: Ясин")
        user_data[uid]["wait"] = "sura_name"
    elif choice == "voice":
        bot.send_message(c.message.chat.id, "🎤 Напиши текст на любом языке, я озвучу его!")
        user_data[uid]["wait"] = "voice_text"

@bot.message_handler(content_types=['text'])
def text_h(m):
    uid = str(m.chat.id)
    if uid not in user_data or "wait" not in user_data[uid]: return
    wait = user_data[uid]["wait"]
    txt = m.text
    if wait == "nashid_name":
        bot.send_message(m.chat.id, f"Ищу нашид: {txt}... 🔍 Делаю видео ⏳")
        make_video(m.chat.id, uid, f"cinematic video with nashid {txt}, high quality")
    elif wait == "sura_name":
        bot.send_message(m.chat.id, f"Ищу суру: {txt}... 🔍 Делаю видео ⏳")
        make_video(m.chat.id, uid, f"cinematic video with Quran surah {txt}, high quality")
    elif wait == "voice_text":
        bot.send_message(m.chat.id, f"Озвучиваю: {txt}... 🎤 Делаю видео ⏳")
        make_video(m.chat.id, uid, f"cinematic video, voiceover: {txt}, high quality")

def make_video(chat_id, uid, prompt):
    photo_url = user_data[uid]["photo_url"]
    headers = {"Authorization": f"Key {FAL_KEY}", "Content-Type": "application/json"}
    data = {"image_url": photo_url, "prompt": prompt, "duration": "5"}
    r = requests.post("https://queue.fal.run/fal-ai/kling-video/v1.6/standard/image-to-video", headers=headers, json=data)
    if r.status_code != 200:
        bot.send_message(chat_id, "Ошибка нейросети, попробуй ещё раз")
        return
    req_id = r.json().get("request_id")
    video_url = None
    for _ in range(30):
        time.sleep(10)
        s = requests.get(f"https://queue.fal.run/fal-ai/kling-video/requests/{req_id}/status", headers=headers).json()
        if s.get("status") == "COMPLETED":
            video_url = s["response"]["video"]["url"]
            break
    if video_url:
        bot.send_video(chat_id, video_url, caption="Готово! 🎬 Твоё 1-е бесплатное видео!\nСледующее - 100 ⭐. Напиши /buy")
        db = load_users()
        db[uid] = db.get(uid, 0) + 1
        save_users(db)
        user_data.pop(uid, None)
    else:
        bot.send_message(chat_id, "Долго делается, попробуй позже")

@bot.message_handler(commands=['buy'])
def buy(m):
    bot.send_message(m.chat.id, "Для оплаты напиши админу, он откроет доступ ✅")

bot.polling(none_stop=True)
