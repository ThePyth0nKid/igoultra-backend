
# iGoUltra – Backend (v1)

This is the backend API of the iGoUltra project – a hybrid between real-life training, XP leveling, and a digital game.  
It is built with Django and Django REST Framework, uses PostgreSQL, and supports Discord OAuth2 login with session-based authentication.

---

## 🔧 Tech Stack

- **Django** + **Django REST Framework**
- **PostgreSQL** via `psycopg2`
- **Session-based authentication** (no JWT)
- **OAuth2 via Discord**
- **Versioned API** (`/api/v1/`)
- Hosted on **Heroku**

---

## 📁 Project Structure

```
igoultra-backend/
├── ultrabackend/        # Django core config (settings, wsgi, urls)
├── api/                 # Versioned API views
│   └── v1/
│       ├── auth/        # Discord login views
│       ├── xp/          # XP endpoints
│       ├── seasons/     # Leaderboard endpoints
│       └── user/        # Current user, profile
├── core/                # Central logic layer (shared services)
│   ├── services/        # Business logic (e.g., XP calculation)
│   ├── constants/       # XP levels, ranks, static values
│   └── utils/           # Reusable helper functions
├── users/               # CustomUser model + Discord Auth
├── xp/                  # XPEntry, XPType models
├── seasons/             # Season, score, leaderboard logic
├── manage.py
├── .env                 # Local dev environment
└── requirements.txt     # Python dependencies
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/igoultra-backend.git
cd igoultra-backend
```

### 2. Create a virtual environment

```bash
python -m venv env
source env/bin/activate    # On Windows: env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your `.env` file

Duplicate the `.env.sample` and rename it to `.env`:

```bash
cp .env.sample .env
```

Edit it and fill in your local database and secret key:

```env
DJANGO_SECRET_KEY=your-secret-key
POSTGRES_DB=igoultra_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
```

---

## 🧪 Database Setup

### Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create a superuser (for admin panel)

```bash
python manage.py createsuperuser
```

---

## ▶️ Run the development server

```bash
python manage.py runserver
```

Then go to: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## 📦 API Endpoints (v1)

All endpoints are prefixed with `/api/v1/`

### Auth

- `POST /api/v1/auth/discord/` → Login via Discord code
- `GET /api/v1/auth/me/` → Get current user (if authenticated)
- `POST /api/v1/auth/logout/` → Logout (with CSRF token)
- `GET /api/v1/auth/csrf/` → Get CSRF cookie

### XP

- `POST /api/v1/xp/add/` → Submit XP event
- `GET /api/v1/xp/stats/` → Get XP, level, progress

### Seasons

- `GET /api/v1/seasons/reality/`
- `GET /api/v1/seasons/cyber/`

---

## 🌐 Deployment

This project is prepared for deployment on **Heroku** with PostgreSQL and automatic `collectstatic`.

Make sure your production `.env` contains:

```env
DEBUG=False
DJANGO_SECRET_KEY=your-secure-production-key
ALLOWED_HOSTS=your-domain.com
```

---

## 📄 License

MIT © 2025 Nelson Nehles
