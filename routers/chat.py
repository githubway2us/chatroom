# routers/chat.py
from fastapi import APIRouter, Depends, WebSocket, HTTPException, WebSocketDisconnect
from sqlalchemy.orm import Session
from database import get_db
from models.message import Message
from models.user import User
from models.room import Room
from routers.auth import get_current_user
from pydantic import BaseModel
import json

router = APIRouter()

class MessageCreate(BaseModel):
    content: str

class RoomCreate(BaseModel):
    name: str

# สร้างห้อง
@router.post("/rooms")
def create_room(room: RoomCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_room = Room(name=room.name, creator_id=user.id)  # บันทึก creator_id
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return {"msg": "Room created", "room_id": db_room.id}

# ดึงรายการห้อง
@router.get("/rooms")
def get_rooms(db: Session = Depends(get_db)):
    rooms = db.query(Room).all()
    return [{"id": room.id, "name": room.name, "creator_id": room.creator_id} for room in rooms]

# ส่งข้อความผ่าน REST
@router.post("/rooms/{room_id}/messages")
def send_message(room_id: int, message: MessageCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    db_message = Message(content=message.content, user_id=user.id, room_id=room_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return {"msg": "Message sent", "message_id": db_message.id}

# ดึงประวัติข้อความ
@router.get("/rooms/{room_id}/messages")
def get_messages(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    messages = db.query(Message).filter(Message.room_id == room_id).order_by(Message.created_at).all()
    return [{"id": msg.id, "content": msg.content, "user_id": msg.user_id, "created_at": msg.created_at.isoformat()} for msg in messages]

# ลบห้อง (เฉพาะผู้สร้าง)
@router.delete("/rooms/{room_id}")
def delete_room(room_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.creator_id != user.id:
        raise HTTPException(status_code=403, detail="Only the creator can delete this room")
    db.query(Message).filter(Message.room_id == room_id).delete()  # ลบข้อความทั้งหมดในห้อง
    db.delete(room)
    db.commit()
    return {"msg": "Room deleted"}

# WebSocket สำหรับแชทแบบเรียลไทม์
active_connections = {}  # เก็บการเชื่อมต่อ WebSocket ตาม room_id

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, db: Session = Depends(get_db)):
    await websocket.accept()
    if room_id not in active_connections:
        active_connections[room_id] = []
    active_connections[room_id].append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            content = message_data.get("content")
            user_id = message_data.get("user_id")
            
            room = db.query(Room).filter(Room.id == room_id).first()
            if not room:
                await websocket.send_text(json.dumps({"error": "Room not found"}))
                break
            
            # บันทึกข้อความลงฐานข้อมูล
            db_message = Message(content=content, user_id=user_id, room_id=room_id)
            db.add(db_message)
            db.commit()
            db.refresh(db_message)
            
            # ส่งข้อความไปยังทุก client ในห้อง
            broadcast_msg = json.dumps({
                "id": db_message.id,
                "content": db_message.content,
                "user_id": db_message.user_id,
                "created_at": db_message.created_at.isoformat()
            })
            for connection in active_connections[room_id]:
                await connection.send_text(broadcast_msg)
    except WebSocketDisconnect:
        active_connections[room_id].remove(websocket)
        if not active_connections[room_id]:
            del active_connections[room_id]
    except Exception as e:
        await websocket.send_text(json.dumps({"error": str(e)}))