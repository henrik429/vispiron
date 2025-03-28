FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./
COPY frontend ./frontend

RUN poetry config virtualenvs.create false \
   && poetry install --no-root

EXPOSE 8501

ENV API_URL="http://backend:8000/brightest_color"

CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]