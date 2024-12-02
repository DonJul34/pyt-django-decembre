import requests
import json
import random
from django.conf import settings
from django.http import JsonResponse


# Liste de prompts prédéfinis
predefined_prompts = [
    "A beautiful sunset over the ocean.",
    "A forest filled with whispers of ancient trees.",
    "A lonely star in the midnight sky.",
    "A flower blooming in the spring rain.",
    "The sound of waves crashing on a rocky shore.",
    "A dream that dances in the quiet night.",
    "The morning dew on a spider's web."
]

# Vue pour générer du texte
def generate_poem(request):
    if request.method == 'GET':  # Traite uniquement les requêtes GET
        # Sélectionne un prompt aléatoire
        prompt = random.choice(predefined_prompts)

        # Contenu du prompt envoyé à OpenAI
        prompt_content = f"""
        You are a poet. Please create a beautiful, creative poem based on the following prompt:

        {prompt}
        """

        # Configuration de la requête API
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}"
        }

        data = {
            "model": "gpt-4",  # Modèle utilisé
            "messages": [
                {"role": "system", "content": "You are a poet."},
                {"role": "user", "content": prompt_content.strip()}
            ],
            "max_tokens": 150,  # Limite de longueur pour un poème court
            "temperature": 0.7,  # Paramètre de créativité
        }

        try:
            # Envoi de la requête POST à OpenAI
            response = requests.post(url, headers=headers, data=json.dumps(data), timeout=120)
            response.raise_for_status()  # Déclenche une exception si la réponse est invalide

            # Lecture de la réponse JSON
            response_json = response.json()
            poem_text = response_json['choices'][0]['message']['content'].strip()


            # Retourne le poème dans une réponse JSON
            return JsonResponse({'poem': poem_text})

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f"Request error: {e}"}, status=500)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f"JSON decode error: {e}"}, status=500)
        except Exception as e:
            return JsonResponse({'error': f"Unexpected error: {e}"}, status=500)

    # Si la méthode n'est pas GET, retourne une erreur
    return JsonResponse({'error': 'Invalid request method. Please use GET.'}, status=400)
