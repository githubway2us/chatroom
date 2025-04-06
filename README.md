# Chat Room Project

Chat Room Project เป็นโปรแกรมแชทที่พัฒนาด้วย Python โดยใช้ FastAPI สำหรับ API และ SQLAlchemy สำหรับจัดการฐานข้อมูล SQLite โปรเจคนี้ให้บริการห้องแชทแบบเรียลไทม์ผ่าน WebSocket และ REST API รองรับการสร้างห้องแชท, ส่งข้อความ, ลบห้อง, และดึงประวัติข้อความ โดยมีการจัดการผู้ใช้ผ่านระบบ token-based authentication

## คุณสมบัติ
- **REST API**: สร้างห้อง, ดึงรายการห้อง, ส่งข้อความ, ดึงประวัติข้อความ, และลบห้อง
- **WebSocket**: รองรับการแชทแบบเรียลไทม์ในห้องแชท
- **ฐานข้อมูล**: ใช้ SQLite ผ่าน SQLAlchemy เพื่อเก็บข้อมูลห้องและข้อความ
- **การยืนยันตัวตน**: ใช้ OAuth2 ด้วย JWT token สำหรับการเข้าถึง API
- **การจัดการห้อง**: เฉพาะผู้สร้างห้องเท่านั้นที่สามารถลบห้องได้

## ความต้องการ
- **Python**: 3.7 หรือสูงกว่า
- **Dependencies**:
  - `fastapi`: กรอบงานสำหรับสร้าง API
  - `sqlalchemy`: ORM สำหรับจัดการฐานข้อมูล
  - `pydantic`: การตรวจสอบข้อมูล
  - `uvicorn`: ASGI server สำหรับรัน FastAPI
  - `python-jose[cryptography]`: สร้างและตรวจสอบ JWT token
  - `passlib[bcrypt]`: เข้ารหัสพาสเวิร์ด

### การติดตั้ง Dependencies
```bash
pip install fastapi sqlalchemy pydantic uvicorn python-jose[cryptography] passlib[bcrypt]
## การใช้งาน

### รันโปรแกรม:
```bash
uvicorn main:app --reload --port 5555

Server จะรันที่ http://localhost:5555

--reload ช่วยรีโหลดอัตโนมัติเมื่อโค้ดเปลี่ยน

