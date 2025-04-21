import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import threading
import schedule
import time

# Liste des mots-clés définis dynamiquement par l'utilisateur
user_keywords = []

# Fonction d'exécution manuelle du script

def run_script():
    try:
        run_button.config(state="disabled", bg=linkedin_blue, fg="white")
        progress_bar.config(mode="determinate", value=0, maximum=100)

        # Enregistre les mots-clés de l'utilisateur dans un fichier
        with open("user_keywords.txt", "w", encoding="utf-8") as f:
            f.write(",".join(user_keywords_entry.get().split(",")))

        # Simule une progression pendant l'exécution
        def animate_progress():
            for i in range(100):
                time.sleep(0.1)
                progress_bar.step(1)
                root.update_idletasks()

        progress_thread = threading.Thread(target=animate_progress)
        progress_thread.start()

        subprocess.run(["python", "main.py"], check=True)

        messagebox.showinfo("Succès", "Script exécuté avec succès !")

    except subprocess.CalledProcessError:
        messagebox.showerror("Erreur", "Une erreur est survenue lors de l'exécution du script.")
    finally:
        progress_bar.stop()
        progress_bar.config(value=0)
        run_button.config(state="normal", bg="white", fg=linkedin_blue)

# Planification avec schedule
scheduled_time = "08:00"

# Tâche de fond qui vérifie l'heure
def scheduler_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Appliquer la nouvelle heure de planification
def set_schedule():
    global scheduled_time
    scheduled_time = time_entry.get()
    schedule.clear()
    schedule.every().day.at(scheduled_time).do(lambda: threading.Thread(target=run_script).start())
    messagebox.showinfo("Planification mise à jour", f"Le script sera exécuté chaque jour à {scheduled_time}.")

# UI principale
root = tk.Tk()
root.title("Planificateur LinkedIn IA")
root.geometry("420x370")
root.resizable(False, False)
root.configure(bg="#FFFFFF")  # Fond blanc

linkedin_blue = "#0077B5"

# Titre
label = tk.Label(root, text="Assistant LinkedIn - Planification", font=("Helvetica", 14, "bold"), bg="#FFFFFF", fg=linkedin_blue)
label.pack(pady=10)

# Champ de saisie pour l'heure
time_label = tk.Label(root, text="Heure d'exécution quotidienne (HH:MM)", bg="#FFFFFF", fg=linkedin_blue)
time_label.pack()
time_entry = tk.Entry(root, justify="center", font=("Helvetica", 12))
time_entry.insert(0, scheduled_time)
time_entry.pack(pady=5)

# Champ de mots-clés
keyword_label = tk.Label(root, text="Mots-clés à filtrer (séparés par des virgules)", bg="#FFFFFF", fg=linkedin_blue)
keyword_label.pack()
user_keywords_entry = tk.Entry(root, justify="center", font=("Helvetica", 12))
user_keywords_entry.insert(0, "freelance,remote,cloud")
user_keywords_entry.pack(pady=5)

# Bouton planification
schedule_button = tk.Button(
    root,
    text="Planifier l'exécution",
    font=("Helvetica", 11),
    bg="white",
    fg=linkedin_blue,
    activebackground=linkedin_blue,
    activeforeground="white",
    highlightbackground=linkedin_blue,
    highlightthickness=1,
    command=set_schedule
)
schedule_button.pack(pady=10)

# Bouton exécution immédiate
def on_manual_run():
    threading.Thread(target=run_script).start()

run_button = tk.Button(
    root,
    text="Exécuter maintenant",
    font=("Helvetica", 11, "bold"),
    bg="white",
    fg=linkedin_blue,
    activebackground=linkedin_blue,
    activeforeground="white",
    highlightbackground=linkedin_blue,
    highlightthickness=1,
    command=on_manual_run
)
run_button.pack(pady=10)

# Barre de progression
style = ttk.Style()
style.theme_use('default')
style.configure("blue.Horizontal.TProgressbar", troughcolor="#FFFFFF", background=linkedin_blue)

progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate", length=300, style="blue.Horizontal.TProgressbar")
progress_bar.pack(pady=15)

# Démarrage du thread de surveillance
threading.Thread(target=scheduler_thread, daemon=True).start()

# Boucle principale de l'app
root.mainloop()