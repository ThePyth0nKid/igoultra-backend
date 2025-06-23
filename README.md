# iGoUltra Backend

Das iGoUltra-Backend ist die serverseitige Grundlage des iGoUltra-Ökosystems. Es bietet APIs für Authentifizierung, XP-Management, Leaderboards und weitere Spielfunktionen. Dieses Backend basiert auf **Django**, **Django REST Framework**, und verwendet **PostgreSQL** als Datenbank.

## 📌 Inhaltsverzeichnis
- [Projektbeschreibung](#projektbeschreibung)
- [Technologien](#technologien)
- [Setup & Installation](#setup--installation)
- [Projektstruktur](#projektstruktur)
- [Datenbankmodelle](#datenbankmodelle)
- [API Endpunkte](#api-endpunkte)
- [Testing](#testing)
- [Deployment](#deployment)
- [Coding Standards](#coding-standards)
- [Contributing](#contributing)
- [Weiterführende Ressourcen](#weiterführende-ressourcen)

## 📝 Projektbeschreibung
Das Backend dient als API-first Architektur für:
- Benutzerregistrierung und Authentifizierung (Discord OAuth / JWT)
- XP-System (Schritte, Push-Ups, Läufe etc.)
- Leaderboards mit Ligen und Rangsystem
- Verwaltung von Seasons (Saisons im Spiel)
- Unterstützung künftiger Features wie Gold-/Ultrapunkte-Währung
- Zentrale Schnittstelle für Frontend, Mobile, AR/VR, Discord-Bot

## ⚙️ Technologien
Im Folgenden werden die Kernbibliotheken und -tools aufgeführt, die im Projekt verwendet werden, sowie die Gründe für ihre Auswahl:

- **Python 3.13.x**: Moderne, leistungsfähige und weit verbreitete Programmiersprache mit umfangreichem Ökosystem. Version 3.13 bringt Performance-Verbesserungen und neue Sprachfeatures.
- **Django 5.2**: Robustes, batteries-included Web-Framework. Bietet eingebaute Authentifizierung, Admin-Interface und klare Projektstruktur für schnelle Entwicklung und Skalierbarkeit.
- **Django REST Framework (DRF) 3.16.0**: Erweiterung zur einfachen Erstellung von RESTful APIs. Bietet Serializers, ViewSets, Pagination und integrierte Validierung.
- **djangorestframework_simplejwt 5.5.0**: JWT-basierte Authentifizierung für APIs. Ermöglicht sichere Token-Mechanismen, wichtig für Mobile- und externe Clients.
- **django-allauth 65.7.0**: Social Authentication (z.B. Discord OAuth). Erleichtert Registrieren und Anbinden externer OAuth-Provider.
- **dj-rest-auth 7.0.1**: REST-API-basierte Authendpoints unter Nutzung von django-allauth und SimpleJWT. Spart Zeit bei Login, Logout, Passwort-Reset etc.
- **dj-database-url 2.3.0**: Datenbank-Konfiguration aus Umgebungsvariablen (DATABASE_URL). Erleichtert Deployment auf Plattformen wie Heroku, da URL-basiert.
- **python-dotenv 1.1.0**: Lädt Umgebungsvariablen aus `.env`. Unterstützt lokale Entwicklung, verhindert Hardcodierung sensibler Daten.
- **psycopg2-binary 2.9.10**: PostgreSQL-Adapter für Python. Standard für Django-PostgreSQL-Integration.
- **PostgreSQL**: Leistungsfähiges, zuverlässiges relationales DBMS. Unterstützt JSONB, erweiterte Abfragen, gute Skalierbarkeit.
- **django-cors-headers 4.7.0**: Erlaubt CORS-Konfiguration für sichere API-Aufrufe von Frontend-Clients (Web, Mobile).
- **django-debug-toolbar 4.3.0**: Werkzeug für Analyse und Debugging in Entwicklung, um Performance-Engpässe und SQL-Abfragen zu überwachen.
- **django-extensions 3.2.3**: Zusätzliche Management-Befehle (Shell Plus, graph_models) für effizientere Entwicklung und Debugging.
- **drf-spectacular 0.27.1**: Automatische OpenAPI-Schema-Generierung für DRF. Erzeugt Swagger/Redoc-Doku, erleichtert API-Verbrauch.
- **asgiref 3.8.1**: ASGI-Reference-Implementation für asynchrone Unterstützung in Django. Bereitet auf künftige asynchrone Views/Kanäle vor.
- **gunicorn 23.0.0**: WSGI-Server für Produktion. Bewährt, performant, einfache Integration z.B. auf Heroku.
- **whitenoise 6.9.0**: Liefert statische Dateien in Produktion ohne externes CDN. Einfach einzurichten und performant.
- **requests 2.32.3**: HTTP-Client für externe API-Interaktionen (z.B. Wearables-APIs). Weit verbreitet und zuverlässig.
- **PyJWT 2.9.0**: JWT-Handling-Bibliothek, in Kombination mit SimpleJWT für Token-Operationen.
- **jsonschema 4.23.0 & jsonschema-specifications 2024.10.1**: Validierung von JSON-Datenstrukturen, etwa bei Webhook-Validierung oder komplexen Payloads.
- **pillow 11.2.1**: Bildverarbeitung, falls Profilbilder hochgeladen und bearbeitet werden müssen.
- **PyYAML 6.0.2**: YAML-Verarbeitung, z.B. Konfigurationsdateien oder Data-Import/Export.
- **certifi 2025.1.31**, **charset-normalizer 3.4.1**, **idna 3.10**, **urllib3 2.4.0**: Komponenten für sichere HTTP-Kommunikation und aktuelle TLS-Zertifikate.
- **attrs 25.3.0**: Hilfsbibliothek für Klassen mit Validierung; wird von einigen Dependencies genutzt.
- **inflection 0.5.1**: Stringkonvertierungen (snake_case <-> CamelCase), nützlich bei Serializing/Deserializing.
- **packaging 24.2**: Versionsvergleiche und Packaging-Tasks.
- **referencing 0.36.2**: Bibliothek für komplexe Referenzen in Datenstrukturen, bereit für erweiterte Features.
- **rpds-py 0.24.0**: Persistente Datenstrukturen in Python, für effiziente unveränderliche Strukturen in künftigen Modulen.
- **sqlparse 0.5.3**: Wird von Django zur Formatierung von SQL in Shell/Debug-Toolbar genutzt.
- **typing_extensions 4.13.2**: Zusätzliche Typ-Hinweise für Kompatibilität mit neueren Python-Versionen.
- **tzdata 2025.2**: Zeitzonendaten für korrekte Zeitberechnungen und Scheduling.
- **uritemplate 4.1.1**: Unterstützung für URI-Template-Manipulation, nützlich bei URL-Generierung oder Validierung.
- **wheel 0.45.1 & setuptools 78.1.0**: Packaging-Tools, um Releases zu bauen und zu verteilen.
- **Heroku**: Einfaches Deployment mit automatischem Scaling, ideal für MVP und frühe Tests.
- **GitHub Actions / CI (optional)**: Automatisierung von Tests, Linting und Deployment-Pipelines.
- **Docker (optional)**: Containerisierung für konsistente Entwicklungs- und Produktionsumgebungen.

**Begründung der Auswahl**  
- Etablierte, gut gewartete Bibliotheken gewährleisten Wartbarkeit und Sicherheit.  
- Django & DRF: schnelle Entwicklung, klare Architektur, eingebaute Features (Auth, Admin).  
- JWT & OAuth: flexible Authentifizierungsmechanismen für Discord-Integration und mobile/externe Clients.  
- Tools wie drf-spectacular und django-debug-toolbar unterstützen Dokumentation und Debugging, beschleunigen Entwicklung.  
- Deployment-Tools (Gunicorn, Whitenoise, dj-database-url, Heroku) ermöglichen reibungslosen Produktionsbetrieb.  
- Zusätzliche Bibliotheken (requests, pillow, PyYAML) decken häufige Anwendungsfälle (Externe APIs, Bildverarbeitung, Konfigmanagement).  
- Python 3.13: moderne Sprachfeatures, Performance-Verbesserungen.  
- CORS, TZ-Daten und Typing-Extensions sichern robuste API-Kommunikation und korrekte Zeit-/Typbehandlung.  
- Persistente Datenstrukturen und Referencing-Bibliotheken ermöglichen künftige Erweiterungen ohne großen Refactoring-Aufwand.  

## 🚀 Setup & Installation
### 1️⃣ Repository klonen
```bash
git clone https://github.com/DEIN_GITHUB_ACCOUNT/igoultra-backend.git
cd igoultra-backend
```
### 2️⃣ Virtuelle Umgebung aktivieren
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```
### 3️⃣ Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```
### 4️⃣ Datenbankmigrationen
```bash
python manage.py migrate
```
### 5️⃣ Superuser erstellen
```bash
python manage.py createsuperuser
```
### 6️⃣ Server starten
```bash
python manage.py runserver
```

## 🗂 Projektstruktur
```plaintext
igoultra-backend/
 ├── igoultra/               # Django Hauptprojekt
 │   ├── settings.py         # Einstellungen
 │   ├── urls.py             # URL-Routing
 │   ├── wsgi.py             # WSGI-Einstiegspunkt
 │   └── ...
 ├── xp_system/              # XP-System App
 │   ├── models.py           # Datenmodelle
 │   ├── views.py            # API-Logik
 │   ├── serializers.py      # DRF-Serializer
 │   ├── urls.py             # Routen
 │   └── ...
 ├── manage.py
 ├── requirements.txt
 └── README.md
```

## 🗃 Datenbankmodelle
### User
Standard Django-User + optional Discord-ID.

### Season
```python
class Season(models.Model):
    name = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField()
    is_active = models.BooleanField(default=False)
```

### SeasonXp
```python
class SeasonXp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    xp = models.IntegerField()
```

## 🔌 API Endpunkte
| Endpoint                     | Methode | Beschreibung                    |
|------------------------------|---------|---------------------------------|
| `/api/v1/auth/jwt/create/`   | POST    | Login (JWT)                     |
| `/api/v1/auth/jwt/refresh/`  | POST    | Token erneuern                  |
| `/api/v1/xp/submit/`         | POST    | XP einreichen                   |
| `/api/v1/xp/leaderboard/`    | GET     | Rangliste anzeigen              |

### Beispiel: XP Submit
```http
POST /api/v1/xp/submit/
Content-Type: application/json
Authorization: Bearer <TOKEN>

{
  "activity": "pushups",
  "amount": 50
}
```
Antwort:
```json
{
  "message": "XP submitted successfully",
  "total_xp": 500
}
```

## ✅ Testing
### Lokale Tests starten
```bash
python manage.py test
```
### Beispiel-Test (xp_system/tests.py)
```python
def test_xp_submission(self):
    response = self.client.post('/api/v1/xp/submit/', {
        'activity': 'pushups',
        'amount': 10
    }, HTTP_AUTHORIZATION=f'Bearer {self.token}')
    self.assertEqual(response.status_code, 200)
```

## ☁ Deployment
Heroku Deployment:
```bash
heroku login
heroku create igoultra-backend
git push heroku main
heroku run python manage.py migrate
```
Domain: https://api.igoultra.de

## ✨ Coding Standards
- Kommentare in Englisch
- PEP8-konform
- API-Endpoints versioniert (`/api/v1/`)
- Modularer Code (pro App ein Bereich)
- DRY-Prinzip (Don't Repeat Yourself)

## 🤝 Contributing
1. Forke das Repo  
2. Erstelle einen Branch `feature/DEIN_FEATURE`  
3. Push Änderungen  
4. Stelle einen Pull Request  

## 🧭 Weiterführende Ressourcen
- [Django Docs](https://docs.djangoproject.com/)
- [DRF Docs](https://www.django-rest-framework.org/)
- [Heroku Django Guide](https://devcenter.heroku.com/categories/python-support)

## 📌 Hinweis
Dieses Backend ist Teil des iGoUltra-Universums. Für Frontend, AR/VR oder Discord-Integration siehe separate Repositories.
