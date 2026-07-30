from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet

# Section B.2 — DefaultRouter auto-generates:
#   GET    /doctors/        -> list
#   POST   /doctors/        -> create
#   GET    /doctors/{id}/   -> retrieve
#   PUT    /doctors/{id}/   -> update
#   PATCH  /doctors/{id}/   -> partial_update
#   DELETE /doctors/{id}/   -> destroy
router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')

urlpatterns = router.urls
