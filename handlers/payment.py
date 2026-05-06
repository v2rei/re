from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.db import get_user, create_order, update_balance
from services.panel_api import create_vpn_user
from services.ton_payment import generate_payment_link
from config import Config
import qrcode
import io
from aiogram.types import BufferedInputFile

router = Router()

@router.callback_query(F.data.startswith("pay:wallet:"))
async def pay_with_wallet(call: CallbackQuery):
    _, _, protocol, gb = call.data.split(":")
    gb = int(gb)
    price = gb * Config.PRICE_PER_GB
    
    user = await get_user(call.from_user.id)
    if user.balance < price:
        await call.answer("❌ موجودی کیف پول کافی نیست!", show_alert=True)
        return
    
    await update_balance(call.from_user.id, -price)
    order = await create_order(user.id, protocol, gb, price)
    
    config_link = await create_vpn_user(
        username=f"ahura_{user.tg_id}_{order.id}",
        protocol=protocol,
        volume_gb=gb
    )
    
    text = (
        "✅ <b>پرداخت موفق!</b>\n\n"
        f"📡 پروتکل: {Config.PROTOCOLS[protocol]}\n"
        f"📦 حجم: {gb}GB\n"
        f"⏱ اعتبار: ۳۰ روز\n\n"
        f"🔗 <b>کانفیگ شما:</b>\n<code>{config_link}</code>\n\n"
        "📚 برای آموزش اتصال به منوی «آموزش اتصال» مراجعه کنید."
    )
    await call.message.edit_text(text, parse_mode="HTML")

@router.callback_query(F.data.startswith("pay:ton:"))
async def pay_with_ton(call: CallbackQuery):
    _, _, protocol, gb = call.data.split(":")
    gb = int(gb)
    price = gb * Config.PRICE_PER_GB
    
    user = await get_user(call.from_user.id)
    order = await create_order(user.id, protocol, gb, price)
    
    payment_link, comment = generate_payment_link(price, order.id)
    
    # Generate QR Code
    qr = qrcode.make(payment_link)
    bio = io.BytesIO()
    qr.save(bio, format="PNG")
    bio.seek(0)
    
    text = (
        "💎 <b>پرداخت با TON Coin</b>\n\n"
        f"💰 مبلغ: <b>{price} TON</b>\n"
        f"📬 آدرس: <code>{Config.TON_WALLET}</code>\n"
        f"📝 کامنت (الزامی): <code>{comment}</code>\n\n"
        "⚠️ حتماً کامنت را وارد کنید!\n"
        "✅ بعد از تایید تراکنش، کانفیگ به‌صورت خودکار ارسال می‌شود."
    )
    
    await call.message.answer_photo(
        BufferedInputFile(bio.getvalue(), filename="qr.png"),
        caption=text,
        parse_mode="HTML"
  )
