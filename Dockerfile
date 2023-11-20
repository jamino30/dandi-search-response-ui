FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
EXPOSE 11434

CMD ["uvicorn", "rest.app:app", "--host", "0.0.0.0", "--port", "8000"]