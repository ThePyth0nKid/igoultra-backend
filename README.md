# iGoUltra Backend

Das iGoUltra-Backend bildet die serverseitige Grundlage des gesamten iGoUltra-Ökosystems. Es stellt REST-APIs bereit, die von Web‑Frontend, mobilen Apps, AR/VR‑Anwendungen und dem Discord‑Bot genutzt werden.

## 🚀 Vision
Das Projekt verfolgt das Ziel, Bewegung spielerisch zu fördern und virtuelle sowie reale Fitness miteinander zu verbinden. Ein zentrales Backend ermöglicht plattformübergreifende Ranglisten, Seasons und zukünftig auch eine eigene Währung.

## 📖 Inhaltsverzeichnis
- [Features](#features)
- [🧠 Skills- & XP-System](#skills--xp-system)
- [Technologie-Stack](#technologie-stack)
- [Quickstart](#quickstart)
- [API-Dokumentation](#api-dokumentation)
- [Projektstruktur](#projektstruktur)
- [Datenmodelle](#datenmodelle)
- [API-Übersicht](#api-übersicht)
- [Testing](#testing)
- [Deployment](#deployment)
- [Coding Standards](#coding-standards)
- [Contributing](#contributing)
- [Ressourcen](#ressourcen)

## ✨ Features
- **Discord OAuth** und **JWT‑Authentifizierung**
- **XP- und Levelsystem** inklusive saisonbasierter Rankings
- **Layer-abhängige Leaderboards** (Real/Cyber)
- **Swagger UI** für interaktive API-Dokumentation
- **Erweiterbare Architektur** für künftige Module wie Bitgold, Wallet oder Skills

## 🧠 Skills- & XP-System

Das Skills- und XP-System ist modular, API-basiert und voll funktionsfähig integriert:

### Features & API

- **XP-System:** 4 XP-Typen (Physical, Mental, Cyber, Ultra)
- **Stats:** 5 Kategorien (Body, Mind, Spirit, Combat, Tech) – werden durch XP automatisch erhöht
- **Skills:**
  - Layer: Real/Cyber
  - Voraussetzungen: Level, XP-Typ, Stats
  - Freischaltung nur bei erfüllten Anforderungen
- **REST API:**
  - `POST   /api/v1/xp/add/`           → XP-Eintrag
  - `GET    /api/v1/skills/stats/`     → Stat-Übersicht
  - `GET    /api/v1/skills/`           → Skill-Übersicht
  - `GET    /api/v1/skills/available/` → Skills mit Freischalt-Status
  - `GET    /api/v1/skills/unlocked/`  → Freigeschaltete Skills
  - `POST   /api/v1/skills/unlock/`    → Skill-Freischaltung
  - `GET    /api/v1/skills/<id>/progress/` → Skill-Fortschritt

### Modularer Aufbau

- **skills/models.py:**
  - `CharacterStats` (pro User, alle Stats)
  - `Skill` (mit Layer, Voraussetzungen, Effekten)
  - `UserSkill` (freigeschaltete Skills)
- **skills/services.py:**
  - Stat-Berechnung, Skill-Freischaltung, Progress
- **skills/serializers.py:**
  - Serializers für alle API-Objekte
- **skills/views.py:**
  - Alle Endpunkte als ViewSets/Generics
- **skills/urls.py:**
  - Sauberes Routing, einfach erweiterbar

### Test & Beispiel-Daten

- **Fixtures:**
  - `skills/fixtures/skills.json` (Beispiel-Skills)
- **Management-Command:**
  - `python manage.py test_skills_system`  → Testet XP, Stat-Update, Skill-Freischaltung

### Hinweise

- Skills, Stats, XP-Typen und Logik sind **leicht erweiterbar**.
- Die API ist **RESTful** und kann direkt im Frontend/Swagger UI getestet werden.
- Die Stat-Logik ist zentral in `skills/services.py` und kann für komplexere Progression angepasst werden.

**Das System ist bereit für den produktiven Einsatz und für weitere Game-Logik!**

---

## 🛠 Technologie-Stack
- **Python 3.13** und **Django 5.2** mit **Django REST Framework**
- **PostgreSQL** als Datenbank über `psycopg2-binary`
- **Authentifizierung:** `dj-rest-auth`, `django-allauth`, `djangorestframework_simplejwt`
- **API-Dokumentation:** `drf-spectacular` mit Swagger UI
- **CORS & Debug:** `django-cors-headers`, `django-debug-toolbar`, `django-extensions`
- **Deployment:** `gunicorn`, `whitenoise`, `dj-database-url`

## ⚡ Quickstart

### Voraussetzungen
- Python 3.13+
- Git
- PostgreSQL (optional, SQLite für Entwicklung)

### Installation
1. **Repository klonen**
   ```bash
   git clone https://github.com/DEIN_GITHUB_ACCOUNT/igoultra-backend.git
   cd igoultra-backend
   ```

2. **Virtuelle Umgebung erstellen und aktivieren**
   ```bash
   python -m venv venv
   # Windows (Git Bash)
   source venv/Scripts/activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```

4. **Umgebungsvariablen konfigurieren**
   ```bash
   # .env Datei erstellen
   cp .env.example .env
   # Bearbeite .env mit deinen Werten
   ```

5. **Datenbank initialisieren**
   ```bash
   python manage.py migrate
   python manage.py loaddata layers/fixtures/layers.json
   python manage.py loaddata xp/fixtures/xptypes.json
   ```

6. **Superuser erstellen**
   ```bash
   python manage.py createsuperuser
   ```

7. **Server starten**
   ```bash
   python manage.py runserver
   ```

## 📚 API-Dokumentation

### Swagger UI
Die interaktive API-Dokumentation ist verfügbar unter:
```
http://localhost:8000/api/docs/
```

**Features:**
- ✅ Vollständige API-Dokumentation
- ✅ Interaktive Endpunkt-Tests
- ✅ Authentifizierung über JWT-Token
- ✅ Request/Response-Beispiele
- ✅ Schema-Validierung

### OpenAPI Schema
Das maschinenlesbare API-Schema ist verfügbar unter:
```
http://localhost:8000/api/schema/
```

### Authentifizierung
Die API verwendet JWT-Token für die Authentifizierung:

1. **Token erhalten:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/jwt/create/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'
   ```

2. **API mit Token aufrufen:**
   ```bash
   curl -X GET http://localhost:8000/api/v1/xp/leaderboard/ \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

## 🗂 Projektstruktur
```
igoultra-backend/
├── api/                    # Versionierte API (aktuell v1)
│   └── v1/
│       ├── auth/          # Authentifizierung
│       ├── rankings/      # Leaderboards
│       ├── seasons/       # Saisonverwaltung
│       ├── user/          # User-Endpunkte
│       └── xp/            # XP-System
├── users/                 # Benutzer und Authentifizierung
├── xp/                    # XP-System (Modelle, Services)
├── seasons/               # Saisonverwaltung
├── rankings/              # Leaderboards nach Layer
├── layers/                # Layer-System (Real/Cyber)
├── ultrabackend/          # Django-Haupteinstellungen
│   └── settings/          # Umgebungsspezifische Settings
├── bitgold/               # Platzhalter für künftige Währung
├── wallet/                # Platzhalter für Wallet-Funktionen
├── inventory/             # Platzhalter für Items
├── store/                 # geplanter Ingame-Store
├── skills/                # noch leere App für Skills
├── community_rang/        # Community-Ranglisten (geplant)
├── stats/                 # Statistiken (geplant)
└── manage.py, requirements.txt, ...
```

### App-Übersicht

#### **API (`api/v1`)**
Zentrale API-Endpunkte mit Versionierung:
```python
# Beispiel: XP hinzufügen
class AddXpView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddXpSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        result = add_xp_to_user(
            user=request.user,
            type_key=ser.validated_data['key'],
            amount_units=ser.validated_data['amount_units'],
            metadata=ser.validated_data.get('metadata')
        )
        return Response({
            'awarded_xp': result['awarded_xp'],
            'total_xp': result['total_xp'],
            'level': result['level'],
        })
```

#### **Users**
Erweiterte User-Modelle mit Discord-Integration:
```python
class User(AbstractUser):
    discord_id = models.CharField(max_length=64, unique=True, null=True, blank=True)
    ultra_name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    real_layer = models.CharField(max_length=20, choices=REAL_LAYERS, default=REAL_LAYERS[0])
    cyber_layer = models.CharField(max_length=20, choices=CYBER_LAYERS, default=CYBER_LAYERS[0])
```

#### **XP-Services**
Kern-XP-System mit Layer-Unterstützung:
```python
@transaction.atomic
def add_xp_to_user(user, type_key, amount_units, layer_type="Real-Life", metadata=None):
    xp_type = XpType.objects.get(key=type_key)
    real_xp = int(amount_units * xp_type.xp_amount)
    XpEvent.objects.create(
        user=user, 
        amount=real_xp, 
        source=type_key, 
        layer_type=layer_type, 
        metadata=metadata or {}
    )
    user.xp = max(0, user.xp + real_xp)
    user.level = level_from_xp(user.xp)
    user.save(update_fields=['xp', 'level'])
    return get_xp_stats(user)
```

#### **Layers**
Layer-System für Real- und Cyber-Welten:
```python
class Layer(models.Model):
    code = models.CharField(max_length=10, unique=True)  # z.B. "RL0", "CL1"
    name = models.CharField(max_length=50)               # z.B. "Base", "DeepNet"
    type = models.CharField(max_length=10, choices=LAYER_TYPE_CHOICES)
    order = models.PositiveIntegerField()
    description = models.TextField(blank=True)
```

#### **Seasons**
Saisonbasierte Wettbewerbe:
```python
class Season(models.Model):
    name = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField()
    is_active = models.BooleanField(default=False)
```

#### **Rankings**
Layer-spezifische Leaderboards:
```python
class LayerRankingEntry(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    xp = models.PositiveIntegerField()
    layer_type = models.CharField(max_length=20, choices=LAYER_TYPE_CHOICES)
```

## 🗃 Datenmodelle

### User & Authentifizierung
```python
class User(AbstractUser):
    discord_id = models.CharField(max_length=64, unique=True, null=True, blank=True)
    ultra_name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    real_layer = models.CharField(max_length=20, choices=REAL_LAYERS, default=REAL_LAYERS[0])
    cyber_layer = models.CharField(max_length=20, choices=CYBER_LAYERS, default=CYBER_LAYERS[0])
```

### XP-System
```python
class XpEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    source = models.CharField(max_length=50)
    layer_type = models.CharField(max_length=20, choices=LAYER_TYPE_CHOICES)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

class SeasonXp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    xp = models.IntegerField()
    layer_type = models.CharField(max_length=20, choices=LAYER_TYPE_CHOICES)
```

### Layer-System
```python
class Layer(models.Model):
    code = models.CharField(max_length=10, unique=True)  # "RL0", "CL1", etc.
    name = models.CharField(max_length=50)               # "Base", "DeepNet", etc.
    type = models.CharField(max_length=10, choices=LAYER_TYPE_CHOICES)
    order = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    essence = models.CharField(max_length=200, blank=True)
    player_action = models.CharField(max_length=200, blank=True)
```

## 📡 API-Übersicht

### Authentifizierung
| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| `/api/v1/auth/jwt/create/` | POST | JWT-Token erstellen |
| `/api/v1/auth/jwt/refresh/` | POST | JWT-Token erneuern |
| `/api/v1/auth/discord/callback/` | GET | Discord OAuth Callback |

### XP-System
| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| `/api/v1/xp/submit/` | POST | XP einreichen |
| `/api/v1/xp/leaderboard/` | GET | XP-Rangliste |
| `/api/v1/xp/stats/` | GET | XP-Statistiken |

### Rankings
| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| `/api/v1/rankings/layer/` | GET | Layer-spezifische Rankings |
| `/api/v1/rankings/season/` | GET | Saison-Rankings |

### User
| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| `/api/v1/user/me/` | GET | Eigenes Profil |
| `/api/v1/user/profile/` | PUT | Profil aktualisieren |

### Seasons
| Endpoint | Methode | Beschreibung |
|----------|---------|--------------|
| `/api/v1/seasons/` | GET | Alle Seasons |
| `/api/v1/seasons/active/` | GET | Aktive Season |

## ✅ Testing

### Lokale Tests ausführen
```bash
# Alle Tests
python manage.py test

# Spezifische App
python manage.py test users

# Mit Coverage
coverage run --source='.' manage.py test
coverage report
```

### Test-Daten erstellen
```bash
# Test-User erstellen
python manage.py create_test_users

# Zufällige XP vergeben
python manage.py give_random_test_xp
```

## ☁ Deployment

### Heroku Deployment
```bash
# Heroku CLI installieren und einloggen
heroku login

# App erstellen
heroku create igoultra-backend

# Umgebungsvariablen setzen
heroku config:set DJANGO_SECRET_KEY="your-secret-key"
heroku config:set DATABASE_URL="your-database-url"
heroku config:set DISCORD_CLIENT_ID="your-discord-client-id"
heroku config:set DISCORD_CLIENT_SECRET="your-discord-client-secret"

# Deployen
git push heroku main

# Migrationen ausführen
heroku run python manage.py migrate
heroku run python manage.py loaddata layers/fixtures/layers.json
heroku run python manage.py loaddata xp/fixtures/xptypes.json
```

### Docker Deployment
```bash
# Docker Compose verwenden
docker-compose up -d

# Oder direkt mit Dockerfile
docker build -t igoultra-backend .
docker run -p 8000:8000 igoultra-backend
```

## ✨ Coding Standards

### Code-Style
- **Python:** PEP 8 konform
- **Django:** Django Coding Style
- **Kommentare:** Deutsch für Business-Logik, Englisch für technische Details
- **Docstrings:** Deutsch für öffentliche APIs

### API-Konventionen
- **Versionierung:** `/api/v1/` für alle Endpunkte
- **Authentifizierung:** JWT-Token über Authorization Header
- **Response-Format:** JSON mit konsistenter Struktur
- **Error-Handling:** HTTP-Status-Codes + strukturierte Fehlermeldungen

### Git Workflow
```bash
# Feature Branch erstellen
git checkout -b feature/neue-funktion

# Änderungen committen
git add .
git commit -m "feat: neue Funktion hinzugefügt"

# Push und Pull Request
git push origin feature/neue-funktion
```

## 🤝 Contributing

1. **Fork** das Repository
2. **Branch** erstellen: `git checkout -b feature/amazing-feature`
3. **Änderungen** committen: `git commit -m 'feat: amazing feature'`
4. **Push** zum Branch: `git push origin feature/amazing-feature`
5. **Pull Request** erstellen

### Commit-Konventionen
- `feat:` neue Features
- `fix:` Bug-Fixes
- `docs:` Dokumentation
- `style:` Code-Style Änderungen
- `refactor:` Code-Refactoring
- `test:` Tests hinzufügen/ändern
- `chore:` Build-Prozess, Dependencies

## 📚 Ressourcen

### Dokumentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [drf-spectacular (Swagger)](https://drf-spectacular.readthedocs.io/)
- [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io/)

### Deployment
- [Heroku Django Guide](https://devcenter.heroku.com/categories/python-support)
- [Docker Django Guide](https://docs.docker.com/samples/django/)

### Community
- [Django Forum](https://forum.djangoproject.com/)
- [Django Users Mailing List](https://groups.google.com/forum/#!forum/django-users)

---

## 📝 Hinweis
Dieses Backend ist Teil des iGoUltra-Universums. Für Frontend oder Discord-Integration existieren separate Repositories.

**Entwickelt mit ❤️ für die iGoUltra Community**
