import telebot
from telebot import types
import json
import os

TOKEN = "9268527081:AAE1NghlmqhegNpVc6rkzjpsCergzyzulU4"
ADMIN_ID = 123456789

bot = telebot.TeleBot(TOKEN)

# --- ПАМЯТЬ: сохраняем в файл, чтобы не забывал ---
FILE = "users.json"

def load_users():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False)

users = load_users()  # user_id (как текст) -> {'lang':..., 'free_used': True/False, ...}

TEXTS = {
    'ru': {'choose': '🌍 Выбери свой язык:', 'hello': '👋 Привет! Я делаю видео из фото!\n\n🎁 1-е видео - БЕСПЛАТНО\n💰 Дальше - всего 3$ за видео\n⚡ ТУРБО +1$ - видео за 1-3 мин!\n\nНажми кнопку ниже:', 'btn_create': '🎬 Создать видео', 'btn_price': '💰 Цены', 'send_photo': '📸 Отправь мне фото (твое лицо):', 'send_text': '✍️ Теперь напиши текст, что должно быть в видео. Например: "Мужчина в костюме идет по Душанбе и говорит..."', 'wait': '⏳ Твой заказ принят! Делаю видео... Жди 10-15 минут, я пришлю сюда.', 'wait_turbo': '⚡ ТУРБО заказ принят! Делаю видео ПЕРВЫМ... Жди 1-3 минуты, я пришлю сюда!', 'free_info': '🎁 Это твое БЕСПЛАТНОЕ видео!', 'pay_info': '💰 Это видео стоит 3$.', 'price': '💰 ЦЕНЫ:\n\n🎁 1-е видео - 0$ БЕСПЛАТНО\n🎬 2-е и дальше - 3$ за видео\n⚡ ТУРБО +1$ - всего 4$, видео за 1-3 мин!',
           'choose_speed': '⚡ Выбери скорость:\n\n⚡ ТУРБО - 4$ всего, видео за 1-3 мин\n🐢 Обычный - 3$, видео за 10-15 мин',
           'turbo_on': '⚡ ТУРБО включен! +1$\nИтого к оплате: 4$\nТеперь отправь фото 👇',
           'turbo_off': '🐢 Обычный режим.\nИтого к оплате: 3$\nТеперь отправь фото 👇',
           'btn_turbo': '⚡ ТУРБО +1$ - 1-3 мин',
           'btn_normal': '🐢 Обычный 3$ - 10-15 мин'},
    'en': {'choose': '🌍 Choose your language:', 'hello': '👋 Hi! I make videos from your photo!\n\n🎁 1st video - FREE\n💰 Next - only 3$ per video\n⚡ TURBO +1$ - video in 1-3 min!\n\nPress button below:', 'btn_create': '🎬 Create video', 'btn_price': '💰 Prices', 'send_photo': '📸 Send me your photo (your face):', 'send_text': '✍️ Now write text for video.', 'wait': '⏳ Order accepted! Making video... Wait 10-15 min.', 'wait_turbo': '⚡ TURBO order accepted! Making your video FIRST... Wait 1-3 min!', 'free_info': '🎁 This is your FREE video!', 'pay_info': '💰 This video costs 3$.', 'price': '💰 PRICES:\n\n🎁 1st video - 0$ FREE\n🎬 Next - 3$ per video\n⚡ TURBO +1$ - 4$ total, video in 1-3 min!',
           'choose_speed': '⚡ Choose speed:\n\n⚡ TURBO - 4$ total, video in 1-3 min\n🐢 Normal - 3$, video in 10-15 min',
           'turbo_on': '⚡ TURBO ON! +1$\nTotal to pay: 4$\nNow send photo 👇',
           'turbo_off': '🐢 Normal mode.\nTotal to pay: 3$\nNow send photo 👇',
           'btn_turbo': '⚡ TURBO +1$ - 1-3 min',
           'btn_normal': '🐢 Normal 3$ - 10-15 min'},
    'tj': {'choose': '🌍 Забони худро интихоб کن:', 'hello': '👋 Салом! Ман аз акси ту видео месозам!\n\n🎁 Видеои 1-ум - РОЙГОН\n💰 Баъд - ҳамагӣ 3$ барои видео\n⚡ ТУРБО +1$ - видео дар 1-3 дақиқа!', 'btn_create': '🎬 Видео сохтан', 'btn_price': '💰 Нархҳо', 'send_photo': '📸 Акси худро фирист (рӯи ту):', 'send_text': '✍️ Ҳоло матнро нависед, дар видео чӣ бояд бошад.', 'wait': '⏳ Фармоиш қабул шуд! Видео сохта истодаам... 10-15 дақиқа интизор шав.', 'wait_turbo': '⚡ Фармоиши ТУРБО қабул шуд! Видеои туро АВВАЛ месозам... 1-3 дақиқа интизор шав!', 'free_info': '🎁 Ин видеои РОЙГОН-и ту!', 'pay_info': '💰 Ин видео 3$ аст.', 'price': '💰 НАРХҲО:\n\n🎁 1-ум - 0$ РОЙГОН\n🎬 Баъд - 3$\n⚡ ТУРБО +1$ - ҳамагӣ 4$, видео дар 1-3 дақиқа!',
           'choose_speed': '⚡ Суръатро интихоб кун:\n\n⚡ ТУРБО - ҳамагӣ 4$, видео дар 1-3 дақиқа\n🐢 Оддӣ - 3$, видео дар 10-15 дақиқа',
           'turbo_on': '⚡ ТУРБО фурӯзон! +1$\nҲамагӣ барои пардохт: 4$\nҲоло аксро фирист 👇',
           'turbo_off': '🐢 Реҷаи оддӣ.\nҲамагӣ барои пардохт: 3$\nҲоло аксро фирист 👇',
           'btn_turbo': '⚡ ТУРБО +1$ - 1-3 дақ',
           'btn_normal': '🐢 Оддӣ 3$ - 10-15 дақ'},
}

