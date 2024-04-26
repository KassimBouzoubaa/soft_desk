from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Project, Contributor
from .serializers import ProjectRegistrationSerializer, ProjectDetailSerializer
from .permissions import IsContributor, IsAuthorOrReadOnly

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]


    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return ProjectRegistrationSerializer
        else:
            return ProjectDetailSerializer
    
    def perform_create(self, serializer):
        # Récupérer l'utilisateur actuellement authentifié
        user = self.request.user
        # Créer le projet en associant l'utilisateur comme auteur
        project_instance = serializer.save(author=user)
        # Créer une entrée dans la table Contributor pour associer l'utilisateur au projet en tant que contributeur
        Contributor.objects.create(user=user, project=project_instance)