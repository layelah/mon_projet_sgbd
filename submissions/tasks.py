from celery.utils.log import get_task_logger
from celery import shared_task
from .services import evaluate_submission

logger = get_task_logger(__name__)

@shared_task(bind=True, autoretry_for=(Exception,), max_retries=3, retry_backoff=True)
def evaluate_submission_task(self, submission_id):
    try:
        logger.info(f"Début évaluation soumission {submission_id}")
        """Tâche Celery pour l'évaluation asynchrone"""
        evaluate_submission(submission_id)
        # ... code existant ...
        logger.info(f"Évaluation {submission_id} terminée")
    except Exception as e:
        logger.error(f"Échec tâche {submission_id}: {str(e)}")
        raise self.retry(exc=e)