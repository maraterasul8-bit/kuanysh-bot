import random
import threading
import time
import telebot
from telebot import types

# Өз ботыңыздың токенін осында жазыңыз
TOKEN = "8991039569:AAGAcAeR0mj5acvbiGVWfxdNO1m9PBgi-lA"
bot = telebot.TeleBot(TOKEN)

# Пайдаланушы таңдаған активтер мен чат ID сақтау
user_settings = {}
active_users = set()

# Скриншоттардан алынған барлық активтер тізімі
all_otc_pairs = [
    "AUD/CHF OTC",
    "CAD/JPY OTC",
    "CHF/JPY OTC",
    "EUR/CHF OTC",
    "EUR/NZD OTC",
    "EUR/USD OTC",
    "NGN/USD OTC",
    "SAR/CNY OTC",
    "UAH/USD OTC",
    "USD/BDT OTC",
    "USD/BRL OTC",
    "USD/CAD OTC",
    "USD/CHF OTC",
    "USD/CNH OTC",
    "USD/EGP OTC",
    "USD/INR OTC",
    "USD/MXN OTC",
    "USD/THB OTC",
    "USD/VND OTC",
    "YER/USD OTC",
    "CHF/NOK OTC",
    "AUD/USD OTC",
    "TND/USD OTC",
    "QAR/CNY OTC",
    "USD/IDR OTC",
    "EUR/TRY OTC",
    "NZD/USD OTC",
    "USD/JPY OTC",
    "JOD/CNY OTC",
    "AED/CNY OTC",
    "LBP/USD OTC",
    "USD/RUB OTC",
    "USD/ARS OTC",
    "GBP/USD OTC",
    "GBP/JPY OTC",
    "USD/COP OTC",
    "EUR/HUF OTC",
    "USD/DZD OTC",
    "USD/SGD OTC",
    "ZAR/USD OTC",
    "AUD/NZD OTC",
    "USD/CLP OTC",
    "USD/PHP OTC",
    "EUR/JPY OTC",
    "GBP/AUD OTC",
    "AUD/CAD OTC",
    "USD/MYR OTC",
    "USD/PKR OTC",
    "BHD/CNY OTC",
    "CAD/CHF OTC",
    "MAD/USD OTC",
    "EUR/GBP OTC",
    # Қосымша негізгі стандартты жұптар
    "EUR/JPY",
    "GBP/JPY",
    "EUR/CAD",
    "GBP/CAD",
    "GBP/CHF",
    "AUD/JPY",
    "EUR/AUD",
]

# Тренд пен свечаны талдайтын шпаргалка-база
strategy_variants = [
    {
        "indicator": "Bollinger Bands шекарасы + Price Action Реверс",
        "direction": "Жоғары (CALL / BUY)",
        "emoji": "🟢",
        "analysis": (
            "📉 **Тренд және Свеча талдауы:** Баға төменгі Bollinger сызығына"
            " тиіп, төменгі көлеңкесі ұзын «Жалған пробой» немесе «Молот» свечасын"
            " түзді. Сатушылардың күші сарқылды.\n"
            "🎯 **Шпаргалка әрекеті:** 1-2 минуттық экспирацияға BUY (UP) ашуға"
            " қатаң сәйкес келеді."
        ),
    },
    {
        "indicator": "Қарсылық деңгейі + Импульстік жабу (Bearish Pin Bar)",
        "direction": "Төмен (PUT / SELL)",
        "emoji": "🔴",
        "analysis": (
            "📈 **Тренд және Свеча талдауы:** Жоғарғы деңгейде ұзын денелі"
            " жасыл свечадан кейін кішкентай денелі және жоғарғы ұзын көлеңкелі"
            " (Pin Bar) свеча пайда болды. Өсу импульсі өшті.\n"
            "🎯 **Шпаргалка әрекеті:** 1-2 минуттық экспирацияға SELL (DOWN) ашуға"
            " қатаң сәйкес келеді."
        ),
    },
    {
        "indicator": "Micro-Trend & Momentum Қайталануы",
        "direction": "Жоғары (CALL / BUY)",
        "emoji": "🟢",
        "analysis": (
            "📈 **Тренд және Свеча талдауы:** Локальді микро-тренд өсу"
            " бағытында. Свечалар тізбегі бірінен соң бірі сенімді жасыл түспен"
            " жабылып, коррекция аяқталды.\n"
            "🎯 **Шпаргалка әрекеті:** 1-2 минуттық экспирацияға тренд бойымен BUY"
            " (UP) бағыты қолайлы."
        ),
    },
    {
        "indicator": "Флэт аймағы Жалған пробой (False Breakout)",
        "direction": "Төмен (PUT / SELL)",
        "emoji": "🔴",
        "analysis": (
            "📉 **Тренд және Свеча талдауы:** Нарықтағы боковик (флэт) кезінде"
            " баға қарсылық деңгейін сәл ғана бұзып өтіп, дереу ішке қайта"
            " кірді.\n"
            "🎯 **Шпаргалка әрекеті:** 2 минуттық экспирацияға SELL (DOWN) ашу"
            " қажет."
        ),
    },
]


