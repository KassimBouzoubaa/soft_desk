from rest_framework.permissions import BasePermission
from .models import Contributor


class IsContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur actuel est un contributeur du projet
        return obj.contributors.filter(user=request.user).exists()


class IsAuthorOrReadOnly(BasePermission):
    """
    Permission to allow only the author of the project to modify or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Autoriser les requêtes GET, HEAD ou OPTIONS.
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Vérifier si l'utilisateur est l'auteur du projet.
        return obj.author == request.user


class IsContributorOfProject(BasePermission):
    """
    Permission personnalisée pour vérifier si l'utilisateur est un contributeur du projet.
    """

    def has_permission(self, request, view):
        project_id = request.data.get("project")
        if project_id:
            # Vérifier si l'utilisateur est un contributeur du projet
            return Contributor.objects.filter(
                project_id=project_id, user=request.user
            ).exists()
        return False
