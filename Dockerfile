FROM python:3.8-slim
ENV PYTHONUNBUFFERED True
WORKDIR /app
COPY *.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt
COPY . ./
CMD exec gunicorn --preload --bind :$PORT --workers 1 --threads 8 --timeout 0 app.bot:app