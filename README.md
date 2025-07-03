# iGoUltra Backend

Das iGoUltra-Backend bildet die serverseitige Grundlage des gesamten iGoUltra-Ökosystems. Es stellt REST-APIs bereit, die von Web‑Frontend, mobilen Apps, AR/VR‑Anwendungen und dem Discord‑Bot genutzt werden.

## 🚀 Vision
Das Projekt verfolgt das Ziel, Bewegung spielerisch zu fördern und virtuelle sowie reale Fitness miteinander zu verbinden. Ein zentrales Backend ermöglicht plattformübergreifende Ranglisten, Seasons und zukünftig auch eine eigene Währung.

## 📖 Inhaltsverzeichnis
- [Features](#features)
- [Technologie-Stack](#technologie-stack)
- [Quickstart](#quickstart)
- [Projektstruktur](#projektstruktur)
- [Datenmodelle](#datenmodelle)
- [API-Übersicht](#api-%C3%BCbersicht)
- [Testing](#testing)
- [Deployment](#deployment)
- [Coding Standards](#coding-standards)
- [Contributing](#contributing)
- [Ressourcen](#ressourcen)
- [Hinweis](#hinweis)

## ✨ Features
- Discord OAuth und JWT‑Authentifizierung
- XP- und Levelsystem inklusive saisonbasierter Rankings
- Layer-abhängige Leaderboards (Real/Cyber)
- Erweiterbare Architektur für künftige Module wie Bitgold, Wallet oder Skills

## 🛠 Technologie-Stack
Die wichtigsten Komponenten:
- **Python 3.13** und **Django 5.2** mit **Django REST Framework**
- **PostgreSQL** als Datenbank über `psycopg2-binary`
- `dj-rest-auth`, `django-allauth` und `djangorestframework_simplejwt` für Authentifizierung
- CORS-, Debug- und Extension-Tools wie `django-cors-headers`, `django-debug-toolbar` und `django-extensions`
- Deployment-Helfer `gunicorn`, `whitenoise` sowie `dj-database-url`

## ⚡ Quickstart
1. Repository klonen
   ```bash
   git clone https://github.com/DEIN_GITHUB_ACCOUNT/igoultra-backend.git
   cd igoultra-backend
   ```
2. Virtuelle Umgebung erstellen und aktivieren
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Abhängigkeiten installieren und Migrationen durchführen
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   ```
4. Superuser anlegen und Server starten
   ```bash
   python manage.py createsuperuser
   python manage.py runserver
   ```

## 🗂 Projektstruktur
```plaintext
igoultra-backend/
 ├── api/              # Versionierte API (aktuell v1)
 ├── users/            # Benutzer und Authentifizierung
 ├── xp/               # XP-System (Modelle, Services)
 ├── seasons/          # Saisonverwaltung
 ├── rankings/         # Leaderboards nach Layer
 ├── ultrabackend/     # Django-Haupteinstellungen
 ├── bitgold/          # Platzhalter für künftige Währung
 ├── wallet/           # Platzhalter für Wallet-Funktionen
 ├── inventory/        # Platzhalter für Items
 ├── store/            # geplanter Ingame-Store
 ├── skills/           # noch leere App für Skills
 ├── community_rang/   # Community-Ranglisten (geplant)
 ├── stats/            # Statistiken (geplant)
 └── manage.py, requirements.txt, ...
```

### App-Übersicht mit Codebeispielen

**API (`api/v1`)**

```python
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
        stats = get_xp_stats(request.user)
        return Response({
            'awarded_xp': result['awarded_xp'],
            'total_xp': stats['total_xp'],
            'level': stats['level'],
        })
```

**Users**

```python
class User(AbstractUser):
    discord_id = models.CharField(max_length=64, unique=True, null=True, blank=True)
    ultra_name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
```

**XP-Services**

```python
@transaction.atomic
def add_xp_to_user(user, type_key, amount_units, layer_type="Real-Life", metadata=None):
    xp_type = XpType.objects.get(key=type_key)
    real_xp = int(amount_units * xp_type.xp_amount)
    XpEvent.objects.create(user=user, amount=real_xp, source=type_key, layer_type=layer_type, metadata=metadata or {})
    user.xp = max(0, user.xp + real_xp)
    user.level = level_from_xp(user.xp)
    user.save(update_fields=['xp', 'level'])
    return get_xp_stats(user)
```

**Seasons**

```python
class Season(models.Model):
    name = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField()
    is_active = models.BooleanField(default=False)
```

**Rankings**

```python
def process_season_end(season_id: int):
    season = Season.objects.get(id=season_id)
    sxps = list(SeasonXp.objects.filter(season=season).select_related("user").order_by("-xp"))
    for pos, sxp in enumerate(sxps):
        p = pos / len(sxps)
        new_real = _adjust_layer(sxp.user.real_layer, REAL_LAYERS, p)
        LayerRankingEntry.objects.create(season=season, user=sxp.user, real_layer=new_real, xp=sxp.xp)
```

## 🗃 Datenmodelle
Beispiel einer Season und dazugehöriger XP-Zuordnung:
```python
class Season(models.Model):
    name = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField()
    is_active = models.BooleanField(default=False)

class SeasonXp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    xp = models.IntegerField()
```

## 📡 API-Übersicht
| Endpoint                       | Methode | Beschreibung          |
|--------------------------------|---------|-----------------------|
| `/api/v1/auth/jwt/create/`     | POST    | Login via JWT         |
| `/api/v1/auth/jwt/refresh/`    | POST    | Token erneuern        |
| `/api/v1/xp/submit/`           | POST    | XP einreichen         |
| `/api/v1/xp/leaderboard/`      | GET     | Rangliste abrufen     |

## ✅ Testing
Lokale Tests ausführen:
```bash
python manage.py test
```

## ☁ Deployment
Standard-Deployment auf Heroku:
```bash
heroku login
heroku create igoultra-backend
git push heroku main
heroku run python manage.py migrate
```

## ✨ Coding Standards
- Kommentare in Englisch, Code PEP8-konform
- API-Versionierung über `/api/v1/`
- Modularer Aufbau pro App

## 🤝 Contributing
1. Forke das Repo
2. Erstelle einen Branch `feature/DEIN_FEATURE`
3. Push deine Änderungen
4. Stelle einen Pull Request

## 📚 Ressourcen
- [Django Docs](https://docs.djangoproject.com/)
- [DRF Docs](https://www.django-rest-framework.org/)
- [Heroku Django Guide](https://devcenter.heroku.com/categories/python-support)

## Hinweis
Dieses Backend ist Teil des iGoUltra-Universums. Für Frontend oder Discord-Integration existieren separate Repositories.
