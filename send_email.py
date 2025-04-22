import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Charger les variables d’environnement
load_dotenv()

def get_user_config(file_path="user_config.txt"):
    if not os.path.exists(file_path):
        return None, None
    with open(file_path, "r") as f:
        line = f.readline().strip()
        if line:
            email, frequency = line.split(",")
            return email.strip(), frequency.strip()
    return None, None

def read_summary(file_path="scraped_posts.txt"):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def send_email_with_summary():
    recipient_email, frequency = get_user_config()
    if not recipient_email:
        return "❌ Aucune configuration utilisateur trouvée."

    summary = read_summary()
    if not summary:
        return "❌ Aucun contenu à envoyer."

    # Récupérer les infos depuis .env
    sender_email = os.getenv("SMTP_EMAIL")
    sender_password = os.getenv("SMTP_PASSWORD")

    subject = "📰 Résumé LinkedIn - " + frequency

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    html = f"""
    <html>
    <body>
        <p>Bonjour,</p>
        <p>Voici votre résumé LinkedIn basé sur vos préférences :</p>
        <pre style="font-family:Arial;">{summary}</pre>
        <p>À bientôt,<br>🤖 LinkedIn Assistant</p>
    </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        return f"✅ Email envoyé à {recipient_email}"
    except Exception as e:
        return f"❌ Erreur d'envoi : {e}"
