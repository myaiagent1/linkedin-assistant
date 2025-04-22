import streamlit as st
import os
import subprocess
from pathlib import Path

def debug_playwright():
    st.title("Diagnostic Playwright")
    
    # Vérifier le dossier Playwright
    st.header("1. Vérification des chemins")
    browser_path = Path("/home/appuser/.cache/ms-playwright")
    
    if browser_path.exists():
        st.success(f"✅ Le dossier {browser_path} existe")
        
        # Liste le contenu du dossier
        try:
            contents = list(browser_path.glob("**/*"))[:20]  # Limiter à 20 éléments
            st.write(f"Contenu ({len(contents)} premiers éléments):")
            for item in contents:
                st.write(f"- {item}")
        except Exception as e:
            st.error(f"Erreur lors de la lecture du dossier: {e}")
    else:
        st.error(f"❌ Le dossier {browser_path} n'existe pas")
    
    # Installation manuelle
    st.header("2. Installation manuelle")
    if st.button("Installer Playwright"):
        with st.spinner("Installation en cours..."):
            try:
                result = subprocess.run(
                    ["playwright", "install", "chromium"],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                st.subheader("Résultat de la commande:")
                st.code(result.stdout)
                
                if result.stderr:
                    st.subheader("Erreurs:")
                    st.code(result.stderr)
                
                # Vérifier à nouveau le dossier
                if browser_path.exists():
                    st.success("✅ Installation réussie! Le dossier existe maintenant.")
                else:
                    st.error("❌ Le dossier n'existe toujours pas après installation.")
            except Exception as e:
                st.error(f"Erreur lors de l'installation: {e}")
    
    # Test de lancement de navigateur
    st.header("3. Test de lancement du navigateur")
    if st.button("Tester le lancement du navigateur"):
        with st.spinner("Test en cours..."):
            try:
                code = """
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://example.com')
    title = page.title()
    browser.close()
    print(f"Test réussi! Titre de la page: {title}")
"""
                result = subprocess.run(
                    ["python", "-c", code],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if "Test réussi" in result.stdout:
                    st.success(result.stdout)
                else:
                    st.error("Le test a échoué")
                    st.code(result.stdout)
                    st.code(result.stderr)
            except Exception as e:
                st.error(f"Erreur lors du test: {e}")

# Exécuter le diagnostic
debug_playwright()
