import os
import requests
from dotenv import load_dotenv

load_dotenv()  # .env 파일 불러오기

API_BASE = os.getenv("KIWOOM_BASE_URL")
API_KEY = os.getenv("KIWOOM_API_KEY")
API_SECRET = os.getenv("KIWOOM_API_SECRET")

def get_stock_info(symbol: str):
    """
    주식 종목 정보 조회 예시
    symbol 예: '005930' (삼성전자)
    """
    url = f"{API_BASE}/api/stock/info"  # 실제 엔드포인트는 Kiwoom 문서 확인 필요
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"symbol": symbol}

    try:
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"❌ [Kiwoom API ERROR]: {e}")
        return {"error": str(e)}
