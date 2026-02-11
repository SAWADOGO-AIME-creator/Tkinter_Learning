"""
Interface de connexion
Fenêtre d'authentification avec validation
"""

import tkinter as tk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, auth_service, on_login_success):
        self.auth_service = auth_service
        self.on_login_success = on_login_success
        
        # Création de la fenêtre
        self.root = tk.Tk()
        self.root.title("GPM - Connexion")
        self.root.geometry("500x300")
        
        # Centrer la fenêtre
        self._center_window()
        
        # Configuration minimale
        self.root.minsize(400, 250)
        
        # Interface
        self._create_ui()
        
        # Focus sur username
        self.username_entry.focus()
        
        # Touche Entrée pour se connecter
        self.root.bind('<Return>', lambda e: self.login())
    
    def _center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_ui(self):
        """Crée l'interface de connexion"""
        # Configuration du grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Frame de connexion
        login_frame = tk.LabelFrame(
            self.root, 
            text="Analyse Vidéo Microscope - GPM", 
            padx=30, 
            pady=25, 
            bd=2,
            font=("Arial", 11, "bold")
        )
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Nom d'utilisateur
        tk.Label(
            login_frame, 
            text="Nom d'utilisateur:", 
            font=("Arial", 10)
        ).grid(row=0, column=0, sticky="w", padx=5, pady=12)
        
        self.username_entry = tk.Entry(
            login_frame, 
            width=25, 
            font=("Arial", 10)
        )
        self.username_entry.grid(row=0, column=1, padx=5, pady=12)
        
        # Mot de passe
        tk.Label(
            login_frame, 
            text="Mot de passe:", 
            font=("Arial", 10)
        ).grid(row=1, column=0, sticky="w", padx=5, pady=12)
        
        self.password_entry = tk.Entry(
            login_frame, 
            width=25, 
            show="●", 
            font=("Arial", 10)
        )
        self.password_entry.grid(row=1, column=1, padx=5, pady=12)
        
        # Bouton de connexion
        tk.Button(
            login_frame,
            text="Se connecter",
            command=self.login,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=25,
            pady=6,
            cursor="hand2",
            relief="flat"
        ).grid(row=2, column=1, sticky="e", pady=15)
    
    def login(self):
        """Vérifie les identifiants et ouvre l'application principale"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning(
                "Champs vides", 
                "Veuillez remplir tous les champs"
            )
            return
        
        # Vérification de l'authentification
        if self.auth_service.authenticate(username, password):
            self.root.destroy()
            self.on_login_success(username)
        else:
            messagebox.showerror(
                "Erreur d'authentification", 
                "Nom d'utilisateur ou mot de passe incorrect"
            )
            self.password_entry.delete(0, tk.END)
    
    def run(self):
        """Lance la fenêtre de connexion"""
        self.root.mainloop()