FROM python:3.11-slim

WORKDIR /app

# Lazımlı sistem paketləri (libpq, gcc, gettext)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt kopyala və quraşdır
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Layihə fayllarını kopyala
COPY . .

# collectstatic S3-ə yükləmək üçün AWS mühit dəyişənləri lazım olacaq
RUN python manage.py collectstatic --noinput

# Prod server üçün gunicorn
CMD ["gunicorn", "masters.wsgi:application", "--bind", "0.0.0.0:8000"]
