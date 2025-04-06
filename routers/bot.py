# routers/bot.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.crypto_bot import CryptoBot
from services.welcome_bot import WelcomeBot

router = APIRouter()

@router.get("/bot/crypto")
def get_crypto_price(currency: str, db: Session = Depends(get_db)):
    bot = CryptoBot()
    price = bot.get_price(currency)
    return {"currency": currency, "price": price}

@router.post("/bot/welcome")
def send_welcome_message(room_id: int, db: Session = Depends(get_db)):
    bot = WelcomeBot()
    message = bot.generate_welcome_message()
    db_message = Message(content=message, room_id=room_id)
    db.add(db_message)
    db.commit()
    return {"msg": "Welcome message sent"}