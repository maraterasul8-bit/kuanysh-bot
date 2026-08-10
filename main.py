import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "СІЗДІҢ_БОТ_ТОКЕНІҢІЗ"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Тек OTC активтері қалдырылған тізім
otc_assets = [
    ("EUR/USD OTC", "eurusd_otc"),
    ("AUD/CAD OTC", "audcad_otc"),
    ("AUD/CHF OTC", "audchf_otc"),
    ("UAH/USD OTC", "uahusd_otc"),
    ("USD/RUB OTC", "usdrub_otc"),
    ("USD/PKR OTC", "usdpkr_otc"),
    ("GBP/USD OTC", "gbpusd_otc"),
    ("EUR/JPY OTC", "eurjpy_otc"),
    ("USD/IDR OTC", "usdidr_otc"),
    ("USD/MXN OTC", "usdmxn_otc"),
    ("USD/JPY OTC", "usdjpy_otc"),
    ("USD/CNH OTC", "usdcnh_otc"),
    ("BHD/CNY OTC", "bhdcny_otc"),
    ("USD/CLP OTC", "usdclp_otc"),
    ("USD/PHP OTC", "usdphp_otc"),
    ("CAD/JPY OTC", "cadjpy_otc"),
    ("OMR/CNY OTC", "omrcny_otc"),
    ("USD/SGD OTC", "usdsgd_otc"),
    ("EUR/CHF OTC", "eurchf_otc"),
    ("EUR/NZD OTC", "eurnzd_otc"),
    ("EUR/TRY OTC", "eurtry_otc"),
    ("LBP/USD OTC", "lbpusd_otc"),
    ("SAR/CNY OTC", "sarcny_otc"),
    ("QAR/CNY OTC", "qarcny_otc"),
    ("USD/COP OTC", "usdcop_otc"),
    ("USD/MYR OTC", "usdmyr_otc"),
    ("USD/VND OTC", "usdvnd_otc"),
    ("YER/USD OTC", "yerusd_otc"),
    ("TND/USD OTC", "tndusd_otc")
]

def get_paginated_keyboard():
    keyboard_buttons = []
    for i in range(0, len(otc_assets), 2):
        row = [InlineKeyboardButton(text=otc_assets[i][0], callback_data=otc_assets[i][1])]
        if i + 1 < len(otc_assets):
            row.append(InlineKeyboardButton(text=otc_assets[i+1][0], callback_data=otc_assets[i+1][1]))
        keyboard_buttons.append(row)
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📊 OTC Анализ алу"), types.KeyboardButton(text="ℹ️ Нұсқаулық")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Сәлем! Бұл тек **OTC** активтеріне арналған сигнал боты.\n"
        "Төмендегі батырманы басып, OTC жұбын таңдаңыз:",
        reply_markup=keyboard
    )

@dp.message(lambda message: message.text == "📊 OTC Анализ алу")
async def choose_otc_asset(message: Message):
    await message.answer(
        "Төмендегі тізімнен анализ жасау үшін OTC активін таңдаңыз:",
        reply_markup=get_paginated_keyboard()
    )

@dp.callback_query(lambda query: any(query.data == asset[1] for asset in otc_assets))
async def process_otc_analysis(callback: types.CallbackQuery):
    selected_asset = next(asset[0] for asset in otc_assets if asset[1] == callback.data)
    
    analysis_result = (
        f"🔍 **OTC Нарық анализі ({selected_asset}):**\n"
        "📈 Волатильность: Жоғары\n"
        "⏱ Уақыт: 1 минут (M1)\n"
        "⚡️ Қорытынды шешім: **ПОКУПКА (ЖОҒАРЫ) 🟢**"
    )
    
    await callback.message.answer(analysis_result, parse_mode="Markdown")
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
