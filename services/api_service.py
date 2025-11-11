import requests
import os
import json

KIWOOM_BASE_URL = "https://api.kiwoom.com"
APP_KEY = os.getenv("KIWOOM_APP_KEY")
SECRET_KEY = os.getenv("KIWOOM_SECRET_KEY")

def get_access_token():
    token = os.getenv("KIWOOM_ACCESS_TOKEN")
    if token:
        return token
    raise ValueError("토큰이 .env 파일에 없습니다. 새로 발급해주세요.")

def get_chart(stk_cd: str, base_dt: str, upd_stkpc_tp: str = "1"):
    try:
        token = get_access_token()
        if not token:
            raise ValueError("토큰 발급 실패")

        url = f"{KIWOOM_BASE_URL}/api/dostk/chart"
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": f"Bearer {token}",
            "api-id": "ka10081"
        }
        payload = {
            "stk_cd": stk_cd,
            "base_dt": base_dt,
            "upd_stkpc_tp": upd_stkpc_tp
        }

        response = requests.post(url, headers=headers, json=payload)

        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"❌ [get_chart ERROR] {e}")
        return {"error": str(e)}

def get_quote(stk_cd: str):
    """
    주식시장상황조회요청 (ka10004)
    - Endpoint: /api/dostk/mrkcond
    - Body: { "stk_cd": "005930" }
    """
    token = get_access_token()
    endpoint = f"{KIWOOM_BASE_URL}/api/dostk/mrkcond"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {token}",
        "api-id": "ka10004",
    }
    body = {"stk_cd": stk_cd}

    try:
        print(f"📤 요청 URL: {endpoint}")
        print(f"📦 Headers: {headers}")
        print(f"📨 Body: {body}")

        res = requests.post(endpoint, headers=headers, json=body)
        res.raise_for_status()

        print(f"📡 상태코드: {res.status_code}")
        print(f"📩 응답본문: {res.text}")

        data = res.json()
        if "return_code" in data and data["return_code"] != 0:
            print(f"⚠️ API 오류: {data.get('return_msg')}")
            return {"error": data.get("return_msg"), "code": data.get("return_code")}

        return data

    except Exception as e:
        print("❌ [get_market_condition ERROR]", e)
        return {"error": str(e)}