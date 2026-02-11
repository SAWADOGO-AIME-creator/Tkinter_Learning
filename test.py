import tkinter as tk
from tkinter import messagebox

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Application de Gestion de Contacts")
fenetre.geometry("900x600")
fenetre.minsize(700, 400)
fenetre.configure(bg="#f0f0f0")  # Fond gris clair

# ==================== FUNCTIONS ====================
def ajouter_contact():
    """Fonction pour ajouter un contact à la liste"""
    nom = entry_nom.get()
    telephone = entry_telephone.get()
    
    if nom and telephone:
        contacts_listbox.insert(tk.END, f"{nom} - {telephone}")
        entry_nom.delete(0, tk.END)
        entry_telephone.delete(0, tk.END)
        status_label.config(text="Contact ajouté avec succès!", fg="green")
    else:
        messagebox.showwarning("Champs vides", "Veuillez remplir tous les champs")

def supprimer_contact():
    """Fonction pour supprimer le contact sélectionné"""
    try:
        index_selection = contacts_listbox.curselection()[0]
        contacts_listbox.delete(index_selection)
        status_label.config(text="Contact supprimé!", fg="red")
    except IndexError:
        messagebox.showinfo("Aucune sélection", "Veuillez sélectionner un contact à supprimer")

def effacer_tout():
    """Fonction pour effacer tous les contacts"""
    if messagebox.askyesno("Confirmation", "Voulez-vous vraiment tout effacer?"):
        contacts_listbox.delete(0, tk.END)
        status_label.config(text="Tous les contacts ont été effacés", fg="orange")

def changer_theme():
    """Fonction pour changer le thème de l'application"""
    if var_theme.get() == 1:
        fenetre.configure(bg="#2c3e50")
        main_frame.configure(bg="#2c3e50")
        status_label.config(bg="#2c3e50", fg="white")
    else:
        fenetre.configure(bg="#f0f0f0")
        main_frame.configure(bg="#f0f0f0")
        status_label.config(bg="#f0f0f0", fg="black")

def afficher_info():
    """Fonction pour afficher des informations"""
    nombre_contacts = contacts_listbox.size()
    messagebox.showinfo("Statistiques", 
                       f"Nombre de contacts : {nombre_contacts}\n"
                       f"Thème sombre : {'Activé' if var_theme.get() == 1 else 'Désactivé'}")

