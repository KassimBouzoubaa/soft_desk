from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet

# Créer un routeur et enregistrer la vue UserViewSet
router = DefaultRouter()
router.register(r'projects', ProjectViewSet)

urlpatterns = router.urls
