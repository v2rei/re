from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import Config

def main_menu():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛒 خرید کانفیگ"), KeyboardButton(text="💳 کیف پول")],
            [KeyboardButton(text="📦 سرویس‌های من"), KeyboardButton(text="👥 زیرمجموعه‌گیری")],
            [KeyboardButton(text="📚 آموزش اتصال"), KeyboardButton(text="💬 پشتیبانی")],
            [KeyboardButton(text="ℹ️ درباره ما")]
        ],
        resize_keyboard=True
    )
    return kb

def protocols_kb():
    buttons = []
    row = []
    for key, name in Config.PROTOCOLS.items():
        row.append(InlineKeyboardButton(text=name, callback_data=f"proto:{key}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="🔙 بازگشت", callback_data="back:main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def packages_kb(protocol: str):
    buttons = []
    row = []
    for gb in Config.PACKAGES:
        price = gb * Config.PRICE_PER_GB
        row.append(InlineKeyboardButton(
            text=f"{gb}GB | {price} TON",
            callback_data=f"pkg:{protocol}:{gb}"
        ))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton(text="🔙 بازگشت", callback_data="back:protocols")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def confirm_purchase_kb(protocol: str, gb: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ تایید و پرداخت از کیف پول", callback_data=f"pay:wallet:{protocol}:{gb}")],
        [InlineKeyboardButton(text="💎 پرداخت مستقیم با TON", callback_data=f"pay:ton:{protocol}:{gb}")],
        [InlineKeyboardButton(text="❌ انصراف", callback_data="back:main")]
    ])

def wallet_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ شارژ کیف پول", callback_data="wallet:deposit")],
        [InlineKeyboardButton(text="📜 تاریخچه تراکنش‌ها", callback_data="wallet:history")],
        [InlineKeyboardButton(text="🔙 بازگشت", callback_data="back:main")]
    ])