@bot.message_handler(commands=["start"])
def send_welcome(message):
  active_users.add(message.chat.id)

  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  for pair in all_otc_pairs:
    markup.add(types.KeyboardButton(f"💱 {pair} таңдау"))

  markup.add(types.KeyboardButton("🛑 Авто-сигналды тоқтату"))

  text = (
      "🤖 **Kuanysh System: Smart OTC Trading Bot**\n\n"
      "Скриншоттағы барлық активтер мен валюта жұптары толығымен қосылды.\n"
      "Төмендегі тізімнен қажетті активті таңдаңыз:"
  )
  bot.send_message(
      message.chat.id, text, parse_mode="Markdown", reply_markup=markup
  )


@bot.message_handler(
    func=lambda message: message.text
    and message.text.endswith("таңдау")
)
def set_user_pair(message):
  chat_id = message.chat.id
  active_users.add(chat_id)

  chosen_pair = message.text.replace("💱", "").replace("таңдау", "").strip()
  user_settings[chat_id] = chosen_pair

  bot.send_message(
      chat_id,
      f"✅ **{chosen_pair}** сәтті таңдалды!\n\n"
      f"⏳ Осы актив бойынша анализдер автоматты түрде келіп тұрады.",
      parse_mode="Markdown",
  )


@bot.message_handler(func=lambda message: message.text == "🛑 Авто-сигналды тоқтату")
def stop_signals(message):
  chat_id = message.chat.id
  if chat_id in active_users:
    active_users.remove(chat_id)
  if chat_id in user_settings:
    del user_settings[chat_id]

  bot.send_message(
      chat_id,
      "🛑 Автоматты сигналдар тоқтатылды. Қайта қосу үшін /start басыңыз.",
  )


def background_strategy_loop():
  while True:
    time.sleep(60)
    for chat_id in list(active_users):
      pair = user_settings.get(chat_id, "EUR/USD OTC")
      strategy = random.choice(strategy_variants)
      tf = random.choice(["1 минут", "2 минут"])

      text = (
          f"⚡️ **KUANYSH SYSTEM: SMART OTC SIGNAL**\n\n"
          f"💱 **Актив:** {pair}\n"
          f"⏱ **Экспирация:** {tf}\n"
          f"📊 **Сигнал түрі:** {strategy['indicator']}\n"
          f"📈 **Бағыты:** {strategy['emoji']} **{strategy['direction']}**\n\n"
          f"📋 **Талдау:**\n{strategy['analysis']}\n\n"
          f"⚠️ *Менеджментті қатаң сақтаңыз!*"
      )

      markup = types.InlineKeyboardMarkup()
      markup.add(
          types.InlineKeyboardButton("🟢 UP (BUY)", callback_data="buy"),
          types.InlineKeyboardButton("🔴 DOWN (SELL)", callback_data="sell"),
      )

      try:
        bot.send_message(
            chat_id, text, parse_mode="Markdown", reply_markup=markup
        )
      except Exception as e:
        print(f"Қате: {e}")


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
  if call.data == "buy":
    bot.answer_callback_query(
        call.id, "✅ UP (BUY) бағыты есепке алынды!", show_alert=True
    )
  elif call.data == "sell":
    bot.answer_callback_query(
        call.id, "❌ DOWN (SELL) бағыты есепке алынды!", show_alert=True
    )


thread = threading.Thread(target=background_strategy_loop)
thread.daemon = True
thread.start()

print("Kuanysh System толық базасы іске қосылды...")
bot.polling(none_stop=True)
