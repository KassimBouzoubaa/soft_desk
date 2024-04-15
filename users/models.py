from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    age = models.IntegerField(validators=[MinValueValidator(16, message="L'âge doit être supérieur à 15 ans.")])
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

