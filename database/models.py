from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    balance = Column(Float, default=0.0)
    referrer_id = Column(Integer, nullable=True)
    is_banned = Column(Boolean, default=False)
    language = Column(String, default="fa")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    protocol = Column(String)
    volume_gb = Column(Integer)
    price_ton = Column(Float)
    config_link = Column(Text, nullable=True)
    status = Column(String, default="pending")  # pending|paid|active|expired
    panel_user_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="orders")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    tx_hash = Column(String, unique=True, nullable=True)
    type = Column(String)  # deposit | purchase | referral
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
