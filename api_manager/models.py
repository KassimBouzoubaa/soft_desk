from django.db import models
from users.models import User
import uuid


class Project(models.Model):
    TYPE_CHOICES = [
        ("front-end", "Front-end"),
        ("backend", "Backend"),
        ("iOS", "iOS"),
        ("android", "Android"),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    contributor = models.ManyToManyField("Contributor", related_name="projects")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    project_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="contributors"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "project")


class Issue(models.Model):
    BALISE_CHOICES = [
        ("bug", "BUG"),
        ("feature", "FEATURE"),
        ("task", "TASK"),
    ]

    PRIORITY_CHOICES = [
        ("low", "LOW"),
        ("medium", "MEDIUM"),
        ("high", "HIGH"),
    ]

    STATUT_CHOICES = [
        ("to_do", "To Do"),
        ("in_progress", "In Progress"),
        ("finished", "Finished"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="to_do")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    balise = models.CharField(max_length=20, choices=BALISE_CHOICES)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="authored_issues"
    )
    contributors = models.ManyToManyField(
        Contributor, related_name="contributed_issues"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issues"
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
