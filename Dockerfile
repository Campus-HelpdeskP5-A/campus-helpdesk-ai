FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -c "import os,hashlib; p='models/category/category_model.joblib'; print('=== MODEL FILE ==='); print('SIZE:',os.path.getsize(p)); print('SHA256:',hashlib.sha256(open(p,'rb').read()).hexdigest())"
EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]