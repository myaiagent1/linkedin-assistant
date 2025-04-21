import streamlit as st
import subprocess
import threading
import time
import os
from scrape_linkedin import get_linkedin_posts
from analyze_posts import analyze_post, enrich_keywords
from send_email import send_email
from jinja2 import Template

# 🎨 Logo LinkedIn en haut de l’interface
st.set_page_config(page_title="Assistant LinkedIn IA", page_icon="🔗", layout="centered")
st.markdown("""
    <div style='text-align: center;'>
        <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' width='60'/>
        <h1 style='color:#0077B5;'>Assistant LinkedIn IA</h1>
    </div>
""", unsafe_allow_html=True)

# 📂 Lire les préférences utilisateur depuis le fichier créé par l'interface Streamlit
def read_user_config():
    try:
        with open("user_config.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]
            email = lines[0].split(":")[1].strip()
            raw_keywords = lines[1].split(":")[1].strip()
            categories = [cat.strip() for cat in lines[2].split(":")[1].split(",")]
            enrich_mode = lines[3].split(":")[1].strip().lower() == "true"
            return email, raw_keywords, categories, enrich_mode
    except FileNotFoundError:
        return "", "", [], False

# 📁 Enregistrer les nouvelles préférences utilisateur
def save_user_config(email, keywords, categories, enrich_mode):
    with open("user_config.txt", "w", encoding="utf-8") as f:
        f.write(f"Email: {email}\n")
        f.write(f"Mots-clés: {keywords}\n")
        f.write(f"Catégories: {', '.join(categories)}\n")
        f.write(f"Enrichissement: {str(enrich_mode)}\n")

# 🎛️ Barre latérale de configuration utilisateur
st.sidebar.title("⚙️ Paramètres utilisateur")

email_default, keywords_default, categories_default, enrich_default = read_user_config()

email_input = st.sidebar.text_input("Adresse email", value=email_default)
keywords_input = st.sidebar.text_input("Mots-clés (séparés par des virgules)", value=keywords_default)
use_enrichment = st.sidebar.checkbox("🤖 Utiliser l'enrichissement intelligent des mots-clés", value=enrich_default)
category_options = ["Offre d’emploi", "Mission freelance", "Événement", "Article pertinent", "Autre (inutile)"]
selected = st.sidebar.multiselect("Catégories à recevoir", options=category_options, default=categories_default)

if st.sidebar.button("📏 Sauvegarder mes paramètres"):
    save_user_config(email_input, keywords_input, selected, use_enrichment)
    st.sidebar.success("✅ Paramètres sauvegardés avec succès !")

# 📋 Récap des paramètres enregistrés
email, raw_keywords, selected_categories, enrich_mode = read_user_config()
if email:
    st.markdown(f"""
    ### 📬 Paramètres utilisateur :
    <ul style='line-height: 2;'>
        <li><b style='color:#0077B5;'>Email :</b> {email}</li>
        <li><b style='color:#0077B5;'>Mots-clés :</b> {raw_keywords}</li>
        <li><b style='color:#0077B5;'>Catégories :</b>
            {' '.join([f"<span style='background:#E8F4FD;padding:4px 8px;border-radius:5px;margin-right:5px;color:#0077B5;'>{cat}</span>" for cat in selected_categories])}
        </li>
    </ul>
    """, unsafe_allow_html=True)

# 🤖 Appliquer enrichissement si activé
keywords_used = raw_keywords
if enrich_mode and raw_keywords:
    enriched = enrich_keywords(raw_keywords)
    keywords_used = ", ".join(enriched)
    with open("filtered_keywords.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(enriched))
else:
    with open("filtered_keywords.txt", "w", encoding="utf-8") as f:
        f.write("\n".join([kw.strip() for kw in raw_keywords.split(",") if kw.strip()]))

# 🔍 Lire les mots-clés pour le filtrage depuis le fichier généré
def load_filtered_keywords():
    try:
        with open("filtered_keywords.txt", "r", encoding="utf-8") as f:
            return [kw.strip().lower() for kw in f.readlines() if kw.strip()]
    except FileNotFoundError:
        return []

# 🔘 Lancement manuel
st.markdown("---")
st.subheader("📤 Lancer l'analyse maintenant")
progress_bar = st.empty()

if st.button("🚀 Exécuter maintenant", type="primary"):
    with st.spinner("Analyse des posts et envoi du mail en cours..."):
        try:
            progress = st.progress(0)
            keywords_filter = load_filtered_keywords()
            posts = get_linkedin_posts()
            progress.progress(20)
            filtered_posts = [p for p in posts if any(kw in p["text"].lower() for kw in keywords_filter)]
            progress.progress(40)

            categorized = {
                "Offre d’emploi": [],
                "Mission freelance": [],
                "Événement": [],
                "Article pertinent": [],
                "Autre (inutile)": []
            }

            for idx, post in enumerate(filtered_posts):
                result = analyze_post(post)

                category = ""
                summary = ""

                lines = result.split("\n")
                for line in lines:
                    if "Catégorie" in line:
                        category = line.split(":", 1)[-1].strip()
                    elif "Résumé" in line:
                        summary = line.split(":", 1)[-1].strip()

                clean_summary = summary.strip()
                if clean_summary.startswith(":"):
                    clean_summary = clean_summary[1:].strip()
                while "  " in clean_summary:
                    clean_summary = clean_summary.replace("  ", " ")

                author = post["author"].strip()
                parts = author.split()
                half = len(parts) // 2
                if len(parts) % 2 == 0 and parts[:half] == parts[half:]:
                    author = " ".join(parts[:half])

                html_line = f"<li><strong>{author}</strong> : {clean_summary} → <a href='{post['link']}'>Voir le post</a></li>"

                if category in categorized:
                    categorized[category].append(html_line)
                else:
                    categorized["Autre (inutile)"].append(html_line)

                progress.progress(40 + int(50 * (idx + 1) / len(filtered_posts)))

            html_template = Template("""
            <h2>Résumé LinkedIn du jour</h2>
            {% for category, items in data.items() if items %}
                <h3>{{ category }}</h3>
                <ul>
                {{ items | join("\n") }}
                </ul>
            {% endfor %}
            """)

            html_content = html_template.render(data=categorized)
            send_email("📬 Résumé LinkedIn quotidien", html_content, email)
            progress.progress(100)
            st.success("🎉 Analyse terminée et email envoyé !")

        except Exception as e:
            st.error(f"❌ Une erreur est survenue : {e}")
