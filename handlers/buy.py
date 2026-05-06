from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.user_kb import protocols_kb, packages_kb, confirm_purchase_kb
from config import Config

router = Router()

PROTOCOL_DESCRIPTIONS = {
    "vless": (
        "🚀 <b>VLESS (XTLS-Reality)</b>\n\n"
        "▫️ نسل جدید پروتکل V2Ray\n"
        "▫️ پشتیبانی از Reality (دور زدن DPI پیشرفته)\n"
        "▫️ سرعت فوق‌العاده بالا\n"
        "▫️ مصرف CPU کم\n"
        "▫️ مناسب: ایران، چین، روسیه\n"
        "✅ پیشنهاد می‌شود برای کاربران حرفه‌ای"
    ),
    "vmess": (
        "⚡ <b>VMess (WebSocket + TLS)</b>\n\n"
        "▫️ پروتکل کلاسیک و پایدار V2Ray\n"
        "▫️ پشتیبانی از CDN (Cloudflare)\n"
        "▫️ مخفی‌سازی ترافیک\n"
        "▫️ مناسب موبایل و دسکتاپ"
    ),
    "trojan": (
        "🛡 <b>Trojan-GFW</b>\n\n"
        "▫️ شبیه‌سازی کامل HTTPS\n"
        "▫️ تشخیص ناپذیر در برابر فیلترینگ\n"
        "▫️ سرعت بالا و پایداری عالی\n"
        "▫️ مناسب کاربران حرفه‌ای"
    ),
    "shadowsocks": (
        "🌀 <b>Shadowsocks (2022)</b>\n\n"
        "▫️ سبک، سریع و ساده\n"
        "▫️ رمزنگاری AEAD مدرن\n"
        "▫️ مصرف باتری پایین در موبایل\n"
        "▫️ مناسب اتصال‌های روزمره"
    ),
    "hysteria2": (
        "🔥 <b>Hysteria2 (QUIC-based)</b>\n\n"
        "▫️ مبتنی بر QUIC و UDP\n"
        "▫️ سرعت دانلود بسیار بالا\n"
        "▫️ مناسب شبکه‌های ضعیف و ناپایدار\n"
        "▫️ Brutal Congestion Control"
    ),
    "tuic": (
        "💎 <b>TUIC v5</b>\n\n"
        "▫️ پروتکل مدرن مبتنی بر QUIC\n"
        "▫️ Latency بسیار کم\n"
        "▫️ ایده‌آل برای گیمینگ و تماس صوتی\n"
        "▫️ پایداری در شبکه موبایل"
    ),
    "wireguard": (
        "🔒 <b>WireGuard</b>\n\n"
        "▫️ سریع‌ترین پروتکل VPN جهان\n"
        "▫️ کد بسیار سبک و امن\n"
        "▫️ مصرف باتری پایین\n"
        "▫️ مناسب همه پلتفرم‌ها"
    ),
    "openvpn": (
        "🛰 <b>OpenVPN</b>\n\n"
        "▫️ پروتکل کلاسیک و قابل اعتماد\n"
        "▫️ پشتیبانی همگانی\n"
        "▫️ امنیت بالا\n"
        "▫️ مناسب سازمان‌ها"
    ),
}

@router.message(F.text == "🛒 خرید کانفیگ")
async def buy_menu(message: Message):
    text = (
        "🛍 <b>فروشگاه کانفیگ AhuraVPN</b>\n\n"
        "لطفاً پروتکل مورد نظر خود را انتخاب کنید:\n"
        f"💰 قیمت هر گیگابایت: <b>{Config.PRICE_PER_GB} TON</b>"
    )
    await message.answer(text, reply_markup=protocols_kb(), parse_mode="HTML")

@router.callback_query(F.data.startswith("proto:"))
async def select_protocol(call: CallbackQuery):
    protocol = call.data.split(":")[1]
    desc = PROTOCOL_DESCRIPTIONS.get(protocol, "")
    text = f"{desc}\n\n📦 لطفاً حجم پک خود را انتخاب کنید:"
    await call.message.edit_text(text, reply_markup=packages_kb(protocol), parse_mode="HTML")

@router.callback_query(F.data.startswith("pkg:"))
async def select_package(call: CallbackQuery):
    _, protocol, gb = call.data.split(":")
    gb = int(gb)
    price = gb * Config.PRICE_PER_GB
    
    text = (
        f"🧾 <b>صورتحساب خرید</b>\n\n"
        f"📡 پروتکل: <b>{Config.PROTOCOLS[protocol]}</b>\n"
        f"📦 حجم: <b>{gb} GB</b>\n"
        f"💰 قیمت: <b>{price} TON</b>\n"
        f"⏱ مدت اعتبار: <b>۳۰ روز</b>\n\n"
        f"روش پرداخت را انتخاب کنید:"
    )
    await call.message.edit_text(text, reply_markup=confirm_purchase_kb(protocol, gb), parse_mode="HTML")

@router.callback_query(F.data == "back:protocols")
async def back_to_protocols(call: CallbackQuery):
    await call.message.edit_text("📡 پروتکل را انتخاب کنید:", reply_markup=protocols_kb())

@router.callback_query(F.data == "back:main")
async def back_to_main(call: CallbackQuery):
    await call.message.delete()
