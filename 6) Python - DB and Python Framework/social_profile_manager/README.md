# Social Profile Manager
### TOPS Technologies Assessment — DB and Python Framework (Django)

A Django web application implementing the full assessment: profile creation
via ModelForms, validation, relational persistence, DTL rendering, and CSV
export using a context manager.

---

## Project Structure

```
social_profile_manager/
├── manage.py
├── requirements.txt
├── Section_A_Conceptual_Answers.md   ← Section A write-up
├── config/                            ← project-level settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── profiles/                          ← the app (Section B & C live here)
    ├── models.py        → Section B, Task 1: UserProfile model
    ├── forms.py          → Section B, Task 2: UserProfileForm + clean_age()
    ├── views.py          → Section B, Tasks 3–4 / Section C, Tasks 1–3
    ├── urls.py           → Section C, Task 4: clean URL routing
    ├── admin.py          → registers UserProfile with Django admin
    ├── tests.py          → basic test coverage for model/form/views
    ├── migrations/
    │   └── 0001_initial.py
    └── templates/profiles/
        ├── base.html
        ├── profile_list.html   → Section B, Task 4 + Section A Q4 (conditional visibility)
        └── profile_form.html
```

---

## Setup Instructions

### 1. Create a virtual environment & install dependencies
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure the database

The project is set up for **PostgreSQL** by default (`config/settings.py`).
Create the database first:
```sql
CREATE DATABASE social_profile_db;
```
Update the `USER` / `PASSWORD` in `config/settings.py` to match your local
Postgres credentials.

**Quick alternative (no DB server needed):** open `config/settings.py` and
swap the `DATABASES` block to the commented-out SQLite option — useful for
quickly testing the app without installing Postgres/MySQL.

### 3. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. (Optional) Create an admin user
```bash
python manage.py createsuperuser
```

### 5. Run the development server
```bash
python manage.py runserver
```

---

## Using the App

| Action | URL |
|---|---|
| View all profiles | `/profiles/` |
| Create a new profile | `/profiles/create/` |
| Edit a profile | `/profiles/<id>/edit/` |
| Export all profiles to CSV | `/profiles/export/` |
| Django admin | `/admin/` |

---

## Running Tests
```bash
python manage.py test
```
Covers: model creation, form validation (age ≤ 13 rejection, blank username
rejection), the list view, the create view persisting to the DB, and the
CSV export returning the correct content type.

---

## How Each Assessment Requirement Maps to the Code

| Requirement | Where |
|---|---|
| `UserProfile` model with CharField/IntegerField/BooleanField | `profiles/models.py` |
| `UserProfileForm` (ModelForm) with `clean_age()` | `profiles/forms.py` |
| View handling POST + `form.is_valid()` + `form.save()` | `profiles/views.py` → `profile_create` |
| `UserProfile.objects.all()` rendered via DTL `{% for %}` | `profiles/views.py` → `profile_list`, `profiles/templates/profiles/profile_list.html` |
| Conditional DTL logic toggling visibility | `profile_list.html` (`{% if profile.is_public %}`) |
| PostgreSQL/MySQL relational integration | `config/settings.py` `DATABASES` |
| CSV export using `with open(...) as file:` | `profiles/views.py` → `profile_export_csv` |
| Clean URL routing (List/Create/Export) | `profiles/urls.py`, included from `config/urls.py` |
