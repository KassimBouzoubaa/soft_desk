from rest_framework.permissions import BasePermission
from .models import Contributor, Project, Issue, Comment


class IsContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Vérifier si l'utilisateur actuel est un contributeur du projet, de l'issue ou du commentaire
        if isinstance(obj, Project):
            # Vérifier si l'utilisateur est un contributeur du projet
            return obj.contributors.filter(user=request.user).exists()
        elif isinstance(obj, Issue):
            # Vérifier si l'utilisateur est un contributeur de l'issue
            return obj.project.contributors.filter(user=request.user).exists()
        elif isinstance(obj, Comment):
            # Vérifier si l'utilisateur est un contributeur du projet associé au commentaire
            return obj.issue.project.contributors.filter(user=request.user).exists()
        return False

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
