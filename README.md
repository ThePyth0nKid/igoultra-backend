# iGoUltra Backend

Das iGoUltra-Backend bildet die serverseitige Grundlage des gesamten iGoUltra-Ökosystems. Es stellt REST-APIs bereit, die von Web‑Frontend, mobilen Apps, AR/VR‑Anwendungen und dem Discord‑Bot genutzt werden.

## 🚀 Vision
Das Projekt verfolgt das Ziel, Bewegung spielerisch zu fördern und virtuelle sowie reale Fitness miteinander zu verbinden. Ein zentrales Backend ermöglicht plattformübergreifende Ranglisten, Seasons und zukünftig auch eine eigene Währung.

## 📖 Inhaltsverzeichnis
- [Features](#features)
- [🧠 Skills- & XP-System](#skills--xp-system)
- [Missionssystem (Daily, Weekly, Seasonal Quests)](#missionssystem-daily-weekly-seasonal-quests)
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

## 🏆 Missionssystem (Daily, Weekly, Seasonal Quests)

Das Missionssystem ist modular, API-first und erkennt automatisch Aktivitäten aus dem iGoUltra-Universum. Es verwaltet tägliche, wöchentliche und saisonale Quests, belohnt User und ist vollständig erweiterbar.

### Features & API
- **Missionstypen:** Daily, Weekly, Seasonal (pro Season)
- **Einheiten:** steps, minutes_in_game, pushups, quests_completed, xp_gained, skills_unlocked, layers_completed, social_interactions, workout_sessions, meditation_minutes, hacking_attempts, real_world_activities, ...
- **Belohnungen:** XP, Gold, Ultra-Points
- **Automatische Fortschrittserkennung:** Fortschritt wird bei jeder relevanten Aktivität automatisch aktualisiert
- **REST API:**
  - `GET    /api/v1/missions/active/`         → Alle aktiven Missionen für den User
  - `GET    /api/v1/missions/progress/`       → Fortschritt für eingeloggten User
  - `GET    /api/v1/missions/completed/`      → Abgeschlossene Missionen
  - `GET    /api/v1/missions/seasons/active/` → Aktuelle Season
  - `POST   /api/v1/missions/progress/update/`→ Fortschritt manuell erhöhen (z.B. für Tests)
  - `GET    /api/v1/missions/statistics/`     → Mission-Statistiken für den User
  - `GET    /api/v1/missions/rewards/`        → Gesamt-Belohnungen
  - `GET    /api/v1/missions/`                → Alle Missionen (Admin)
  - `POST   /api/v1/missions/create/`         → Neue Mission anlegen (Admin)
  - `GET    /api/v1/missions/seasons/`        → Alle Seasons (Admin)
  - `POST   /api/v1/missions/seasons/create/` → Neue Season anlegen (Admin)

### Modularer Aufbau
- **missions/models.py:**
  - `Season` (nur eine aktive Season gleichzeitig)
  - `Mission` (Typ, Einheit, Zielwert, Belohnungen, Zeitrahmen, Season)
  - `MissionProgress` (pro User, Fortschritt, Abschluss, Zeitstempel)
- **missions/services.py:**
  - Fortschritts-Update, Belohnungslogik, Statistiken, Vorschläge
- **missions/serializers.py:**
  - Serializers für alle API-Objekte
- **missions/views.py:**
  - Alle Endpunkte als APIViews/Generics
- **missions/urls.py:**
  - Sauberes Routing, einfach erweiterbar
- **missions/signals.py:**
  - Automatische Verknüpfung zu XP, Skills, Layern etc.

### Admin-Panel
- **Missionen, Seasons und Fortschritt** können komfortabel im Django-Admin verwaltet werden
- Automatische Validierung: Nur eine aktive Season, Belohnungen, Zeitrahmen etc.
- Fortschritt und Abschlussstatus pro User einsehbar

### Test & Beispiel-Daten
- **Fixtures:**
  - `missions/fixtures/missions.json` (Beispiel-Missionen & Season)
- **Management-Command:**
  - `python manage.py test_missions_system --create-user`  → Testet das gesamte Missionssystem inkl. Fortschritt, Belohnungen, Statistiken

### Hinweise
- Das System ist **vollständig modular** und kann um Monatsmissionen, Events etc. erweitert werden
- Die API ist **RESTful** und kann direkt im Frontend/Swagger UI getestet werden
- Fortschritt wird automatisch bei XP-Gewinn, Skill-Freischaltung, Layer-Abschluss etc. aktualisiert (siehe signals.py)

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

# Skillsystem: Aktive & Passive Skills

## Übersicht

Das Skill-System unterscheidet zwischen **aktiven** und **passiven** Skills:
- **Aktive Skills**: Müssen vom Spieler ausgelöst werden, haben Effekte wie Schaden, Heilung, Flächenwirkung etc.
- **Passive Skills**: Wirken dauerhaft oder werden automatisch unter bestimmten Bedingungen aktiviert (z. B. Buffs, Auren, Resistenzen).

Jeder Skill gehört zu einem Layer (`Real` oder `Cyber`) und kann weitere Voraussetzungen haben.

---

## Admin Panel: Character Stats einsehen

### Character Stats eines Users anzeigen

Im Django Admin Panel kannst du die Character Stats (Ausdauer, Stärke, etc.) eines Users auf verschiedene Arten einsehen:

#### **1. In der User-Liste**
- Gehe zu: `/admin/users/user/`
- Du siehst eine Spalte **"Character Stats"** mit einem Link "Stats anzeigen"
- Klicke auf den Link, um die detaillierten Stats zu sehen

#### **2. In der User-Detail-Ansicht**
- Klicke auf einen User in der Liste
- Scroll runter zum Abschnitt **"Character Stats"** (standardmäßig eingeklappt)
- Dort siehst du alle Stats direkt übersichtlich dargestellt:
  - **Body Stats**: Strength, Endurance, Agility
  - **Mind Stats**: Intelligence, Focus, Memory  
  - **Spirit Stats**: Willpower, Charisma, Intuition
  - **Combat Stats**: Combat Skill, Reaction Time, Tactical Awareness
  - **Tech Stats**: Hacking, Programming, Cyber Awareness

#### **3. Direkt über CharacterStats**
- Gehe zu: `/admin/skills/characterstats/`
- Dort siehst du alle Character Stats aller User in einer Tabelle
- Du kannst nach Usern filtern und suchen

### Admin Panel Features

- **Automatische Updates**: Stats werden automatisch aktualisiert, wenn User XP sammeln
- **Übersichtliche Darstellung**: Alle Stats sind in Kategorien gruppiert
- **Filter und Suche**: Einfaches Finden von Usern und deren Stats
- **Direkte Links**: Schnelle Navigation zwischen User und Character Stats

---

## Skill-Modell (Felder)

| Feld                | Typ         | Beschreibung                                                                 |
|---------------------|-------------|------------------------------------------------------------------------------|
| name                | str         | Name des Skills                                                              |
| description         | str         | Beschreibung                                                                 |
| layer               | str         | „Real" oder „Cyber"                                                          |
| skill_type          | str         | „active" oder „passive"                                                      |
| required_level      | int         | Mindestlevel                                                                 |
| required_xp_type    | str         | XP-Typ (z. B. „Physical", „Mental")                                          |
| required_xp_amount  | int         | Benötigte XP im Typ                                                          |
| required_stats      | JSON        | Benötigte Stats (z. B. {"strength": 10})                                     |
| effects             | JSON        | Zusätzliche Effekte                                                          |
| category            | str         | Kategorie (z. B. „Combat", „Utility")                                        |
| tier                | int         | Tier-Stufe                                                                   |
| is_active           | bool        | Skill aktiv                                                                  |
| created_at          | datetime    | Erstellungsdatum                                                             |

**Nur für aktive Skills (`skill_type = 'active'`):**
| Feld           | Typ    | Beschreibung                        |
|----------------|--------|-------------------------------------|
| range          | int    | Reichweite in Metern                |
| area_of_effect | int    | Radius der Wirkung in Metern        |
| damage         | int    | Schaden (positiv) oder Heilung (negativ) |
| duration       | int    | Dauer in Sekunden                   |
| effect_type    | str    | Effekt-Typ (z. B. „stun", „burn")   |

**Nur für passive Skills (`skill_type = 'passive'`):**
| Feld             | Typ    | Beschreibung                        |
|------------------|--------|-------------------------------------|
| buff_type        | str    | Art des Buffs (z. B. „resistance")  |
| buff_value       | str    | Wert des Buffs (z. B. „+10%")       |
| trigger_condition| str    | Auslösebedingung (z. B. „on_low_hp")|
| passive_duration | int    | Dauer in Sekunden (optional)        |

---

## Endpunkte

### 1. **Alle Skills (mit Filter)**
**GET** `/api/v1/skills/`  
**Query-Parameter:**  
- `skill_type=active` oder `skill_type=passive`
- `layer=Real` oder `layer=Cyber`
- `category=Combat` usw.

**Beispiel:**  
`GET /api/v1/skills/?skill_type=active&layer=Real`

---

### 2. **Nur aktive Skills**
**GET** `/api/v1/skills/active/`  
**Query-Parameter:**  
- `layer`, `category`, `effect_type` (optional)

**Beispiel:**  
`GET /api/v1/skills/active/?effect_type=stun`

---

### 3. **Nur passive Skills**
**GET** `/api/v1/skills/passive/`  
**Query-Parameter:**  
- `layer`, `category`, `buff_type`, `trigger_condition` (optional)

**Beispiel:**  
`GET /api/v1/skills/passive/?buff_type=shield`

---

### 4. **Skill-Detail**
**GET** `/api/v1/skills/<id>/`  
Zeigt alle Felder, inkl. aktiver/passiver Skill-spezifischer Felder.

---

### 5. **Skill anlegen (Admin)**
**POST** `/api/v1/skills/create/`  
**Body (JSON):**
```json
{
  "name": "Fireball",
  "description": "Du erzeugst eine mächtige Feuerkugel.",
  "layer": "Real",
  "skill_type": "active",
  "required_level": 7,
  "required_xp_type": "Physical",
  "required_xp_amount": 1500,
  "required_stats": {"intelligence": 15, "focus": 12},
  "effects": {"intelligence_bonus": 3, "focus_bonus": 2},
  "category": "Combat",
  "tier": 2,
  "range": 12,
  "area_of_effect": 3,
  "damage": 45,
  "duration": 5,
  "effect_type": "burn"
}
```
**Validierung:**  
- Für `active` müssen mindestens `damage` oder `effect_type` und `range` gesetzt sein.
- Für `passive` müssen `buff_type` und `buff_value` gesetzt sein.

---

### 6. **Verfügbare Skills für User**
**GET** `/api/v1/skills/available/`  
Filterbar nach `layer`, `category`, `skill_type` usw.

---

### 7. **Freigeschaltete Skills des Users**
**GET** `/api/v1/skills/unlocked/`  
**GET** `/api/v1/skills/unlocked/active/`  
**GET** `/api/v1/skills/unlocked/passive/`  

---

### 8. **Skill-Fortschritt & Freischaltung**
**GET** `/api/v1/skills/<id>/progress/`  
**POST** `/api/v1/skills/unlock/`  
Body: `{ "skill_id": 1 }`

---

## Beispiel-Responses

### Aktiver Skill (GET `/api/v1/skills/active/`)
```json
{
  "id": 2,
  "name": "Mind Reader",
  "description": "Du kannst die Gedanken und Emotionen anderer Menschen lesen und verstehen.",
  "layer": "Real",
  "skill_type": "active",
  "required_level": 10,
  "required_xp_type": "Mental",
  "required_xp_amount": 2000,
  "required_stats": {"intelligence": 20, "intuition": 15},
  "effects": {"intelligence_bonus": 5, "charisma_bonus": 3},
  "category": "Utility",
  "tier": 2,
  "is_active": true,
  "created_at": "2025-07-11T14:00:00Z",
  "active_skill_data": {
    "range": 10,
    "area_of_effect": 5,
    "damage": 0,
    "duration": 30,
    "effect_type": "debuff"
  },
  "passive_skill_data": null
}
```

### Passiver Skill (GET `/api/v1/skills/passive/`)
```json
{
  "id": 1,
  "name": "Iron Will",
  "description": "Deine Willenskraft ist unerschütterlich.",
  "layer": "Real",
  "skill_type": "passive",
  "required_level": 5,
  "required_xp_type": "Physical",
  "required_xp_amount": 1000,
  "required_stats": {"willpower": 15, "endurance": 10},
  "effects": {"willpower_bonus": 5, "endurance_bonus": 3},
  "category": "Combat",
  "tier": 1,
  "is_active": true,
  "created_at": "2025-07-11T14:00:00Z",
  "active_skill_data": null,
  "passive_skill_data": {
    "buff_type": "resistance",
    "buff_value": "+15%",
    "trigger_condition": "always_active",
    "duration": null
  }
}
```

---

## Beispiel: Skill freischalten

**POST** `/api/v1/skills/unlock/`
```json
{
  "skill_id": 2
}
```
**Response:**
```json
{
  "success": true,
  "message": "Skill erfolgreich freigeschaltet."
}
```

---

## Beispiel: Skill-Fortschritt

**GET** `/api/v1/skills/2/progress/`
```json
{
  "skill": { ...Skill-Daten... },
  "requirements_met": {
    "level": true,
    "xp": true,
    "stats": true
  },
  "overall_progress": 1.0,
  "can_unlock": true,
  "message": "Alle Voraussetzungen erfüllt",
  "is_unlocked": false
}
```

---

## Hinweise zur Erweiterbarkeit

- Neue Skill-Typen (z. B. „ultimate") können einfach über das Enum und die Serializers ergänzt werden.
- Die API ist so gestaltet, dass Frontends (z. B. 2D/3D-Spiele) alle nötigen Skill-Parameter direkt auslesen können.
- Die Validierung sorgt dafür, dass Skills immer konsistent angelegt werden.

---

**Fragen oder weitere Beispiele gewünscht?**  
Gerne kann ich auch Beispiel-Requests für das Freischalten oder die Skill-Fortschritts-API liefern!

---

## 🧩 Onboarding-Flow, Fehlerquellen & Bugfixes

### Übersicht & Umsetzung
- **Modularer Onboarding-Flow**: Der Onboarding-Prozess ist API-first und umfasst folgende Schritte/Felder:
  - Discord-Login (OAuth, kein klassisches Passwort)
  - Ultraname (Benutzername im iGoUltra-Universum)
  - Fraktion (z.B. Kapitalisten, Kommunisten, Gläubige) – als eigene App, ForeignKey im User
  - Herkunft (z.B. Berlin, Neo-Tokyo, Mars, Unbekannt) – als eigene App, ForeignKey im User
  - Bio (Freitextfeld im User)
  - Avatar (Bild-Upload, separater Endpunkt)
- **API-Integration**:
  - Endpunkte zum Listen aller Fraktionen und Herkünfte
  - PATCH/GET `/api/v1/auth/me/` gibt immer das Feld `missing_onboarding_fields` zurück, das dynamisch alle noch fehlenden Onboarding-Schritte enthält
  - Avatar-Upload über `/api/v1/auth/avatar-upload/`, Bild wird in `media/avatars/` gespeichert, URL nach Upload korrekt gesetzt

### Typische Fehlerquellen & Lösungen
- **500er Fehler** durch falsche Serializer-Argumente (`files=...`):
  - Lösung: Korrekte Übergabe der Daten im View, insbesondere beim Bild-Upload
- **404er Fehler** durch fehlenden oder falsch gesetzten media-Ordner:
  - Lösung: `MEDIA_ROOT` korrekt auf das Projekt-Root setzen (`BASE_DIR.parent / "media"`), Ordner anlegen, Django im Development `/media/`-URLs ausliefern lassen
- **Falsche avatar_url** durch zu frühes Setzen vor dem Speichern:
  - Lösung: Reihenfolge beachten – erst Bild speichern, dann URL generieren und setzen
- **Falsche URL ohne `/avatars/`**:
  - Lösung: Nach dem Speichern die URL mit Unterordner generieren (`/media/avatars/...`)
- **Frontend-Integration**:
  - Das Frontend muss immer die vom Backend gelieferte URL verwenden (z.B. `user.avatar_url`), niemals selbst den Pfad zusammenbauen

### Hinweise zur Resilienz & Sicherheit
- Der Onboarding-Status ist **rein datengetrieben**: Nach jedem Login oder Seiten-Reload prüft das Backend, welche Felder fehlen, und gibt diese als `missing_onboarding_fields` zurück
- Es gibt **kein separates Onboarding-Flag** – der Status ist immer aktuell und kann nicht inkonsistent werden
- **Empfehlung**: Teste, ob nach Abbruch (Tab schließen, Logout) der Onboarding-Status korrekt bleibt und der User beim nächsten Login an der richtigen Stelle weitermachen muss

### Zusammenfassung
Das Onboarding- und Missionssystem ist jetzt API-first, modular und robust. Der Avatar-Upload funktioniert wie gewünscht, alle relevanten Felder und Endpunkte sind vorhanden, und das Frontend kann sich auf die gelieferten URLs verlassen. Alle typischen Fehlerquellen wurden behoben und dokumentiert.

---

## 🛡️ Admin-User-API & Backend-Panel

### Features
- Vollständige User-Admin-API für das Admin-Panel (React/Vite-Frontend)
- Endpunkte für User-Liste, Detail, Bearbeiten, Anlegen, Löschen
- Zugriff nur für eingeloggte User mit `is_staff: true`
- Alle relevanten Felder: id, username, email, is_staff, is_active, ultra_name, bio, avatar_url, avatar, faction, origin, missing_onboarding_fields, date_joined, last_login, level, xp, rank
- **Explizite Unterstützung für Suche, Filter und Sortierung:**
  - `filter_backends = [filters.OrderingFilter, filters.SearchFilter]`
  - **Suchfelder:** `username`, `ultra_name`, `email`
  - **Filterfelder:** `is_active`, `is_staff`, `faction`, `origin`
  - **Sortierfelder:** `date_joined`, `last_login`, `username`, `ultra_name`
- Suche, Filter, Sortierung, Paginierung (DRF-Standard)

### API-Endpunkte
- **GET /api/v1/auth/admin/users/** – User-Liste (mit Suche, Filter, Paginierung)
- **POST /api/v1/auth/admin/users/** – User anlegen
- **GET /api/v1/auth/admin/users/<id>/** – User-Detail
- **PATCH/PUT /api/v1/auth/admin/users/<id>/** – User bearbeiten
- **DELETE /api/v1/auth/admin/users/<id>/** – User löschen

**Hinweis:** Die Endpunkte sind unter `/api/v1/auth/admin/users/` erreichbar, da sie im auth-Router registriert sind.

### Authentifizierung
- JWT-Token wie im restlichen Projekt (Authorization: Bearer ...)
- Nur User mit `is_staff: true` erhalten Zugriff (403 Forbidden sonst)

### Pagination
- Die API liefert standardmäßig paginierte Responses mit `results`-Array:
  ```json
  {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [ ... ]
  }
  ```
- Pagination ist in `settings/base.py` aktiviert:
  ```python
  REST_FRAMEWORK = {
      ...
      "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
      "PAGE_SIZE": 10,
  }
  ```

### last_login Handling
- Das Feld `last_login` wird jetzt **immer** aktualisiert:
  - Nach erfolgreichem Discord-Login (OAuth)
  - Nach klassischem JWT-Login (`/api/v1/auth/jwt/create/`)
- Umsetzung: In beiden Login-Flows wird `user.last_login = timezone.now()` explizit gesetzt und gespeichert.
- Damit ist das Feld im Admin-Panel und in allen API-Responses immer aktuell.

### Typische Probleme & Lösungen
- **404 auf /api/v1/admin/users/**: Die Route ist unter `/api/v1/auth/admin/users/` registriert. Im Frontend die URL entsprechend anpassen.
- **Kein `results`-Array in der Response**: Pagination war nicht aktiviert. Lösung: Pagination in den DRF-Settings aktivieren (siehe oben).
- **Felder `date_joined` und `last_login` fehlen**: Diese Felder wurden im UserSerializer ergänzt und sind jetzt immer enthalten.
- **`last_login` bleibt leer**: Wird bei OAuth/JWT nicht automatisch gesetzt. Lösung: Nach jedem Login explizit setzen (siehe oben).
- **Zugriffsbeschränkung**: Nur User mit `is_staff: true` können die Admin-API nutzen. Andernfalls gibt es 403 Forbidden.

### Beispiel-Response (User-Detail)
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "is_staff": true,
  "is_active": true,
  "ultra_name": "UltraAdmin",
  "bio": "Ich bin der Admin.",
  "avatar_url": "https://example.com/media/avatars/admin.png",
  "avatar": "/media/avatars/admin.png",
  "faction": { "id": 1, "name": "Fraktion A" },
  "faction_id": 1,
  "origin": { "id": 2, "name": "Erde" },
  "origin_id": 2,
  "missing_onboarding_fields": [],
  "date_joined": "2024-07-15T12:34:56Z",
  "last_login": "2024-07-16T08:00:00Z",
  "level": 5,
  "xp": 1234,
  "rank": "Elite"
}
```

---
