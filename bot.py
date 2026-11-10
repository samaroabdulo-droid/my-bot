import os
import telebot
from telebot import types

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 6776153004

bot = telebot.TeleBot(TOKEN)
users = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
        "Привет! 👋 Отправь фото, сделаю видео!\n\n"
        "1-е видео - БЕСПЛАТНО 🎁\n"
        "Дальше - 100 ⭐\n"
        "Музыку выберешь сам!")
    users[message.from_user.id] = {'step': 'photo'}
    bot.send_message(message.chat.id, "📸 Отправь своё фото:")

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    uid = message.from_user.id
    if uid not in users:
        users[uid] = {}
    users[uid]['photo'] = message.photo[-1].file_id
    users[uid]['step'] = 'music'

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎵 Без музыки", callback_data="music_none"))
    markup.add(types.InlineKeyboardButton("🕌 Нашид", callback_data="music_nashid"))
    markup.add(types.InlineKeyboardButton("📖 Сура", callback_data="music_sura"))
    markup.add(types.InlineKeyboardButton("🎤 Голос / Текст", callback_data="music_voice"))
    bot.send_message(message.chat.id, "Фото получил! 🔥 Что добавить? Выбери:", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith('music_'))
def music(call):
    uid = call.from_user.id
    music_map = {
        'music_none': 'Без музыки',
        'music_nashid': 'Нашид',
        'music_sura': 'Сура',
        'music_voice': 'Голос / Текст'
    }
    users[uid]['music'] = music_map.get(call.data, 'Без музыки')
    users[uid]['step'] = 'text'
    bot.send_message(call.message.chat.id, f"Понял! Музыка: {users[uid]['music']}\n\n✍️ Теперь напиши текст, что должно быть в видео:")

@bot.message_handler(func=lambda m: users.get(m.from_user.id, {}).get('step') == 'text')
def get_text(message):
    uid = message.from_user.id
    text = message.text
    music = users[uid].get('music', 'Без музыки')
    photo = users[uid].get('photo')

    try:
        bot.send_message(ADMIN_ID, f"🔥 НОВЫЙ ЗАКАЗ!\nОт: @{message.from_user.username} ID:{uid}\nМузыка: {music}\nТекст: {text}")
        if photo:
            bot.send_photo(ADMIN_ID, photo)
    except Exception as e:
        print(f"Не смог отправить админу: {e}")

    users[uid]['step'] = None
    bot.send_message(message.chat.id, "✅ Заказ принят! Делаю видео... ⏳\nЖди 10-15 минут, я пришлю сюда.")

@bot.message_handler(func=lambda m: True)
def other(message):
    bot.send_message(message.chat.id, "Нажми /start и отправь фото 📸")

print("Бот запущен!")
bot.polling(none_stop=True)
