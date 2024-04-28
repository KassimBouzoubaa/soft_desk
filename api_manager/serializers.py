from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment
from users.serializers import UserDetailSerializer


# ---- CONTRIBUTOR SERIALIZER ---- #
class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["user", "project", "created_time"]


# ---- PROJECT SERIALIZER ---- #


class ProjectRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["title", "description", "project_type"]


class ProjectDetailSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    contributors = ContributorSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "project_type",
            "created_time",
            "author",
            "contributors",
        ]


# ---- ISSUE SERIALIZER ---- #


class IssueRegistrationSerializer(serializers.ModelSerializer):
    contributors = serializers.PrimaryKeyRelatedField(
        queryset=Contributor.objects.all(), many=True
    )

    class Meta:
        model = Issue
        fields = [
            "title",
            "description",
            "statut",
            "priority",
            "balise",
            "contributors",
        ]


class IssueDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username")
    contributors = ContributorSerializer(many=True)
    project_id = serializers.PrimaryKeyRelatedField(source="project", read_only=True)

    class Meta:
        model = Issue
        fields = [
            "title",
            "description",
            "statut",
            "priority",
            "balise",
            "created_time",
            "author",
            "contributors",
            "project_id",
        ]


class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ["id", "title", "description", "statut", "priority", "balise"]


# ---- COMMENT SERIALIZER ---- #


class CommentListSerializer(serializers.ModelSerializer):
    id = serializers.CharField()

    class Meta:
        model = Comment
        fields = ["id", "description"]


class CommentDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username")
    # issue = serializers.HyperlinkedRelatedField(
    #        view_name='project-issue-detail',  # Nom de la vue pour récupérer les détails de l'issue
    #       lookup_field='pk"',  # Champ utilisé pour identifier l'issue (dans ce cas, l'ID de l'issue)
    #      read_only=True
    # )
    issue_id = serializers.PrimaryKeyRelatedField(source="issue", read_only=True)

    id = serializers.CharField()

    class Meta:
        model = Comment
        fields = ["id", "description", "created_time", "author", "issue_id"]


class CommentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "description",
        ]
