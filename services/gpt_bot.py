# services/gpt_bot.py

import openai

# ตั้งค่า API Key ของคุณ
openai.api_key = "your-openai-api-key"

def ask_gpt(message: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # หรือ gpt-4 ถ้าคุณใช้ได้
            messages=[
                {"role": "system", "content": "คุณเป็นผู้ช่วยในห้องแชท"},
                {"role": "user", "content": message}
            ],
            max_tokens=100,
            temperature=0.8
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return "❌ ขอโทษครับ บอท AI ตอบไม่ได้ตอนนี้"
