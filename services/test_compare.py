import requests
from services.ui_service import get_ui_structure

if __name__ == "__main__":
    # 1️⃣ 백엔드 UI 데이터
    screen_data = get_ui_structure("Home")

    # 2️⃣ 파서 데이터
    parser_res = requests.get("http://localhost:4001/parse/Home")
    parser_data = parser_res.json()

    # 3️⃣ AI 서버 비교
    payload = {
        "screen": "Home",
        "ui_data": screen_data,
        "parser_data": parser_data
    }

    res = requests.post("http://localhost:6002/compare", json=payload)
    print(res.json())
