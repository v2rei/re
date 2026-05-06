from aiogram import Router, F
from aiogram.types import Message
from database.db import get_user
from config import Config

router = Router()

@router.message(F.text == "👥 زیرمجموعه‌گیری")
async def referral_menu(message: Message):
    user = await get_user(message.from_user.id)
    bot_username = (await message.bot.me()).username
    ref_link = f"https://t.me/{bot_username}?start=ref{message.from_user.id}"
    
    text = (
        "👥 <b>سیستم زیرمجموعه‌گیری AhuraVPN</b>\n\n"
        f"🔗 لینک اختصاصی شما:\n<code>{ref_link}</code>\n\n"
        f"💎 پاداش هر زیرمجموعه: <b>{Config.REFERRAL_BONUS} TON</b>\n"
        "🎁 با هر خرید زیرمجموعه‌هایتان، پاداش به کیف پول شما واریز می‌شود.\n\n"
        "📤 لینک خود را با دوستان به اشتراک بگذارید!"
    )
    await message.answer(text, parse_mode="HTML")
