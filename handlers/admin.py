from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy import select, func
from database.db import async_session
from database.models import User, Order, Transaction
from config import Config

router = Router()

def is_admin(user_id):
    return user_id in Config.ADMIN_IDS

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return
    
    async with async_session() as s:
        users_count = (await s.execute(select(func.count(User.id)))).scalar()
        orders_count = (await s.execute(select(func.count(Order.id)))).scalar()
        revenue = (await s.execute(select(func.sum(Order.price_ton)).where(Order.status == "paid"))).scalar() or 0
    
    text = (
        "🔐 <b>پنل مدیریت AhuraVPN</b>\n\n"
        f"👤 کل کاربران: <b>{users_count}</b>\n"
        f"📦 کل سفارش‌ها: <b>{orders_count}</b>\n"
        f"💰 درآمد کل: <b>{revenue} TON</b>\n\n"
        "دستورات ادمین:\n"
        "/broadcast - پیام همگانی\n"
        "/ban [user_id] - مسدود کردن\n"
        "/addbalance [user_id] [amount] - افزایش موجودی\n"
        "/stats - آمار کامل"
    )
    await message.answer(text, parse_mode="HTML")
