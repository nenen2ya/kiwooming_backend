from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.ui_service import get_ui_structure

from pydantic import BaseModel
from services.ai_service import get_ai_response

from fastapi import FastAPI, Query
from services.api_service import get_chart
from services.api_service import get_quote

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

@app.get("/chart/{stk_cd}")
def chart(stk_cd: str, base_dt: str = Query(...), upd_stkpc_tp: str = "1"):
    return get_chart(stk_cd, base_dt, upd_stkpc_tp)

@app.get("/quote/{stk_cd}")
def market_condition(stk_cd: str):
    data = get_quote(stk_cd)
    return data

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
    

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
