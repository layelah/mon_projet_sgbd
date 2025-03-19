from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('teacher', 'Professeur'),
        ('student', 'Étudiant'),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLES,
        help_text="Rôle de l'utilisateur (professeur ou étudiant)"
    )

    def __str__(self):
        return self.username