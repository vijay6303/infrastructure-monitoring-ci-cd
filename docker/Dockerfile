FROM python:3.12-slim

WORKDIR /app

COPY monitoring/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY monitoring/ .

RUN mkdir -p logs reports

CMD ["python", "monitor.py"]