# ==================== MAIN FRAME ====================
main_frame = tk.Frame(fenetre, bg="#f0f0f0", padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# ==================== TITRE ====================
titre = tk.Label(
    main_frame, 
    text="📇 GESTIONNAIRE DE CONTACTS",
    font=("Arial", 18, "bold"),
    fg="#2c3e50",
    bg="#f0f0f0"
)
titre.pack(pady=(0, 20))

# ==================== FRAME POUR SAISIE ====================
frame_saisie = tk.LabelFrame(
    main_frame, 
    text="Ajouter un nouveau contact",
    font=("Arial", 11),
    bg="white",
    relief=tk.GROOVE,#la bordure du frame
    borderwidth=2
)
frame_saisie.pack(fill=tk.X, pady=(0, 20))#fill=tk.X, pour que le frame prenne toute la largeur disponible, pady=(0, 20) pour ajouter un espace en bas du frame

# Label et Entry pour le nom (ENTRY - widget de saisie)
tk.Label(frame_saisie, text="Nom :", bg="white", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_nom = tk.Entry(frame_saisie, width=30, font=("Arial", 10))
entry_nom.grid(row=0, column=1, padx=10, pady=10)
entry_nom.focus()  # Curseur placé dans ce champ au démarrage

# Label et Entry pour le téléphone
tk.Label(frame_saisie, text="Téléphone :", bg="white", font=("Arial", 10)).grid(row=0, column=2, padx=10, pady=10, sticky="w")
entry_telephone = tk.Entry(frame_saisie, width=20, font=("Arial", 10))
entry_telephone.grid(row=0, column=3, padx=10, pady=10)

# Bouton pour ajouter (BUTTON - widget bouton)
btn_ajouter = tk.Button(
    frame_saisie,
    text="Ajouter le contact",
    command=ajouter_contact,
    bg="#27ae60",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=15,
    pady=5
)
btn_ajouter.grid(row=0, column=4, padx=20, pady=10)

# ==================== FRAME POUR LA LISTE ====================
frame_liste = tk.LabelFrame(
    main_frame, 
    text="Liste des contacts",
    font=("Arial", 11),
    bg="white",
    relief=tk.GROOVE,
    borderwidth=2
)
frame_liste.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

# Scrollbar pour la liste (SCROLLBAR - barre de défilement)
scrollbar = tk.Scrollbar(frame_liste)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#



# Listbox pour afficher les contacts (LISTBOX - liste d'éléments)
contacts_listbox = tk.Listbox(
    frame_liste,
    yscrollcommand=scrollbar.set,
    font=("Arial", 11),
    height=10,
    selectbackground="#3498db",
    selectmode=tk.SINGLE
)
contacts_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
scrollbar.config(command=contacts_listbox.yview)

# ==================== FRAME POUR LES BOUTONS D'ACTION ====================
frame_boutons = tk.Frame(main_frame, bg="#f0f0f0")
frame_boutons.pack(fill=tk.X, pady=(0, 20))

# Bouton pour supprimer
btn_supprimer = tk.Button(
    frame_boutons,
    text="Supprimer le contact sélectionné",
    command=supprimer_contact,
    bg="#e74c3c",
    fg="white",
    font=("Arial", 10),
    padx=15,
    pady=8
)
btn_supprimer.pack(side=tk.LEFT, padx=5)

# Bouton pour tout effacer
btn_effacer = tk.Button(
    frame_boutons,
    text="Effacer tout",
    command=effacer_tout,
    bg="#f39c12",
    fg="white",
    font=("Arial", 10),
    padx=15,
    pady=8
)
btn_effacer.pack(side=tk.LEFT, padx=5)

# Bouton pour afficher les infos
btn_info = tk.Button(
    frame_boutons,
    text="Afficher les informations",
    command=afficher_info,
    bg="#3498db",
    fg="white",
    font=("Arial", 10),
    padx=15,
    pady=8
)
btn_info.pack(side=tk.LEFT, padx=5)

# ==================== FRAME POUR LES OPTIONS ====================
frame_options = tk.Frame(main_frame, bg="#f0f0f0")
frame_options.pack(fill=tk.X)

# Checkbutton pour le thème sombre (CHECKBUTTON - case à cocher)
var_theme = tk.IntVar()  # Variable pour stocker l'état de la checkbox
check_theme = tk.Checkbutton(
    frame_options,
    text="Activer le thème sombre",
    variable=var_theme,
    command=changer_theme,
    bg="#f0f0f0",
    font=("Arial", 10)
)
check_theme.pack(side=tk.LEFT, padx=5)

# Scale pour la taille de police (SCALE - curseur)
tk.Label(frame_options, text="Taille police:", bg="#f0f0f0", font=("Arial", 10)).pack(side=tk.LEFT, padx=(20,5))

def changer_taille_police(val):
    """Fonction pour changer la taille de la police"""
    contacts_listbox.config(font=("Arial", int(val)))

scale_police = tk.Scale(
    frame_options,
    from_=8,
    to=16,
    orient=tk.HORIZONTAL,
    command=changer_taille_police,
    bg="#f0f0f0",
    length=150
)
scale_police.set(11)  # Valeur par défaut
scale_police.pack(side=tk.LEFT, padx=5)

# OptionMenu pour trier (OPTIONMENU - menu déroulant)
tk.Label(frame_options, text="Trier par:", bg="#f0f0f0", font=("Arial", 10)).pack(side=tk.LEFT, padx=(20,5))

option_var = tk.StringVar(value="Ordre d'ajout")
option_menu = tk.OptionMenu(
    frame_options,
    option_var,
    "Ordre d'ajout",
    "Nom (A-Z)",
    "Nom (Z-A)"
)
option_menu.config(font=("Arial", 9))
option_menu.pack(side=tk.LEFT, padx=5)

# ==================== BARRE DE STATUT ====================
status_label = tk.Label(
    fenetre,
    text="Prêt à utiliser. Ajoutez votre premier contact!",
    bd=1,
    relief=tk.SUNKEN,
    anchor=tk.W,
    font=("Arial", 9),
    bg="#f0f0f0",
    fg="#2c3e50"
)
status_label.pack(side=tk.BOTTOM, fill=tk.X)

# ==================== MENU PRINCIPAL ====================
menu_bar = tk.Menu(fenetre)

# Menu Fichier
menu_fichier = tk.Menu(menu_bar, tearoff=0)
menu_fichier.add_command(label="Nouveau", accelerator="Ctrl+N")
menu_fichier.add_command(label="Ouvrir...")
menu_fichier.add_separator()
menu_fichier.add_command(label="Quitter", command=fenetre.quit)
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)

# Menu Édition
menu_edition = tk.Menu(menu_bar, tearoff=0)
menu_edition.add_command(label="Copier", accelerator="Ctrl+C")
menu_edition.add_command(label="Coller", accelerator="Ctrl+V")
menu_bar.add_cascade(label="Édition", menu=menu_edition)

# Menu Aide
menu_aide = tk.Menu(menu_bar, tearoff=0)
menu_aide.add_command(label="À propos", command=lambda: messagebox.showinfo("À propos", "Gestionnaire de Contacts v1.0\n\nApplication démonstrative Tkinter"))
menu_bar.add_cascade(label="Aide", menu=menu_aide)

fenetre.config(menu=menu_bar)

# ==================== LANCEMENT DE L'APPLICATION ====================
fenetre.mainloop()