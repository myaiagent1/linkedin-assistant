from playwright.sync_api import sync_playwright
import json
import time
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Lecture des identifiants LinkedIn (optionnel, pour une future automatisation)
linkedin_email = os.getenv("LINKEDIN_EMAIL")
linkedin_password = os.getenv("LINKEDIN_PASSWORD")

def load_cookies(context, cookies_file="linkedin_cookies.json"):
    if not os.path.exists(cookies_file):
        raise FileNotFoundError("⚠️ Fichier de cookies non trouvé. Merci de te connecter et de sauvegarder tes cookies.")
    with open(cookies_file, "r") as f:
        cookies = json.load(f)
    context.add_cookies(cookies)

def read_keywords(file_path="user_keywords.txt"):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return [kw.strip().lower() for kw in f.readlines() if kw.strip()]

def save_posts(posts, filename="scraped_posts.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for post in posts:
            f.write(post + "\n\n")

def scrape_linkedin_posts():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            # Charger les cookies LinkedIn
            load_cookies(context)

            # Aller sur le feed LinkedIn
            page.goto("https://www.linkedin.com/feed/", timeout=60000)
            time.sleep(5)

            # Faire défiler la page pour charger plus de contenu
            for _ in range(3):
                page.mouse.wheel(0, 1000)
                time.sleep(2)

            # Localiser tous les posts
            posts_elements = page.locator("div.feed-shared-update-v2")
            count = posts_elements.count()
            print(f"{count} posts détectés.")

            keywords = read_keywords()
            matched_posts = []

            for i in range(count):
                post = posts_elements.nth(i)
                content = post.inner_text()

                if any(keyword in content.lower() for keyword in keywords):
                    try:
                        post_url = post.locator("a").first.get_attribute("href")
                        summary = content[:300]  # Simple résumé brut
                        matched_posts.append(f"{summary}\n➡️ {post_url}")
                    except:
                        continue

            save_posts(matched_posts)
            return f"✅ {len(matched_posts)} posts filtrés avec succès."

        except Exception as e:
            print("Erreur :", e)
            return f"❌ Échec du scraping : {e}"

        finally:
            browser.close()
            try:
    browser = p.chromium.launch(headless=True)
except Exception as e:
    return "❌ Playwright ne peut pas lancer Chromium ici. Essaie depuis ton ordinateur local."

