# Simple Dockerfile for the Flask demo
FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
# Install minimal packages first; TensorFlow can be large — if you want GPU or full TF, modify accordingly.
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python", "src/app.py", "--model", "models/model.h5", "--labels", "models/model_labels.json", "--host", "0.0.0.0", "--port", "5000"]
