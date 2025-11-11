# services/ai_service.py
from pathlib import Path
import json
from openai import OpenAI
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "AI" / "project2" / "config.json"
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

client = OpenAI(api_key=config["openai_api_key"])
model_id = config["kiwume_model_id"]

ui_context_cache = {}
conversation_history = [{"role": "system", "content": config.get(
    "kiwooming_system_prompt",
    "당신은 키움증권 MTS 내 AI 반려 챗봇 키우밍입니다. 화면 구조를 바탕으로 맥락을 이해하고 답하세요. 화면 구조에서 찾을 수 없는 정확하지 않은 정보는 전부 잘 모르겠다고 대답합니다."
)}]


def get_ai_response(user_input: str, context: str | None = None) -> str:
    """
    - user_input: 사용자의 입력
    - context: 현재 화면 이름 (예: 'Home', 'Quote')
    """

    try:
        ui_json = ui_context_cache.get(context)
        if not ui_json and context:
            try:
                res = requests.get(f"http://127.0.0.1:4000/parse/{context}")
                if res.status_code == 200:
                    ui_json = res.json()
                    ui_context_cache[context] = ui_json
            except Exception as e:
                print("⚠️ UI 파서 연결 실패:", e)

        rag_context = ""
        try:
            rag_context = search_from_vectorDB(user_input)
        except:
            pass

        prompt = f"""
        [현재 화면 이름]
        {context or '정보 없음'}

        [화면 구조(JSON 기반 인식)]
        {json.dumps(ui_json, ensure_ascii=False, indent=2) if ui_json else 'UI 정보 없음'}

        [참고 지식 (RAG 검색 결과)]
        {rag_context or '없음'}

        [사용자 메시지]
        {user_input}
        """

        conversation_history.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=model_id,
            messages=conversation_history,
            temperature=0.6,
            max_tokens=500,
        )

        reply = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": reply})

        if context and ui_json:
            ui_context_cache[context] = ui_json

        return reply

    except Exception as e:
        print("❌ [get_ai_response ERROR]", e)
        return f"⚠️ 오류 발생: {e}"

def search_from_vectorDB(query: str):
    """ (선택) RAG 검색 로직 자리 — 추후 연결 가능 """
    return ""
