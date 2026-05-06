from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, CommandObject
from database.db import get_or_create_user
from keyboards.user_kb import main_menu

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
    referrer_id = None
    if command.args and command.args.startswith("ref"):
        try:
            referrer_id = int(command.args.replace("ref", ""))
        except:
            pass
    
    user = await get_or_create_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
        referrer_id=referrer_id
    )
    
    text = (
        "🌟 <b>به ربات AhuraVPN خوش آمدید!</b>\n\n"
        "🚀 سریع‌ترین و امن‌ترین کانفیگ‌های VPN\n"
        "💎 پرداخت با تون‌کوین (TON)\n"
        "🔥 پشتیبانی از تمام پروتکل‌های مدرن\n\n"
        "📌 از منوی پایین گزینه مورد نظر را انتخاب کنید:"
    )
    await message.answer(text, reply_markup=main_menu(), parse_mode="HTML")
