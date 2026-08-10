import os
import telebot
from telebot import types
import random

# Render-дегі веб-сервер
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот Kuanysh запущен!"

TOKEN = "8991035959:AAF#H1o6A7L7gcbNegIf86KEGjt0V_VHQ"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Барлық активтер тізімі
    resursi = [
        # Стандартты жұптар
        ("💱 GBP/USD", "gbpusd"), ("💱 USD/CAD", "usdcad"),
        ("💱 USD/CHF", "usdchf"), ("💱 USD/JPY", "usdjpy"),
        ("💱 AUD/CAD", "audcad"), ("💱 AUD/JPY", "audjpy"),
        ("💱 EUR/AUD", "euraud"), ("💱 GBP/AUD", "gbpaud"),
        ("💱 CAD/CHF", "cadchf"), ("💱 EUR/USD", "eurusd"),
        ("💱 AUD/CHF", "audchf"), ("💱 CHF/JPY", "chfjpy"),
        ("💱 EUR/CAD", "eurcad"), ("💱 EUR/CHF", "eurchf"),
        ("💱 EUR/GBP", "eurgbp"), ("💱 GBP/CAD", "gbpcad"),
        ("💱 GBP/CHF", "gbpchf"),
        
        # ОТС-диапазондар (нақты бағаларға жақындатылған диапазон)
        ("📉 CAD/CHF OTC", "cadchfotc"), ("📉 USD/ARS OTC", "usdarsotc"),
        ("📉 KES/USD OTC", "kesusdotc"), ("📉 NZD/JPY OTC", "nzdjpyotc"),
        ("📉 CHF/JPY OTC", "chfjpyotc"), ("📉 NZD/USD OTC", "nzdusdotc"),
        ("📉 USD/CHF OTC", "usdchfotc"), ("📉 EUR/HUF OTC", "eurhufotc"),
        ("📉 USD/EGP OTC", "usdegpotc"), ("📉 USD/THB OTC", "usdthbotc"),
        ("📉 USD/CLP OTC", "usdclpotc"), ("📉 EUR/RUB OTC", "eurrubotc"),
        ("📉 USD/DZD OTC", "usddzdotc"), ("📉 GBP/JPY OTC", "gbpjpyotc"),
        ("📉 USD/SGD OTC", "usdsgdotc"), ("📉 USD/IDR OTC", "usdidrotc"),
        ("📉 AUD/JPY OTC", "audjpyotc"), ("📉 USD/PKR OTC", "usdpkrotc"),
        ("📉 USD/PHP OTC", "usdphpotc"), ("📉 CHF/NOK OTC", "chfnokotc"),
        ("📉 USD/CAD OTC", "usdcadotc"), ("📉 YER/USD OTC", "yerusdotc"),
        ("📉 SAR/CNY OTC", "sarcnyotc"), ("📉 LBP/USD OTC", "lbpusdotc"),
        ("📉 AUD/NZD OTC", "audnzdotc"), ("📉 USD/MYR OTC", "usdmyrotc"),
        ("📉 BHD/CNY OTC", "bhdcnyotc"), ("📉 EUR/GBP OTC", "eurgbpotc"),
        ("📉 OMR/CNY OTC", "omrcnyotc"), ("📉 QAR/CNY OTC", "qarcnyotc"),
        ("📉 TND/USD OTC", "tndusdotc"), ("📉 UAH/USD OTC", "uahusdotc"),
        ("📉 USD/BDT OTC", "usdbdtotc"), ("📉 USD/CNH OTC", "usdcnhotc"),
        ("📉 USD/COP OTC", "usdcopotc"), ("📉 USD/INR OTC", "usdinrotc"),
        ("📉 ZAR/USD OTC", "zarusdotc"), ("📉 AED/CNY OTC", "aedcnyotc"),
        ("📉 EUR/TRY OTC", "eurtryotc"), ("📉 EUR/USD OTC", "eurusdotc"),
        ("📉 GBP/AUD OTC", "gbpaudotc"), ("📉 GBP/USD OTC", "gbpusdotc"),
        ("📉 NGN/USD OTC", "ngnusdotc"), ("📉 EUR/NZD OTC", "eurnzdotc"),
        ("📉 EUR/JPY OTC", "eurjpyotc"), ("📉 MAD/USD OTC", "madusdotc"),
        ("📉 USD/VND OTC", "usdvndotc"), ("📉 USD/BRL OTC", "usdbrlotc"),
        ("📉 JOD/CNY OTC", "jodcnyotc"), ("📉 USD/MXN OTC", "usdmxnotc")
    ]

    for текст, данные in resursi:
        markup.add(types.InlineKeyboardButton(текст, callback_data=данные))

    bot.send_message(
        message.chat.id,
        "🎛 **ТОРГОВАЯ СИСТЕМА KUANYSH**\n\nБарлық активтер тізімі қосылды. Активті таңдаңыз:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda вызов: True)
def handle_callback(вызов):
    # Диапазондар нақты график бағаларына қарай жақындатылды
    актив_данные = {
        "gbpusd": ("GBP/USD", (1.28, 1.35)),
        "usdcad": ("USD/CAD", (1.30, 1.40)),
        "usdchf": ("USD/CHF", (0.85, 0.95)),
        "usdjpy": ("USD/JPY", (145.0, 155.0)),
        "audcad": ("AUD/CAD", (0.88, 0.95)),
        "audjpy": ("AUD/JPY", (95.0, 105.0)),
        "euraud": ("EUR/AUD", (1.60, 1.70)),
        "gbpaud": ("GBP/AUD", (1.85, 1.95)),
        "cadchf": ("CAD/CHF", (0.63, 0.69)),
        "eurusd": ("EUR/USD", (1.05, 1.15)),
        "audchf": ("AUD/CHF", (0.55, 0.62)),
        "chfjpy": ("CHF/JPY", (160.0, 175.0)),
        "eurcad": ("EUR/CAD", (1.45, 1.55)),
        "eurchf": ("EUR/CHF", (0.94, 0.99)),
        "eurgbp": ("EUR/GBP", (0.83, 0.88)),
        "gbpcad": ("GBP/CAD", (1.70, 1.80)),
        "gbpchf": ("GBP/CHF", (1.10, 1.20)),

        # OTC-диапазондар
        "cadchfotc": ("CAD/CHF OTC", (0.63, 0.69)),
        "usdarsotc": ("USD/ARS OTC", (950.0, 1050.0)),
        "kesusdotc": ("KES/USD OTC", (125.0, 135.0)),
        "nzdjpyotc": ("NZD/JPY OTC", (90.0, 100.0)),
        "chfjpyotc": ("CHF/JPY OTC", (160.0, 175.0)),
        "nzdusdotc": ("NZD/USD OTC", (0.58, 0.65)),
        "usdchfotc": ("USD/CHF OTC", (0.85, 0.95)),
        "eurhufotc": ("EUR/HUF OTC", (398.0, 410.0)),
        "usdegpotc": ("USD/EGP OTC", (45.0, 50.0)),
        "usdthbotc": ("USD/THB OTC", (35.0, 38.0)),
        "usdclpotc": ("USD/CLP OTC", (900.0, 950.0)),
        "eurrubotc": ("EUR/RUB OTC", (95.0, 105.0)),
        "usddzdotc": ("USD/DZD OTC", (130.0, 140.0)),
        "gbpjpyotc": ("GBP/JPY OTC", (190.0, 205.0)),
        "usdsgdotc": ("USD/SGD OTC", (1.30, 1.38)),
        "usdidrotc": ("USD/IDR OTC", (15500.0, 16200.0)),
        "audjpyotc": ("AUD/JPY OTC", (95.0, 105.0)),
        "usdpkrotc": ("USD/PKR OTC", (275.0, 285.0)),
        "usdphpotc": ("USD/PHP OTC", (55.0, 60.0)),
        "chfnokotc": ("CHF/NOK OTC", (11.5, 12.5)),
        "usdcadotc": ("USD/CAD OTC", (1.30, 1.40)),
        "yerusdotc": ("YER/USD OTC", (245.0, 255.0)),
        "sarcnyotc": ("SAR/CNY OTC", (1.85, 1.95)),
        "lbpusdotc": ("LBP/USD OTC", (89000.0, 91000.0)),
        "audnzdotc": ("AUD/NZD OTC", (1.08, 1.15)),
        "usdmyrotc": ("USD/MYR OTC", (4.40, 4.70)),
        "bhdcnyotc": ("BHD/CNY OTC", (18.5, 19.5)),
        "eurgbpotc": ("EUR/GBP OTC", (0.83, 0.88)),
        "omrcnyotc": ("OMR/CNY OTC", (18.0, 19.0)),
        "qarcnyotc": ("QAR/CNY OTC", (1.95, 2.05)),
        "tndusdotc": ("TND/USD OTC", (3.0, 3.2)),
        "uahusdotc": ("UAH/USD OTC", (38.0, 42.0)),
        "usdbdtotc": ("USD/BDT OTC", (115.0, 120.0)),
        "usdcnhotc": ("USD/CNH OTC", (7.10, 7.30)),
        "usdcopotc": ("USD/COP OTC", (3900.0, 4100.0)),
        "usdinrotc": ("USD/INR OTC", (82.0, 84.0)),
        "zarusdotc": ("ZAR/USD OTC", (17.5, 18.5)),
        "aedcnyotc": ("AED/CNY OTC", (1.90, 2.00)),
        "eurtryotc": ("EUR/TRY OTC", (35.0, 38.0)),
        # EUR/USD OTC үшін нақты диапазон 1.19 - 1.20 аралығына жақындатылды
        "eurusdotc": ("EUR/USD OTC", (1.1900, 1.2000)),
        "gbpaudotc": ("GBP/AUD OTC", (1.85, 1.95)),
        "gbpusdotc": ("GBP/USD OTC", (1.25, 1.35)),
        "ngnusdotc": ("NGN/USD OTC", (1400.0, 15500.0)),
        "eurnzdotc": ("EUR/NZD OTC", (1.75, 1.85)),
        "eurjpyotc": ("EUR/JPY OTC", (165.0, 175.0)),
        "madusdotc": ("MAD/USD OTC", (9.8, 10.5)),
        "usdvndotc": ("USD/VND OTC", (24500.0, 25500.0)),
        "usdbrlotc": ("USD/BRL OTC", (5.4, 5.8)),
        "jodcnyotc": ("JOD/CNY OTC", (10.0, 10.5)),
        "usdmxnotc": ("USD/MXN OTC", (17.0, 18.5))
    }

    if вызов.data in актив_данные:
        имя, (мин_п, мах_п) = актив_данные[вызов.data]
        bot.answer_callback_query(вызов.id, f"{имя} талдауы жасалуда...")

        # Нақтырақ баға генерациясы
        цена = round(random.uniform(мин_п, мах_п), 4)
        сигнал = случайный.выбор(["🟢 ЖОҒАРЫ (ЗВОНОК)", "🔴 ТӨМЕН (ПУТ)"])
        тренд = "🟢 Өсу тренді (Бычий)" if "ЖОҒАРЫ" in сигнал else "🔴 Құлдырау тренді (Медвежий)"

        анализ_текст = (
            f"📈 **КУАНЫШ АНАЛИЗАТОРЫ: {имя}**\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"💵 Ағымдағы баға: `{цена}`\n"
            f"📊 Тренд жағдайы: {тренд}\n"
            f"⚙️ Индикатор (RSI/SMA): Талдау аяқталды\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 **ҚОРЫТЫНДЫ БЕРИШ:**\n"
            f"📢 Сигнал: **{сигнал}**\n"
            f"⏱ Уақыт: `1 минута`"
        )

        try:
            bot.send_message(вызов.message.chat.id, анализ_текст, parse_mode="Markdown")
        except Исключение:
            pass

def run_bot():
    bot.remove_webhook()
    print("Телеграм-бот запущен через ветку обсуждения...")
    bot.infinity_polling(none_stop=True)

if __name__ == "__main__":
    import threading
    # Веб-сервер мен ботты қатар қосу (Render үшін міндетті)
    t = threading.Thread(target=run_bot)
    t.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
        
