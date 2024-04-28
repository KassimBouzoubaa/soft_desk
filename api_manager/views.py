from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Project, Contributor, Issue, Comment
from .serializers import (
    ProjectRegistrationSerializer,
    ProjectDetailSerializer,
    IssueRegistrationSerializer,
    IssueDetailSerializer,
    IssueListSerializer,
    CommentDetailSerializer,
    CommentListSerializer,
    CommentRegistrationSerializer,
)
from .permissions import IsContributor, IsAuthorOrReadOnly
from users.models import User


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
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


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return IssueRegistrationSerializer
        elif self.action == "list":
            return IssueListSerializer
        else:
            return IssueDetailSerializer

    def perform_create(self, serializer):
        user = self.request.user
        project_pk = self.kwargs["project_pk"]
        project = get_object_or_404(Project, pk=project_pk)

        # Récupérer les IDs des contributeurs fournis dans les données de la requête
        provided_contributors_ids = self.request.data.get("contributors", [])

        # Récupérer les instances de contributeurs correspondant aux IDs fournis
        provided_contributors = [
            get_object_or_404(Contributor, id=contributor_id, project=project)
            for contributor_id in provided_contributors_ids
        ]

        # Ajouter l'auteur comme contributeur s'il n'est pas déjà dans la liste des contributeurs fournis
        author_contributor = Contributor.objects.filter(
            user=user, project=project
        ).first()
        if author_contributor and author_contributor not in provided_contributors:
            provided_contributors.append(author_contributor)

        # Liste pour stocker les contributeurs validés
        validated_contributors = []

        # Vérifier si les contributeurs fournis appartiennent au projet et les ajouter à la liste des contributeurs validés
        for contributor in provided_contributors:
            if contributor in project.contributors.all():
                validated_contributors.append(contributor)

        # Enregistrer l'issue avec les contributeurs validés
        serializer.save(
            author=user, project=project, contributors=validated_contributors
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return CommentRegistrationSerializer
        elif self.action == "list":
            return CommentListSerializer
        else:
            return CommentDetailSerializer

    def perform_create(self, serializer):
        user = self.request.user

        issue_pk = self.kwargs["issue_pk"]
        issue = get_object_or_404(Issue, pk=issue_pk)

        # Enregistrer l'issue avec les contributeurs validés
        serializer.save(author=user, issue=issue)
