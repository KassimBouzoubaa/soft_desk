from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    age = models.IntegerField(
        validators=[
            MinValueValidator(16, message="L'âge doit être supérieur à 15 ans.")
        ],
        null=True,
        blank=True,  # Permet à l'âge d'être vide
    )
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.is_superuser:
            # Appliquer la validation de l'âge uniquement pour les utilisateurs normaux
            if self.age is None:
                raise ValueError("L'âge est requis pour les utilisateurs normaux.")
            if self.age < 16:
                raise ValueError("L'âge doit être supérieur à 15 ans.")
        super().save(*args, **kwargs)
