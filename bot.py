import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import Config
from database.db import init_db
from handlers import start, buy, payment, wallet, admin, referral
from services.ton_payment import check_ton_transaction

logging.basicConfig(level=logging.INFO)
