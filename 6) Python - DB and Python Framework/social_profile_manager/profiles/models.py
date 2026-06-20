"""
Section B - Task 1: Define UserProfile Model

A class inheriting from models.Model, with CharField for username,
IntegerField for age, and BooleanField for is_public status.

Why these typed fields matter (Section A, Q2): unlike a plain Python
attribute (which could silently hold any type — a string, an int, a list,
None), each Django field enforces both a Python-level type AND a matching
database column type (VARCHAR, INTEGER, BOOLEAN). That means bad data is
rejected before it ever reaches the database, and the schema itself
documents what every profile is allowed to contain.
"""

from django.db import models


class UserProfile(models.Model):
    username = models.CharField(
        max_length=50,
        unique=True,
        help_text="Public display name for the profile."
    )
    age = models.IntegerField(
        help_text="User's age in years. Must be 13 or older (see UserProfileForm.clean_age)."
    )
    is_public = models.BooleanField(
        default=True,
        help_text="If True, the profile is visible to everyone; if False, it is private."
    )
    bio = models.TextField(
        max_length=300,
        blank=True,
        help_text="Optional short bio shown on the profile page."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # newest profiles first

    def __str__(self):
        return self.username
