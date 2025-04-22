import openai
import os
from dotenv import load_dotenv

# Charger les variables du fichier .env
load_dotenv()

# Lire la clé API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def read_scraped_posts(file_path="scraped_posts.txt"):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return content.strip() if content else None

def summarize_text_with_ai(text, max_tokens=600):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant qui résume des publications LinkedIn pour un utilisateur."},
                {"role": "user", "content": f"Voici des publications LinkedIn. Résume-les de manière claire, avec des points-clés et en français :\n\n{text}"}
            ],
            max_tokens=max_tokens,
            temperature=0.5,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Erreur lors du résumé : {e}"

def analyze_posts():
    posts = read_scraped_posts()
    if not posts:
        return "Aucun contenu à résumer. Veuillez scraper des posts d'abord."
    return summarize_text_with_ai(posts)
