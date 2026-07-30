# settings_additions.py
#
# This is NOT a full settings.py — it's the specific block you add to the
# settings.py that `django-admin startproject` already generated for you.
# Drop these into the matching sections of your real settings.py.

INSTALLED_APPS = [
    # ... Django's default apps stay as-is ...
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Add these two:
    'rest_framework',
    'doctor_finder',
]

# Section B.3 — Global pagination config.
# We set PageNumberPagination as the project-wide default (simple
# ?page=2 style navigation), and then override it locally to
# LimitOffsetPagination inside DoctorViewSet for Section C.2's
# requirement of ?limit= / ?offset= control.
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

    # Section C.2 — OrderingFilter as a default filter backend
    # (DoctorViewSet also declares it explicitly, but this makes it
    # available project-wide for any other viewset too).
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.OrderingFilter',
    ],

    # Section C.4 — Browsable API is DRF's default renderer set already;
    # listed here explicitly so it's not accidentally removed.
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}
