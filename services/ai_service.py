# services/ai_service.py
import requests

AI_SERVER_URL = "https://kiwooming-ai.onrender.com/chat"

def get_ai_response(user_input: str, context: str | None = None) -> str:
    """
    배포된 AI 서버에 요청을 보내는 함수
    """
    try:
        payload = {
            "text": user_input,
            "context": context
        }

        # Render에 배포된 AI 서버로 POST 요청
        res = requests.post(AI_SERVER_URL, json=payload, timeout=20)

        if res.status_code == 200:
            data = res.json()
            return data.get("reply", "⚠️ AI 응답 형식이 올바르지 않습니다.")
        else:
            print(f"❌ [AI SERVER ERROR] {res.status_code}: {res.text}")
            return f"⚠️ AI 서버 오류: {res.status_code}"

    except Exception as e:
        print(f"❌ [get_ai_response ERROR] {e}")
        return "⚠️ AI 서버에 연결할 수 없습니다."
    