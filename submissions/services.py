import os
import requests
from django.conf import settings
from submissions.models import Submission
from .pdf_utils import extract_text_from_pdf, clean_extracted_text


def call_ollama_api(prompt):
    """Appelle l'API Ollama pour l'analyse de réponse."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-coder",
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.2}
            },
            timeout=530
        )
        return response.json()
    except Exception as e:
        print(f"Erreur API Ollama: {str(e)}")
        return None


def parse_ai_response(response_text):
    """Extrait la note et le feedback de la réponse de l'IA."""
    try:
        # Logique d'analyse basique (à améliorer)
        grade = 10.0  # Valeur par défaut
        if "/20" in response_text:
            grade_part = response_text.split("/20")[0][-2:]
            grade = float(grade_part.strip())

        feedback = response_text[:2000]  # Limite la longueur
        return grade, feedback
    except:
        return 0.0, "Erreur d'analyse de la réponse"


def evaluate_submission(submission_id):
    """Fonction principale d'évaluation."""
    try:
        submission = Submission.objects.get(id=submission_id)

        # Chemins des fichiers
        answer_path = os.path.join(settings.MEDIA_ROOT, submission.answer_file.name)
        correction_path = os.path.join(settings.MEDIA_ROOT, submission.exercise.correction_file.name)

        # Extraction des textes avec nettoyage
        student_answer = clean_extracted_text(extract_text_from_pdf(answer_path))
        correction_text = clean_extracted_text(extract_text_from_pdf(correction_path))

        # Construction du prompt
        prompt = f"""  
        [ROLE] Correcteur automatique d'exercices SQL        [CORRECTION OFFICIELLE] {correction_text}  
        [RÉPONSE ÉTUDIANT] {student_answer}  
        [TÂCHE] Donnez :        - Une note sur 20 avec justification        - Les erreurs techniques détectées        - Des conseils d'amélioration        """

        # Appel à l'IA
        ai_response = call_ollama_api(prompt)

        if ai_response and 'response' in ai_response:
            grade, feedback = parse_ai_response(ai_response['response'])
        else:
            grade, feedback = 0.0, "Échec de l'analyse par l'IA"

        # Mise à jour de la soumission
        Submission.objects.filter(id=submission_id).update(
            grade=grade,
            feedback=feedback
        )

    except Exception as e:
        print(f"ERREUR CRITIQUE dans evaluate_submission: {str(e)}")
        Submission.objects.filter(id=submission_id).update(
            feedback=f"Erreur système: {str(e)[:200]}"
        )
