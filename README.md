# StudyBud

StudyBud is a Django web application for collaborative learning and community discussion. Users create topic-based rooms, hold threaded conversations, and connect with other learners — wrapped in a clean, modern, responsive UI with light/dark themes.

## Features

- **User authentication** — register, log in/out, and manage your profile (email-based login).
- **Rooms & topics** — create, update, and delete discussion rooms organized by topic.
- **Messaging** — threaded conversations inside each room, with a chat-style composer.
- **Participants** — join rooms and see who else is in each one.
- **Profiles** — display name, bio, and avatar uploads.
- **Search & pagination** — partial-match search across rooms, topics, and descriptions.
- **REST API** — read-only JSON endpoints for rooms (Django REST Framework).
- **Modern UI** — flat SaaS-style design, Google Fonts + Material Symbols icons, light/dark mode, and custom 404/500 pages.

## Tech stack

- Python 3.12+ · Django 6.0
- Django REST Framework · django-cors-headers
- WhiteNoise (static file serving) · Gunicorn (production server)
- SQLite (default) · Pillow (image uploads)

## Getting started

### 1. Clone and create a virtual environment

```sh
git clone https://github.com/ronak026/StudyBudy.git
cd StudyBudy
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
```

### 3. Configure environment

Copy the example env file and fill in values:

```sh
cp .env.example .env
```

Generate a secret key:

```sh
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Key settings in `.env`:

| Variable | Description |
| --- | --- |
| `SECRET_KEY` | Django secret key (required in production) |
| `DEBUG` | `True` for development, `False` for production |
| `ALLOWED_HOSTS` | Comma-separated hostnames |
| `CORS_ALLOWED_ORIGINS` | Comma-separated origins allowed to call the API |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated trusted origins for CSRF |

### 4. Migrate and (optionally) seed sample data

```sh
python manage.py migrate
python manage.py seed_data            # 10 users, 15 topics, 50 rooms, messages
```

Sample login from the seeder: `alice@example.com` / `password123`.

### 5. Create an admin user (optional)

```sh
python manage.py createsuperuser
```

### 6. Run the development server

```sh
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Seeding data

A management command populates the database with realistic sample content:

```sh
python manage.py seed_data            # default: 50 rooms
python manage.py seed_data --rooms 30 # custom room count
python manage.py seed_data --flush    # wipe rooms/topics/messages, then reseed
```

## REST API

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/` | List available routes |
| `GET` | `/api/rooms/` | All rooms |
| `GET` | `/api/rooms/<id>/` | A single room (404 if missing) |

## Testing

```sh
python manage.py test
```

The suite (`base/tests.py`) covers models, authentication, room flows, and the API.

## Deployment

The project is deploy-ready (Heroku/Render/Railway-style):

- Configuration is read from environment variables; `DEBUG=False` enables HTTPS/HSTS hardening and secure cookies.
- Static files are served by WhiteNoise. In production, a compressed manifest storage is used and built by `collectstatic`.
- The `Procfile` runs migrations and `collectstatic` on release, then starts Gunicorn:

```Procfile
release: python manage.py migrate --no-input && python manage.py collectstatic --no-input
web: gunicorn studybud.wsgi --log-file -
```

## Project structure

```
StudyBudy/
├── base/                     # main app: models, views, urls, forms, API, tests
│   ├── api/                  # DRF serializers and views
│   ├── management/commands/  # seed_data command
│   ├── migrations/
│   └── templates/base/       # page templates and components
├── studybud/                 # project settings, urls, wsgi/asgi
├── templates/                # base layout, navbar, error pages (404/500)
├── static/                   # css, js, images, favicon
├── manage.py
├── requirements.txt
└── Procfile
```

## Customization

- **Theme & colors** — CSS custom properties (design tokens) live at the top of `static/style/style.css`; edit the `:root` and `.dark-mode` blocks.
- **Avatars** — uploaded to `MEDIA_ROOT/avatars/`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

Made with Django & ❤️
