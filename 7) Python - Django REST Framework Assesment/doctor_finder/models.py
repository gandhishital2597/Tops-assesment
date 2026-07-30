from django.db import models


class Doctor(models.Model):
    """
    Section B.1 — Doctor Model Definition
    Fields required: name, specialization, city (all CharField)
    """
    name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']  # default ordering; overridable via ?ordering= (Section C.2)

    def __str__(self):
        return f"{self.name} ({self.specialization}, {self.city})"
