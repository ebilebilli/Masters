# Professionals Platform API

## Tech Stack

<div style="display: flex; justify-content: center; align-items: center; gap: 20px;">
  <img src="static/django.png" alt="Django" height="50" />
  <img src="static/drf.png" alt="DRF" height="50" />
  <img src="static/celery.png" alt="Celery" height="50" />
  <img src="static/redis.png" alt="Redis" height="50" />
  <img src="static/postgresql.png" alt="PostgreSQL" height="50" />
  <img src="static/aws_s3.png" alt="AWS S3" height="50" />
  <img src="static/swagger.png" alt="Swagger" height="50" />
</div>

## Overview
A robust, modular Django REST API for managing professionals ("professionals"), services, reviews, and user authentication. Features JWT auth, OTP, Redis-cache-powered search, async tasks with Celery, and cloud-ready deployment.

---


## Features
- Modular RESTful APIs for users, services, reviews, and search
- JWT authentication & OTP password reset
- Redis-cache for advanced search (Elasticsearch ready, but will apply for product step)
- Celery + Redis for async/background tasks
- AWS S3 integration for media storage
- Dockerized for easy deployment
- Swagger/OpenAPI documentation

---



- **Backend:** Django 5.2, Django REST Framework
- **Auth:** JWT (SimpleJWT), OTP
- **Async:** Celery, Redis
- **Search:** Redis-cache for advanced search (Elasticsearch ready, but will apply for product step)
- **Storage:** AWS S3, django-storages
- **API Docs:** drf-yasg, django-rest-swagger
- **Deployment:** Docker, Gunicorn, Whitenoise
- **Database:** PostgreSQL (recommended)

<details>
<summary>All Python dependencies</summary>

```
# requirements.txt (partial)
Django==5.2.1
djangorestframework==3.16.0
djangorestframework_simplejwt==5.5.0
celery==5.5.2
redis==6.1.0
django-elasticsearch-dsl==8.0
elasticsearch==8.18.1
django-storages==1.14.6
boto3==1.34.103
gunicorn==23.0.0
psycopg2-binary==2.9.10
# ... see requirements.txt for full list
```
</details>

---

## Project Structure
```
masters/
  apis/
    core_apis/      # Cities, languages
    user_apis/      # Users, auth, profiles, OTP
    review_apis/    # Reviews
    service_apis/   # Services, categories
    search_apis/    # Search
  core/             # Core models/serializers
  users/            # User models/logic
  reviews/          # Review models/logic
  services/         # Service/category models/logic
  utils/            # Utilities (OTP, permissions, etc)
  manage.py         # Django entrypoint
  Dockerfile        # Docker config
  requirements.txt  # Python dependencies
  ...
```

---

## Setup & Installation
1. **Clone the repo:**
   ```bash
   git clone <your-repo-url>
   cd Masters/masters
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment:**
   - Copy `env.example` to `.env` and set your secrets.
4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Run server:**
   ```bash
   python manage.py runserver
   ```
6. **(Optional) Run with Docker:**
   ```bash
   docker-compose up --build
   ```
7. **Access API docs:**
   - Swagger: `/swagger/` or `/docs/` (see your deployment)

---

## API Endpoints

### User APIs
- `POST   /api/user/register/` — Register user
- `POST   /api/user/login/` — Login user
- `GET    /api/user/profile/` — Get profile
- `PUT    /api/user/profile/update/` — Update profile
- `DELETE /api/user/profile/delete/` — Delete profile
- `POST   /api/user/logout/` — Logout
- `POST   /api/user/password/reset/request/` — Request password reset (OTP)
- `POST   /api/user/password/otp/verify/` — Verify OTP
- `POST   /api/user/password/reset/confirm/` — Confirm password reset
- `POST   /api/user/api/token/` — Obtain JWT
- `POST   /api/user/api/token/refresh/` — Refresh JWT
- **Professionals (Masters):**
  - `GET    /api/user/professionals/` — List all
  - `GET    /api/user/professionals/top/` — Top rated
  - `GET    /api/user/professionals/<id>/` — Detail
  - `DELETE /api/user/professionals/<id>/delete` — Delete
  - **Images:**
    - `GET    /api/user/professionals/<id>/images/` — List images
    - `POST   /api/user/professionals/images/create/` — Add image
    - `DELETE /api/user/professionals/images/delete/` — Delete image

### Review APIs
- `GET    /api/review/professionals/<id>/reviews/` — List reviews for professional
- `POST   /api/review/professionals/<id>/reviews/create/` — Create review
- `PUT    /api/review/professionals/reviews/<id>/update/` — Update review
- `DELETE /api/review/professionals/reviews/<id>/delete/` — Delete review
- `GET    /api/review/professionals/<id>/reviews/filter/` — Filter reviews

### Service APIs
- `GET    /api/service/categories/` — List categories
- `GET    /api/service/category/<id>/professionals/` — Professionals by category
- `GET    /api/service/services/` — List services
- `GET    /api/service/category/<id>/services/` — Services by category
- `GET    /api/service/service/<id>/professionals/` — Professionals by service
- `GET    /api/service/services/statistics/` — Service statistics

### Core APIs
- `GET    /api/core/cities/` — List cities
- `GET    /api/core/languages/` — List languages

### Search APIs
- `POST   /api/search/professionals/search/` — Search professionals

---

