import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# 🔐 Charger les infos du fichier .env
load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_SENDER = os.getenv("SMTP_EMAIL")
EMAIL_PASSWORD = os.getenv("SMTP_PASSWORD")  # mot de passe d'application
EMAIL_NAME = os.getenv("YOUR_EMAIL")         # nom visible dans la boîte

# ✉️ Fonction pour envoyer un email HTML
def send_email(subject, html_content, receiver_email):
    print("📤 Tentative d'envoi de l'email à :", receiver_email)

    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{EMAIL_NAME} <{EMAIL_SENDER}>"
        message["To"] = receiver_email

        # Corps du message
        part_html = MIMEText(html_content, "html")
        message.attach(part_html)

        # Connexion sécurisée et envoi
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, receiver_email, message.as_string())

        print("✅ Email envoyé avec succès !")

    except Exception as e:
        print(f"❌ Erreur lors de l’envoi de l’email : {e}")
        raise e  # permet de remonter l'erreur à Streamlit
