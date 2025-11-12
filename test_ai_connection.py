# backend/test_ai_connection.py
import requests

# 1️⃣ AI 서버 로컬 주소
AI_SERVER_URL = "http://localhost:6002/chat"

if __name__ == "__main__":
    test_input = "안녕 AI, 테스트야!"
    
    try:
        res = requests.post(AI_SERVER_URL, json={"text": test_input, "context": "Home"})
        if res.status_code == 200:
            data = res.json()
            print("✅ AI 서버 연결 성공!")
            print("응답:", data.get("reply"))
        else:
            print(f"❌ AI 서버 오류: {res.status_code}")
            print(res.text)
    except Exception as e:
        print("⚠️ AI 서버에 연결할 수 없습니다.")
        print(e)
