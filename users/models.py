from django.db import models
from django.core.validators import MinValueValidator


class User(models.Model):
    age = models.IntegerField(
        validators=[MinValueValidator(16, message="L'âge doit être supérieur à 15 ans.")]
    )
    consentement = models.BooleanField(default=False)

    
