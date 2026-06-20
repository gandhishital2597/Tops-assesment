from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'age', 'is_public', 'created_at')
    list_filter = ('is_public',)
    search_fields = ('username',)
