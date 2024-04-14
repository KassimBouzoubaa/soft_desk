from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# Créer un routeur et enregistrer la vue UserViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet)

# Inclure les URLs générées par le routeur
urlpatterns = router.urls
