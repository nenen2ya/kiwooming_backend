# 1️⃣ 베이스 이미지
FROM python:3.11-slim

# 2️⃣ 컨테이너 안의 기본 경로 설정
WORKDIR /app

# 3️⃣ (선택) requirements.txt가 없으므로 FastAPI와 필요한 패키지 직접 설치
RUN pip install --no-cache-dir fastapi uvicorn requests supabase python-dotenv

# 4️⃣ 프로젝트 코드 복사
COPY . .

# 5️⃣ FastAPI 서버 실행 (포트 8000)
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
