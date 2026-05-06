import aiohttp
import uuid
from config import Config

class MarzbanAPI:
    def __init__(self):
        self.base_url = Config.PANEL_URL
        self.token = None
    
    async def login(self):
        async with aiohttp.ClientSession() as s:
            async with s.post(
                f"{self.base_url}/api/admin/token",
                data={"username": Config.PANEL_USERNAME, "password": Config.PANEL_PASSWORD}
            ) as r:
                data = await r.json()
                self.token = data.get("access_token")
    
    async def create_user(self, username: str, protocol: str, volume_gb: int, days: int = 30):
        if not self.token:
            await self.login()
        
        headers = {"Authorization": f"Bearer {self.token}"}
        proxies = {protocol: {}}
        
        payload = {
            "username": username,
            "proxies": proxies,
            "inbounds": {protocol: []},
            "data_limit": volume_gb * 1024 * 1024 * 1024,
            "expire": int((__import__("time").time() + days * 86400)),
            "status": "active"
        }
        
        async with aiohttp.ClientSession() as s:
            async with s.post(f"{self.base_url}/api/user", json=payload, headers=headers) as r:
                data = await r.json()
                return data.get("subscription_url")

panel = MarzbanAPI()

async def create_vpn_user(username: str, protocol: str, volume_gb: int):
    try:
        link = await panel.create_user(username, protocol, volume_gb)
        return link or f"vless://demo-{uuid.uuid4()}@server.com:443"
    except Exception as e:
        return f"⚠️ خطا در ساخت کانفیگ: {e}"
