from rest_framework import permissions

class IsContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Vérifie si l'utilisateur actuel est un contributeur du projet
        return obj.contributors.filter(user=request.user).exists()
