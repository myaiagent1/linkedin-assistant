from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # visible pour te connecter
    context = browser.new_context()

    page = context.new_page()
    page.goto("https://www.linkedin.com/login")

    print("🔐 Connecte-toi à LinkedIn dans la fenêtre qui s’ouvre.")
    input("✅ Appuie sur Entrée ici quand tu es connecté et sur ton fil d’actualité...")

    # Sauvegarder ta session
    context.storage_state(path="linkedin_cookies.json")
    print("📝 Session LinkedIn sauvegardée dans linkedin_cookies.json")

    browser.close()
