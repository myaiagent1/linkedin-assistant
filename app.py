import streamlit as st
from scrape_linkedin import scrape_linkedin_posts
from analyze_posts import analyze_posts
from send_email import send_email_with_summary
import os

st.set_page_config(page_title="LinkedIn Assistant", layout="centered")
st.title("🤖 LinkedIn Assistant")
st.write("Configurez vos préférences pour recevoir un résumé de posts LinkedIn par mail.")

# === SECTION : CONFIGURATION UTILISATEUR ===
st.subheader("🛠️ Configuration")

email = st.text_input("📧 Entrez votre adresse email")
keywords_input = st.text_area("🔍 Mots-clés (séparés par des virgules)", placeholder="ex: IA, marketing, Python")
frequency = st.selectbox("⏱️ Fréquence d’envoi", ["Quotidien", "Hebdomadaire", "Mensuel"])

if st.button("💾 Sauvegarder les préférences"):
    if not email or not keywords_input:
        st.error("Merci de remplir tous les champs.")
    else:
        # Sauvegarde dans les fichiers txt
        with open("user_config.txt", "w") as f:
            f.write(f"{email},{frequency}\n")

        with open("user_keywords.txt", "w") as f:
            for kw in keywords_input.split(","):
                kw = kw.strip()
                if kw:
                    f.write(f"{kw}\n")

        st.success("✅ Préférences enregistrées.")

# === SECTION : EXÉCUTION AUTOMATISÉE ===
st.subheader("🚀 Lancer le traitement")

if st.button("1️⃣ Scraper les posts LinkedIn"):
    result = scrape_linkedin_posts()
    st.success("✅ Posts récupérés.")

if st.button("2️⃣ Résumer les posts"):
    summary = analyze_posts()
    st.text_area("Résumé généré par l'IA :", summary, height=300)

if st.button("3️⃣ Envoyer le mail"):
    status = send_email_with_summary()
    st.success("📬 Mail envoyé avec succès.")
