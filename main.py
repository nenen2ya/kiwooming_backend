from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.ui_service import get_ui_structure

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

@app.get("/{screen_name}")
def fetch_ui(screen_name: str):
    data = get_ui_structure(screen_name)
    return data
