from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.ui_service import get_ui_structure

from pydantic import BaseModel
from services.ai_service import get_ai_response

app = FastAPI(title="KUM UI Context API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "KUM backend is running"}

@app.get("/ui/{screen_name}")
def fetch_ui(screen_name: str):
    data = get_ui_structure(screen_name)
    return data

class ChatRequest(BaseModel):
    text: str
    context: str | None = None


@app.post("/chat")
def chat_with_ai(req: ChatRequest):
    """
    - text: 사용자가 입력한 메시지
    - context: (선택) 현재 화면 이름 등
    """
    try:
        reply = get_ai_response(req.text, context=req.context)
        return {"reply": reply}
    except Exception as e:
        print("❌ [chat_with_ai ERROR]", e)
        return {"reply": f"오류가 발생했습니다: {str(e)}"}