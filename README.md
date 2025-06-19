# Professionals Platform API

## Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python" height="40" />
  <img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white" alt="Django" height="40" />
  <img src="https://img.shields.io/badge/DRF-ff1709?style=flat&logo=django&logoColor=white" alt="DRF" height="40" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white" alt="PostgreSQL" height="40" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker" height="40" />
  <img src="https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white" alt="Redis" height="40" />>
  <img src="https://img.shields.io/badge/Celery-37814A?style=flat&logo=python&logoColor=white" alt="Celery" height="40" />
  <img src="https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonaws&logoColor=white" alt="AWS" height="40" />
</p>

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
amqp==5.3.1
asgiref==3.8.1
billiard==4.2.1
boto3==1.34.103
botocore==1.34.103
celery==5.5.2
certifi==2025.4.26
charset-normalizer==3.4.2
click==8.2.0
click-didyoumean==0.3.1
click-plugins==1.1.1
click-repl==0.3.0
colorama==0.4.6
coreapi==2.3.3
coreschema==0.0.4
dj-database-url==3.0.0
Django==5.2.1
django-autoslug==1.9.9
django-cities-light==3.10.1
django-cors-headers==4.7.0
django-elasticsearch-dsl==8.0
django-redis==5.4.0
django-rest-swagger==2.2.0
django-sslserver==0.22
django-storages==1.14.6
djangorestframework==3.16.0
djangorestframework_simplejwt==5.5.0
dotenv==0.9.9
drf-yasg==1.21.10
elastic-transport==8.17.1
elasticsearch==8.18.1
elasticsearch-dsl==8.18.0
gunicorn==23.0.0
idna==3.10
inflection==0.5.1
itypes==1.2.0
Jinja2==3.1.6
jmespath==1.0.1
kombu==5.5.3
MarkupSafe==3.0.2
openapi-codec==1.3.2
packaging==25.0
pillow==11.2.1
progressbar2==4.5.0
prompt_toolkit==3.0.51
psycopg2-binary==2.9.10
PyJWT==2.9.0
python-dateutil==2.9.0.post0
python-dotenv==1.1.0
python-utils==3.9.1
pytz==2025.2
PyYAML==6.0.2
redis==6.1.0
requests==2.32.3
s3transfer==0.10.0
simplejson==3.20.1
six==1.17.0
sqlparse==0.5.3
typing_extensions==4.13.2
tzdata==2025.2
Unidecode==1.4.0
uritemplate==4.1.1
urllib3==2.4.0
vine==5.1.0
wcwidth==0.2.13
whitenoise==6.9.0

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

