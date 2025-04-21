from openai import OpenAI
from dotenv import load_dotenv
import os

# 📥 Charger la clé API depuis le fichier .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🧠 Fonction principale pour analyser un post LinkedIn
def analyze_post(post):
    prompt = f"""
Tu es un assistant intelligent chargé d'analyser des publications LinkedIn professionnelles.

Voici un post :
\"\"\"{post["text"]}\"\"\"

Ta mission est de :
1. Classer le post dans **UNE SEULE** des catégories suivantes :

🔹 Offre d’emploi :
→ Le post propose un poste salarié (CDI, CDD, alternance, stage, VIE)
→ Il peut mentionner un recrutement, une embauche, un lien vers une offre, un besoin d'équipe
→ Mots-clés fréquents : « nous recrutons », « recherche un(e) », « rejoignez-nous », « hiring »

🔹 Mission freelance :
→ Le post propose une mission temporaire pour un freelance, consultant ou prestataire externe (hors CDI/CDD)
→ Cela inclut les appels à freelance, auto-entrepreneurs, missions en régie, portage salarial, prestations ponctuelles
→ Même si le post utilise les mots « recrute » ou « nous cherchons », vérifie s’il s’agit bien d’un contrat **freelance et non salarié**
→ Mots-clés : mission freelance, indépendant, prestation, portage, régie, facturation, disponibilité, TJM, SSII, ESN
→ ❗ Si c’est une **offre de prestation avec date de démarrage, durée, et lieu**, c’est une mission freelance

🔹 Événement :
→ Le post annonce un événement à venir ou passé, en ligne ou en présentiel
→ Cela inclut webinaires, conférences, salons, workshops, lives, sessions de networking, meetups, bootcamps
→ Peut contenir une date, un lien d’inscription ou un visuel d’événement

🔹 Article pertinent :
→ Le post partage un contenu à forte valeur ajoutée, souvent écrit ou relayé
→ Cela inclut articles de blog, études, infographies, analyses, threads éducatifs, conseils professionnels, retours d’expérience
→ Souvent formulé sous forme de storytelling, d’analyse, de top 5, de témoignage ou de recommandation

🔹 Autre (inutile) :
→ Le post est personnel, promotionnel, vague ou hors-sujet
→ Cela inclut les posts auto-promo, vœux, citations inspirantes, remerciements sans opportunité, photos sans contenu pro clair, réactions sans informations concrètes

2. Résumer le contenu du post en **une seule phrase claire**, informative et utile pour un lecteur qui ne clique pas sur le lien.

Ta réponse doit suivre ce format, sans rien ajouter d’autre :
Catégorie : <catégorie choisie>
Résumé : <phrase claire et informative>

⚠️ Ne commence jamais le résumé par le nom de l’auteur
⚠️ Ne répète pas le texte tel quel
⚠️ Sois factuel, professionnel, et synthétique
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un assistant qui classe et résume des posts LinkedIn pour un résumé quotidien par email."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()

# ✨ Fonction pour enrichir des mots-clés
def enrich_keywords(input_keywords: str) -> list:
    prompt = f"""
Tu es un assistant intelligent.

L'utilisateur a saisi les mots-clés suivants pour cibler les bons posts LinkedIn :
\"\"\"{input_keywords}\"\"\"

Ta mission est de :
1. Comprendre le sens général de ces mots
2. Générer une liste enrichie de mots-clés proches, liés ou équivalents, incluant :
   - Synonymes
   - Sigles
   - Expressions connexes
   - Métiers, outils, secteurs associés
3. Retourner uniquement la liste des mots-clés enrichis, séparés par des virgules, sans phrase ni explication.

Exemples :
Entrée : freelance → Sortie : freelance, indépendant, mission, prestation, consultant, TJM
Entrée : IA → Sortie : intelligence artificielle, IA, machine learning, deep learning, GPT, LLM
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu enrichis une liste de mots-clés pour filtrer intelligemment les posts LinkedIn."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    raw = response.choices[0].message.content.strip()
    return [kw.strip().lower() for kw in raw.split(",") if kw.strip()]
