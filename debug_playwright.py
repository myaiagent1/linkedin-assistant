import os
import subprocess
import streamlit as st

def debug_playwright():
    st.header("Diagnostique de Playwright")
    
    # Vérifier le contenu du dossier cache
    st.subheader("Vérification des dossiers")
    
    cache_dir = "/home/appuser/.cache/ms-playwright/"
    st.write(f"Recherche du dossier: {cache_dir}")
    
    if os.path.exists(cache_dir):
        st.success(f"✅ Le dossier existe!")
        try:
            files = os.listdir(cache_dir)
            st.write(f"Contenu: {files}")
        except Exception as e:
            st.error(f"Erreur lors de la lecture du dossier: {e}")
    else:
        st.error(f"❌ Le dossier n'existe pas!")
    
    # Tenter une installation manuelle
    st.subheader("Tentative d'installation manuelle")
    
    if st.button("Installer Playwright maintenant"):
        try:
            st.info("Installation en cours... Veuillez patienter (peut prendre jusqu'à 2 minutes)")
            result = subprocess.run(
                ["python", "-m", "playwright", "install", "chromium"],
                capture_output=True,
                text=True,
                timeout=180
            )
            st.write("Résultat de la commande:")
            st.code(result.stdout)
            
            if result.stderr:
                st.write("Erreurs éventuelles:")
                st.code(result.stderr)
                
            # Vérifier si l'installation a réussi
            if os.path.exists(cache_dir):
                try:
                    updated_files = os.listdir(cache_dir)
                    st.success(f"Contenu mis à jour: {updated_files}")
                except Exception as e:
                    st.error(f"Erreur lors de la lecture du dossier: {e}")
        except Exception as e:
            st.error(f"Erreur lors de l'installation: {e}")

# Interface principale
st.title("Débogage de Playwright")
st.write("Cet outil vous aide à diagnostiquer les problèmes avec Playwright")

debug_playwright()
