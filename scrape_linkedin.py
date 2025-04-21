from playwright.sync_api import sync_playwright
import time
import os

def get_last_seen_post():
    if os.path.exists("last_seen.txt"):
        with open("last_seen.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def save_last_seen_post(post_id):
    with open("last_seen.txt", "w", encoding="utf-8") as f:
        f.write(post_id)

def get_linkedin_posts():
    last_seen = get_last_seen_post()
    new_posts = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state="linkedin_cookies.json")
        page = context.new_page()

        page.goto("https://www.linkedin.com/feed/")
        time.sleep(5)

        print("🔄 Début du scroll pour charger les posts...")

        for _ in range(5):
            page.mouse.wheel(0, 5000)
            time.sleep(2.5)

        posts = page.locator("div.feed-shared-update-v2")
        count = posts.count()
        print(f"📄 {count} posts détectés")

        for i in range(count):
            try:
                post = posts.nth(i)

                urn = post.get_attribute("data-urn")
                if not urn or "activity" not in urn:
                    continue

                activity_id = urn.split(":")[-1]
                link = f"https://www.linkedin.com/feed/update/urn:li:activity:{activity_id}"

                if last_seen and link == last_seen:
                    print("🛑 Dernier post déjà vu trouvé, fin du scraping.")
                    break

                author = None
                author_el = post.locator("span.feed-shared-actor__name")
                if author_el.count() > 0:
                    author = author_el.first.inner_text().strip()

                # ✅ Nettoyage : si nom répété à l'identique (ex: "Anna Higgins Anna Higgins")
                if author:
                    author = author.strip()
                    if author.count(" ") >= 1:
                        half = len(author) // 2
                        if author[:half] == author[half:].strip():
                            author = author[:half].strip()

                if not author:
                    alt_author_el = post.locator("span.update-components-actor__title span span")
                    if alt_author_el.count() > 0:
                        author = alt_author_el.first.inner_text().strip()

                if not author:
                    author = "Inconnu"

                # Déplier "... plus"
                see_more_btn = post.locator("button[aria-label*='… plus'], button[aria-label*='… more']")
                if see_more_btn.count() > 0 and see_more_btn.first.is_visible():
                    see_more_btn.first.click()
                    time.sleep(1)

                # Extraire texte complet
                text_blocks = post.locator("span[dir='ltr']").all_inner_texts()
                text = " ".join(text_blocks).strip()

                if text:
                    new_posts.append({
                        "author": author,
                        "text": text,
                        "link": link
                    })

            except Exception as e:
                print(f"⚠️ Erreur sur le post {i} :", e)

        browser.close()

        if new_posts:
            save_last_seen_post(new_posts[0]["link"])
            print("📝 Lien du dernier post sauvegardé :", new_posts[0]["link"])

        return new_posts
