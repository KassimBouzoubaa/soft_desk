from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, IssueViewSet
from django.urls import path

# Créer un routeur
router = DefaultRouter()
router.register(r"project", ProjectViewSet, basename="project")

# Définir les URL supplémentaires pour les issues liées aux projets
project_issues_urls = [
    path(
        "project/<int:project_pk>/issues/",
        IssueViewSet.as_view(
            {
                "get": "list",  # Pour la liste des issues d'un projet
                "post": "create",  # Pour la création d'une nouvelle issue dans un projet
            }
        ),
        name="project-issues-list",
    ),
    path(
        "project/<int:project_pk>/issues/<int:pk>/",
        IssueViewSet.as_view(
            {
            "get": "retrieve",  # Pour récupérer les détails d'une issue dans un projet
            "put": "update",    # Pour mettre à jour une issue dans un projet
            "patch": "partial_update",  # Vous pouvez également utiliser "patch" pour une mise à jour partielle
            "delete": "destroy",  # Pour supprimer une issue dans un projet

        }
        ),
        name="project-issue-detail",
    ),
]

# Combiner les URLs du routeur avec les URLs supplémentaires
urlpatterns = router.urls + project_issues_urls
