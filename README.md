# CalendarAI

## Local setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Useful commands
- Health check endpoint: `http://127.0.0.1:8000/api/health/`
- Seed onboarding categories for a user:
  ```bash
  python manage.py seed_onboarding <user_id>
  ```

## Quick API smoke tests
```bash
curl http://127.0.0.1:8000/api/health/
curl http://127.0.0.1:8000/api/onboarding/status/
curl http://127.0.0.1:8000/api/categories/
```
