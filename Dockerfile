FROM python:3.9-alpine

WORKDIR /app
RUN python3 -m pip install --upgrade pip

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

# COPY app .

CMD ["uvicorn", "app.main:app", "--host 0.0.0.0"]