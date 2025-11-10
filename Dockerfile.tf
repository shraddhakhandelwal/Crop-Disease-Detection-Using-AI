# Dockerfile using official TensorFlow base image to avoid long pip TensorFlow install
# This image uses an official TensorFlow runtime image with Python and TF preinstalled.
# It installs only the remaining Python packages from requirements.txt (excluding TensorFlow).

FROM tensorflow/tensorflow:2.10.0

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy requirements and remove tensorflow line before installing to avoid reinstalling
COPY requirements.txt ./
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/* || true
# Create a requirements file without the tensorflow entry
RUN grep -vi "^tensorflow" requirements.txt > req_no_tf.txt || cp requirements.txt req_no_tf.txt

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r req_no_tf.txt

COPY . /app

EXPOSE 5000

CMD ["python", "src/app.py", "--model", "models/model.h5", "--labels", "models/model_labels.json", "--host", "0.0.0.0", "--port", "5000"]
