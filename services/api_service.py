# services/api_service.py
import os
import time
import requests

KIWOOM_API_BASE = os.getenv("KIWOOM_API_BASE", "https://api.kiwoom.com")
API_ID_CHART = os.getenv("KIWOOM_API_ID_CHART", "ka10081")
API_ID_MRKCOND = os.getenv("KIWOOM_API_ID_MRKCOND", "ka10004")

# --- 토큰 캐싱 ---
_token_cache = {"access_token": None, "expires_at": 0}

def _fetch_access_token():
    url = f"{KIWOOM_API_BASE}/oauth2/token"
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    body = {
        "grant_type": "client_credentials",
        "appkey": os.getenv("KIWOOM_API_KEY"),
        "secretkey": os.getenv("KIWOOM_API_SECRET"),
    }
    res = requests.post(url, headers=headers, json=body, timeout=20)
    data = res.json()
    if res.status_code == 200 and data.get("return_code") == 0:
        # expires_dt 는 문자열이므로, 안전하게 50분짜리 캐시로 처리
        _token_cache["access_token"] = data["token"]
        _token_cache["expires_at"] = time.time() + 50 * 60
        return data["token"]
    raise RuntimeError(f"토큰발급 실패: {data}")

def get_access_token():
    if _token_cache["access_token"] and time.time() < _token_cache["expires_at"]:
        return _token_cache["access_token"]
    return _fetch_access_token()

def _auth_headers(api_id: str | None):
    token = get_access_token()
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {token}",
    }
    if api_id:
        headers["api-id"] = api_id
    return headers

def get_chart(stk_cd: str, base_dt: str, upd_stkpc_tp: str = "1"):
    """
    /api/dostk/chart (일봉)
    """
    url = f"{KIWOOM_API_BASE}/api/dostk/chart"
    headers = _auth_headers(API_ID_CHART)
    body = {"stk_cd": stk_cd, "base_dt": base_dt, "upd_stkpc_tp": upd_stkpc_tp}
    res = requests.post(url, headers=headers, json=body, timeout=20)
    try:
        data = res.json()
    except Exception:
        data = {"raw": res.text}
    return data

def get_quote(stk_cd: str):
    """
    /api/dostk/mrkcond (호가/시장상태)
    """
    url = f"{KIWOOM_API_BASE}/api/dostk/mrkcond"
    headers = _auth_headers(API_ID_MRKCOND)
    body = {"stk_cd": stk_cd}
    res = requests.post(url, headers=headers, json=body, timeout=20)
    try:
        data = res.json()
    except Exception:
        data = {"raw": res.text}
    return data
