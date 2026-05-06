import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram
    BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
    ADMIN_IDS = [int(x) for x in os.getenv("ADMINS", "123456789").split(",")]
    
    # TON Wallet
    TON_WALLET = os.getenv("TON_WALLET", "UQxxxxxxxxxxxxxxxxxxxxxx")
    TON_API_KEY = os.getenv("TON_API_KEY", "")
    TON_NETWORK = "mainnet"  # یا testnet
    
    # Pricing
    PRICE_PER_GB = 0.5  # TON
    
    # Panel (3x-ui / Marzban)
    PANEL_URL = os.getenv("PANEL_URL", "https://panel.example.com")
    PANEL_USERNAME = os.getenv("PANEL_USER", "admin")
    PANEL_PASSWORD = os.getenv("PANEL_PASS", "admin")
    PANEL_TYPE = "marzban"  # marzban | 3x-ui
    
    # Database
    DB_URL = "sqlite+aiosqlite:///data/ahuravpn.db"
    
    # Referral
    REFERRAL_BONUS = 0.1  # TON
    
    # Packages (GB)
    PACKAGES = list(range(1, 11))  # 1 تا 10 گیگ
    
    # Available Protocols
    PROTOCOLS = {
        "vless": "🚀 VLESS (Reality/XTLS)",
        "vmess": "⚡ VMess (WS/TLS)",
        "trojan": "🛡 Trojan",
        "shadowsocks": "🌀 Shadowsocks",
        "hysteria2": "🔥 Hysteria2",
        "tuic": "💎 TUIC v5",
        "wireguard": "🔒 WireGuard",
        "openvpn": "🛰 OpenVPN"
    }
