FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -c "import sys,joblib,sklearn,numpy,scipy; print('=== BUILD ENV ==='); print('Python:',sys.version); print('joblib:',joblib.__version__); print('sklearn:',sklearn.__version__); print('numpy:',numpy.__version__); print('scipy:',scipy.__version__); print('=== MODEL TEST ==='); joblib.load('models/category/category_model.joblib'); print('MODEL OK'); joblib.load('models/category/category_vectorizer.joblib'); print('VECTORIZER OK')"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]