# Chat API Client - PUK PUKUMPEE

![Python](https://img.shields.io/badge/Python-3.11-blue) ![License](https://img.shields.io/badge/License-MIT-green)

Chat API Client เป็นแอปพลิเคชัน GUI ที่พัฒนาด้วย Python และ Tkinter เพื่อให้ผู้ใช้สามารถโต้ตอบกับ Chat API ได้อย่างง่ายดาย แอปพลิเคชันนี้รองรับการเชื่อมต่อ API, การลงทะเบียน/ล็อกอิน, การจัดการห้องแชท และการส่ง/รับข้อความในห้องแชทต่างๆ โดยมี backend ที่พัฒนาด้วย FastAPI

## คุณสมบัติ

- **เชื่อมต่อ API**: ระบุ URL ของ Chat API เพื่อเชื่อมต่อและตรวจสอบสถานะ
- **การยืนยันตัวตน**: ลงทะเบียนและล็อกอินด้วย username และ password
- **การจัดการห้องแชท**: สร้างห้องแชทใหม่, รีเฟรชรายการห้อง, และเลือกห้องเพื่อดูประวัติแชท
- **การแชท**: ส่งข้อความในห้องที่เลือกและดูประวัติพร้อม timestamp และ username
- **สถานะ**: แสดงสถานะ API และการดำเนินการต่างๆ ในแถบสถานะ
- **ส่วนต่อประสานที่ใช้งานง่าย**: GUI ด้วย Tkinter แบ่งเป็นแท็บ Connection, Authentication และ Chat

## ความต้องการของระบบ

- Python 3.11 หรือสูงกว่า
- ระบบปฏิบัติการ: Windows, macOS, หรือ Linux
- การเชื่อมต่ออินเทอร์เน็ต (สำหรับเชื่อมต่อกับ Chat API)

## การติดตั้ง

### Client (GUI)

1. **โคลน Repository**:
   ```bash
   git clone https://github.com/githubway2us/chatroom.git
   cd chatroom
# การใช้งาน Chat API Client - PUK PUKUMPEE

เอกสารนี้อธิบายขั้นตอนการใช้งาน **Chat API Client** ซึ่งเป็นแอปพลิเคชัน GUI ที่พัฒนาด้วย Tkinter สำหรับโต้ตอบกับ Chat API ที่รันบน FastAPI

## ขั้นตอนการใช้งาน

### 1. รัน Backend
- เริ่ม FastAPI server (local หรือ deployed) เพื่อให้ client สามารถเชื่อมต่อได้
- **Default URL**: `http://localhost:5555`
- **ตัวอย่างการรัน locally**:
  ```bash
  uvicorn main:app --host 0.0.0.0 --port 5555
