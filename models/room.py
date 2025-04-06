# models/room.py
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from models.message import Message  # Import Message จาก message.py

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))