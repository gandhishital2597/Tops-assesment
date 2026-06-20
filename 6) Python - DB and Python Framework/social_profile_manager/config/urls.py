"""
Root URL configuration for the Social Profile Manager project.

This keeps things clean (Section C, Task 4: Clean URL Routing) by
delegating all "/profiles/..." routes to the profiles app's own urls.py
via include(), rather than defining every view route here.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profiles/', include('profiles.urls')),
]
