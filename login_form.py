import tkinter as tk

# Création de la fenêtre principale
app = tk.Tk()
app.title("Login Form")
app.geometry("800x400")

# Centrer la fenêtre sur l'écran
app.update_idletasks()
width = app.winfo_width()
height = app.winfo_height()
x = (app.winfo_screenwidth() // 2) - (width // 2)
y = (app.winfo_screenheight() // 2) - (height // 2)
app.geometry(f'{width}x{height}+{x}+{y}')
app.minsize(600, 250)  # Taille minimale de la fenêtre

# Configuration pour que le frame s'adapte à la taille de l'écran
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

# Création du frame de connexion
login_frame = tk.LabelFrame(app, text="Connexion", padx=20, pady=20, bd=3, relief="groove")
login_frame.place(relx=0.5, rely=0.5, anchor="center")

# Champs du formulaire
username_label = tk.Label(login_frame, text="Nom d'utilisateur:", font=("Arial", 10))
username_label.grid(row=0, column=0, sticky="w", padx=5, pady=10)

username_entry = tk.Entry(login_frame, width=30, font=("Arial", 10))
username_entry.grid(row=0, column=1, padx=5, pady=10)

password_label = tk.Label(login_frame, text="Mot de passe:", font=("Arial", 10))
password_label.grid(row=1, column=0, sticky="w", padx=5, pady=10)

password_entry = tk.Entry(login_frame, width=30, show="*", font=("Arial", 10))
password_entry.grid(row=1, column=1, padx=5, pady=10)

# Fonction de connexion
def login():
    username = username_entry.get()
    password = password_entry.get()
    print(f"Connexion en cours pour: {username}")
    # Ajoutez ici votre logique de connexion

# Bouton de connexion
login_button = tk.Button(login_frame, text="Se connecter", command=login, 
                        bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                        padx=20, pady=5, cursor="hand2")
login_button.grid(row=2, column=1, sticky="e", pady=15)

# Focus sur le champ username au démarrage
username_entry.focus()

# Permettre la connexion avec la touche Entrée
app.bind('<Return>', lambda event: login())

# Lancement de l'application
app.mainloop()