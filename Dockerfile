FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD ["python", "./app/main.py"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9090"]



