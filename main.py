# main.py
from fastapi import FastAPI
from routers import auth, chat, bot
from database import Base, engine
from models.user import User
from models.room import Room
from models.message import Message
from sqlalchemy.orm import Session
import uvicorn

app = FastAPI()

# ฟังก์ชันสร้างห้องเริ่มต้น
def create_default_rooms(db: Session):
    default_rooms = [
        {"name": "#ทั่วไป"},
        {"name": "#สอบถาม"},
        {"name": "#แจ้งปัญหาการใช้งาน"}
    ]
    
    # ตรวจสอบและสร้างห้องถ้ายังไม่มี
    for room_data in default_rooms:
        existing_room = db.query(Room).filter(Room.name == room_data["name"]).first()
        if not existing_room:
            new_room = Room(name=room_data["name"])
            db.add(new_room)
    db.commit()

# สร้างตารางและห้องเริ่มต้น
Base.metadata.create_all(bind=engine)

# เริ่มต้นฐานข้อมูลด้วยห้องเริ่มต้น
from database import get_db
with next(get_db()) as db:
    create_default_rooms(db)

app.include_router(auth.router, prefix="/auth")
app.include_router(chat.router, prefix="/chat")
app.include_router(bot.router, prefix="/bot")

@app.get("/")
def root():
    return {"message": "Welome to the chat API -PUK PUKUMPEE-"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5555)