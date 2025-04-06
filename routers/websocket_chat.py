from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from database import USERS, ROOMS
from services.crypto_bot import get_crypto_price
from services.gpt_bot import ask_gpt  # นำเข้าฟังก์ชันจาก services/gpt_bot.py
import json
from websocket.connection_manager import ConnectionManager

# สร้าง APIRouter
router = APIRouter()
manager = ConnectionManager()

# WebSocket endpoint ที่จัดการการเชื่อมต่อระหว่างผู้ใช้และห้อง
@router.websocket("/ws/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str):
    # ตรวจสอบห้องและผู้ใช้
    if room_id not in ROOMS or user_id not in USERS:
        await websocket.close(code=4000)
        return

    # เชื่อมต่อ WebSocket
    await manager.connect(room_id, websocket)
    user = USERS[user_id]
    await manager.broadcast(room_id, f"📥 {user.display_name} เข้าร่วมห้องแล้ว")

    try:
        # ฟังข้อความจากผู้ใช้
        while True:
            data = await websocket.receive_text()
            message = f"{user.display_name}: {data}"
            await manager.broadcast(room_id, message)

            # === 💬 BOT LOGIC HERE ===
            response = handle_bot_response(data)
            if response:
                await manager.broadcast(room_id, f"🤖 บอท: {response}")

    except WebSocketDisconnect:
        # ถ้าผู้ใช้ตัดการเชื่อมต่อ
        manager.disconnect(room_id, websocket)
        await manager.broadcast(room_id, f"📤 {user.display_name} ออกจากห้อง")


# ฟังก์ชันตรวจสอบคำสั่งจากผู้ใช้และตอบกลับ
def handle_bot_response(text: str) -> str | None:
    # คำสั่งพื้นฐาน
    if "ราคา" in text and "BTC" in text:
        price = get_crypto_price("BTCUSDT")
        return f"ราคาบิทคอยน์ตอนนี้: {price} USDT"

    if "สวัสดี" in text:
        return "สวัสดีครับ 👋 มีอะไรให้ช่วยมั้ย?"

    # ถ้าไม่ตรงกับคำสั่งทั่วไป → ส่งให้ GPT ช่วยตอบ
    if len(text.strip()) > 5:
        return ask_gpt(text)  # เรียก GPT บอทตอบกลับ

    return None
