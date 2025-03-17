# submissions/pdf_utils.py
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
import logging
import os
import re

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_path):
    """Extrait le texte d'un PDF avec gestion d'erreurs avancée"""
    try:
        # Vérification préalable du fichier
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Fichier introuvable : {file_path}")

        if os.path.getsize(file_path) == 0:
            raise ValueError("Fichier PDF vide")

        text = []
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)

            # Vérification du PDF chiffré
            if reader.is_encrypted:
                reader.decrypt('')  # Tentative avec mot de passe vide

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    # Nettoyage basique du texte
                    cleaned_text = ' '.join(page_text.replace('\n', ' ').split())
                    text.append(cleaned_text)

        return ' '.join(text) if text else "Aucun texte extrait"

    except PdfReadError as e:
        logger.error(f"Erreur de lecture PDF : {str(e)}")
        return "Format PDF non supporté"
    except Exception as e:
        logger.error(f"Erreur générale : {str(e)}")
        return f"Erreur d'extraction : {str(e)}"

def clean_extracted_text(text):
    """Nettoyage avancé du texte extrait"""
    # Supprime les caractères non imprimables
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', ' ', text)
    # Réduit les espaces multiples
    text = re.sub(r'\s+', ' ', text)
    # Corrige les césures de mots
    text = re.sub(r'(\w+-\n\w+)', lambda m: m.group(1).replace('-\n', ''), text)
    return text.strip()
