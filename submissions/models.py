# submissions/models.py
from django.db import models
from django.utils import timezone
from exercises.models import Exercise


class Submission(models.Model):
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    student_name = models.CharField(
        max_length=100,
        help_text="Nom de l'étudiant (temporaire)"
    )
    answer_file = models.FileField(
        upload_to='submissions/',
        help_text="PDF de la réponse étudiante"
    )
    grade = models.FloatField(
        null=True,
        blank=True,
        help_text="Note sur 20"
    )
    feedback = models.TextField(
        null=True,
        blank=True,
        help_text="Feedback détaillé"
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date de soumission"
    )

    def __str__(self):
        return f"{self.student_name} - {self.exercise.title}"

    def save(self, *args, **kwargs):
        if self._state.adding:
            super().save(*args, **kwargs)
            from .tasks import evaluate_submission_task
            evaluate_submission_task.delay(self.id)  # <-- Appel asynchrone
        else:
            super().save(*args, **kwargs)