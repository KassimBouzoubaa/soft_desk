from rest_framework import serializers
from .models import Project, Contributor, Issue
from users.serializers import UserDetailSerializer


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["user", "project", "created_time"]


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
