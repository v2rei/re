import aiohttp
from config import Config
import hashlib
import time

def generate_payment_link(amount: float, order_id: int):
    """ساخت لینک پرداخت TON با کامنت یکتا"""
    comment = f"AHURA{order_id}{int(time.time())%10000}"
    nano_amount = int(amount * 1_000_000_000)
    link = f"ton://transfer/{Config.TON_WALLET}?amount={nano_amount}&text={comment}"
    return link, comment

async def check_ton_transaction(comment: str, expected_amount: float):
    """بررسی تراکنش‌های ورودی به کیف پول TON"""
    url = f"https://toncenter.com/api/v2/getTransactions"
    params = {
        "address": Config.TON_WALLET,
        "limit": 50,
        "api_key": Config.TON_API_KEY
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()
            for tx in data.get("result", []):
                msg = tx.get("in_msg", {})
                tx_comment = msg.get("message", "")
                value = int(msg.get("value", 0)) / 1_000_000_000
                if comment in tx_comment and value >= expected_amount:
                    return True, tx.get("transaction_id", {}).get("hash")
    return False, None
