from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from database.models import Base, User, Order, Transaction
from config import Config

engine = create_async_engine(Config.DB_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_or_create_user(tg_id, username=None, full_name=None, referrer_id=None):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()
        if not user:
            user = User(tg_id=tg_id, username=username, full_name=full_name, referrer_id=referrer_id)
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user

async def get_user(tg_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        return result.scalar_one_or_none()

async def update_balance(tg_id, amount):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()
        if user:
            user.balance += amount
            await session.commit()
        return user

async def create_order(user_id, protocol, volume_gb, price_ton):
    async with async_session() as session:
        order = Order(
            user_id=user_id,
            protocol=protocol,
            volume_gb=volume_gb,
            price_ton=price_ton
        )
        session.add(order)
        await session.commit()
        await session.refresh(order)
        return order
