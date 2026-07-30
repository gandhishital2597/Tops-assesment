# Doctor Finder REST API — Setup & Testing Guide
### (Covers Section B: Practical Tasks + Section C: Mini Project — combined)

## Why Sections B and C are combined

Section C's "Mini Project" requirements are not a new build — they're Section B's
same model, same `ModelViewSet`, same atomic-transaction pattern, with two specific
upgrades layered on top:

| Requirement | Section B asked for | Section C asked for | What this code does |
|---|---|---|---|
| Model + CRUD | `Doctor` model + `ModelViewSet` + `DefaultRouter` | Same | One model, one viewset |
| Pagination | "Choose `PageNumberPagination` **or** `LimitOffsetPagination`" | Specifically `LimitOffsetPagination` | Project default = `PageNumberPagination`; this viewset overrides it with `LimitOffsetPagination`, satisfying both the open choice in B and the specific requirement in C |
| Ordering | Not required | `OrderingFilter` (`?ordering=-name`) | Added once, used everywhere |
| Atomic transactions | On `create` only | On any "profile update" too | `perform_create` **and** `perform_update` both wrapped in `transaction.atomic()` |
| Browsable API / Postman | Postman testing | DRF Browsable API | Both work out of the box — DRF ships the Browsable API by default, no extra code needed |

Writing this as two separate projects would mean duplicating the model/serializer/
viewset and then immediately overriding Section B's pagination choice with
Section C's — so one project that satisfies the union of both requirements is the
more honest deliverable.

## Project structure

```
doctor_finder_api/
├── config/
│   ├── urls.py                 # project-level urls (already wired to doctor_finder app)
│   └── settings_additions.py   # block to merge into your generated settings.py
└── doctor_finder/
    ├── models.py                # Section B.1
    ├── serializers.py           # Section A.2 demo + validation
    ├── views.py                 # Section B.2/3/4, Section C.2/3
    └── doctor_urls.py            # Section B.2 (DefaultRouter)
```

## Setup from scratch

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install django djangorestframework

# 3. Start a Django project (skip if you already have one)
django-admin startproject config .
python manage.py startapp doctor_finder

# 4. Copy in the files from this delivery:
#    - doctor_finder/models.py
#    - doctor_finder/serializers.py
#    - doctor_finder/views.py
#    - doctor_finder/doctor_urls.py   (app-level routes — see note below)
#    - merge config/settings_additions.py into config/settings.py
#    - replace config/urls.py with the one provided (project-level root router)
#
# Note: Django normally names BOTH the project-level and app-level files
# "urls.py" by convention (it's two different layers: project root vs. app).
# We renamed the app-level one to doctor_urls.py here just so the two files
# aren't identically named when browsing the folder. If you've worked with
# Django before and prefer the standard convention, it's safe to rename it
# back to urls.py and update the include() in config/urls.py to match.

# 5. Migrations (Section B.1)
python manage.py makemigrations doctor_finder
python manage.py migrate

# 6. Create a superuser (optional, for /admin/)
python manage.py createsuperuser

# 7. Run the server
python manage.py runserver
```

API base URL: `http://127.0.0.1:8000/api/doctors/`

## Postman / Browsable API verification (Section B.5 / C.4)

### 1. Create a doctor (POST) — expect `201 Created`
- **Method:** POST
- **URL:** `http://127.0.0.1:8000/api/doctors/`
- **Body (raw, JSON):**
```json
{
    "name": "Anjali Mehta",
    "specialization": "Cardiology",
    "city": "Vadodara"
}
```
- **Expected response:** `201 Created` with the new doctor's JSON, including its assigned `id`.

### 2. List doctors with pagination (GET)
- **URL:** `http://127.0.0.1:8000/api/doctors/?limit=5&offset=0`
- **Expected response:** `200 OK` with a body shaped like:
```json
{
    "count": 12,
    "next": "http://127.0.0.1:8000/api/doctors/?limit=5&offset=5",
    "previous": null,
    "results": [ ... 5 doctor objects ... ]
}
```

### 3. Ordering (Section C.2)
- **URL:** `http://127.0.0.1:8000/api/doctors/?ordering=-name`
- Returns doctors sorted by name, descending. Try `?ordering=specialization` for ascending by specialization.

### 4. Validation failure (confirms Section A.2 / serializer validation)
- **POST body:**
```json
{
    "name": "Dr123",
    "specialization": "Witchcraft",
    "city": "X"
}
```
- **Expected response:** `400 Bad Request` with field-specific error messages for `name`, `specialization`, and `city`.

### 5. Update a doctor (PUT/PATCH) — confirms atomic transaction path
- **URL:** `http://127.0.0.1:8000/api/doctors/1/`
- **Method:** PATCH
- **Body:** `{ "city": "Ahmedabad" }`
- **Expected response:** `200 OK` with the updated record.

### 6. Delete a doctor (DELETE)
- **URL:** `http://127.0.0.1:8000/api/doctors/1/`
- **Expected response:** `204 No Content`

### 7. Browsable API (Section C.4)
Just open `http://127.0.0.1:8000/api/doctors/` directly in a browser (not Postman) —
DRF renders an interactive HTML form for GET/POST testing automatically, no extra
setup required.
