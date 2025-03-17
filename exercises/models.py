# exercises/models.py
from django.db import models

class Exercise(models.Model):
    title = models.CharField(
        max_length=200,
        help_text="Titre de l'exercice"
    )
    description = models.TextField(
        help_text="Énoncé de l'exercice"
    )
    correction_file = models.FileField(
        upload_to='corrections/',
        help_text="PDF de correction"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date de création"
    )

    def __str__(self):
        return self.title