def get_user(uid):
    uid = str(uid)
    if uid not in users:
        users[uid] = {'lang': 'ru', 'free_used': False}
    return users[uid]

def get_text(user_id, key):
    u = get_user(user_id)
    lang = u.get('lang', 'ru')
    return TEXTS.get(lang, TEXTS['ru']).get(key, key)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        types.InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"),
        types.InlineKeyboardButton("🇹🇯 Тоҷикӣ", callback_data="lang_tj"),
        types.InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz"),
        types.InlineKeyboardButton("🇹🇷 Türkçe", callback_data="lang_tr"),
        types.InlineKeyboardButton("🇦🇪 العربية", callback_data="lang_ar"),
    ]
    markup.add(*btns)
    bot.send_message(message.chat.id, "🌍 Choose your language / Выбери свой язык / Забонатро интихоб кун:", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith('lang_'))
def set_lang(call):
    lang = call.data.split('_')[1]
    if lang not in TEXTS:
        lang = 'ru'
    u = get_user(call.from_user.id)
    u['lang'] = lang
    save_users()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(get_text(call.from_user.id, 'btn_create')))
    markup.add(types.KeyboardButton(get_text(call.from_user.id, 'btn_price')))
    bot.send_message(call.message.chat.id, get_text(call.from_user.id, 'hello'), reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data in ["turbo_yes", "turbo_no"])
def turbo_choose(call):
    uid = call.from_user.id
    u = get_user(uid)
    if call.data == "turbo_yes":
        u['turbo'] = True
        u['price'] = 4
        bot.send_message(call.message.chat.id, get_text(uid, 'turbo_on'))
    else:
        u['turbo'] = False
        u['price'] = 3
        bot.send_message(call.message.chat.id, get_text(uid, 'turbo_off'))
    u['step'] = 'photo'
    save_users()

@bot.message_handler(func=lambda m: m.text in ["🎬 Создать видео", "🎬 Create video", "🎬 Видео сохтан"])
def create(message):
    uid = message.from_user.id
    u = get_user(uid)
    used = u.get('free_used', False)
    if not used:
        bot.send_message(message.chat.id, get_text(uid, 'free_info'))
        u['turbo'] = False
        u['price'] = 0
        bot.send_message(message.chat.id, get_text(uid, 'send_photo'))
        u['step'] = 'photo'
        save_users()
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(get_text(uid, 'btn_turbo'), callback_data="turbo_yes"))
        markup.add(types.InlineKeyboardButton(get_text(uid, 'btn_normal'), callback_data="turbo_no"))
        bot.send_message(message.chat.id, get_text(uid, 'choose_speed'), reply_markup=markup)
        u['step'] = 'choose_turbo'
        save_users()

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    uid = message.from_user.id
    u = get_user(uid)
    u['photo'] = message.photo[-1].file_id
    u['step'] = 'text'
    save_users()
    bot.send_message(message.chat.id, get_text(uid, 'send_text'))

@bot.message_handler(func=lambda m: get_user(m.from_user.id).get('step') == 'text')
def get_text_msg(message):
    uid = message.from_user.id
    u = get_user(uid)
    text = message.text
    is_turbo = u.get('turbo', False)
    price = u.get('price', 3)
    is_free = not u.get('free_used')
    try:
        speed = "⚡ ТУРБО - СДЕЛАТЬ ПЕРВЫМ! +1$" if is_turbo else "🐢 Обычный"
        bot.send_message(ADMIN_ID, f"🔥 НОВЫЙ ЗАКАЗ!\nОт: @{message.from_user.username} ID:{uid}\nЯзык: {u.get('lang')}\nСкорость: {speed}\nЦена: {price}$\nТекст: {text}\nБесплатно: {is_free}")
        if u.get('photo'):
            bot.send_photo(ADMIN_ID, u['photo'])
    except:
        pass
    u['free_used'] = True
    u['step'] = None
    save_users()
    if is_turbo:
        bot.send_message(message.chat.id, get_text(uid, 'wait_turbo'))
    else:
        bot.send_message(message.chat.id, get_text(uid, 'wait'))

@bot.message_handler(func=lambda m: True)
def other(message):
    uid = message.from_user.id
    if message.text and ('Цены' in message.text or 'Prices' in message.text or 'Нарх' in message.text):
        bot.send_message(message.chat.id, get_text(uid, 'price'))
    else:
        bot.send_message(message.chat.id, get_text(uid, 'hello'))

print("Бот запущен! С ПАМЯТЬЮ + ТУРБО ⚡")
bot.polling(none_stop=True)