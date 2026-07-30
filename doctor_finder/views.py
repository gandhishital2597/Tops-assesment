from django.db import transaction
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination

from .models import Doctor
from .serializers import DoctorSerializer


class DoctorLimitOffsetPagination(LimitOffsetPagination):
    """
    Section C.2 — LimitOffsetPagination lets clients pick the exact
    page size (?limit=) and starting point (?offset=).
    Example: /api/doctors/?limit=5&offset=10
    """
    default_limit = 10
    max_limit = 100


class DoctorViewSet(viewsets.ModelViewSet):
    """
    Section B.2 — ModelViewSet gives us list/retrieve/create/update/destroy
    for free. Combined with DefaultRouter (see urls.py) this auto-generates
    the standard GET/POST/PUT/PATCH/DELETE endpoints.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    # Section B.3 / C.2 — pagination + ordering
    pagination_class = DoctorLimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'name', 'specialization', 'city']
    ordering = ['id']  # default; client can override e.g. ?ordering=-name

    def perform_create(self, serializer):
        """
        Section B.4 / Section A.6 — Atomic transaction on create.
        Guarantees no partial/orphan rows are committed if anything
        downstream of save() fails.
        """
        with transaction.atomic():
            serializer.save()

    def perform_update(self, serializer):
        """
        Section C.3 — Atomic transaction on update as well, so a failed
        update rolls back completely rather than leaving a half-applied
        change in the database.
        """
        with transaction.atomic():
            serializer.save()
