import tkinter as tk
import randfacts 
from deep_translator import GoogleTranslator
import customtkinter as ctk
from PIL import Image, ImageTk

def afficher_info():
    info = randfacts.get_fact()

    #traduire le message avant de l'afficher
    info = GoogleTranslator(source='en', target='fr').translate(info)
    message_info.config(text=info)

ctk.set_appearance_mode("dark")  # Modes: "System" (par défaut), "Dark", "Light"

# Création de la fenêtre principale

app = ctk.CTk()
app.title("Random Facts")
app.geometry("1000x400")
app.update_idletasks()
width = app.winfo_width()
height = app.winfo_height()
x = (app.winfo_screenwidth() // 2) - (width // 2)
y = (app.winfo_screenheight() // 2) - (height // 2)
app.geometry(f'{width}x{height}+{x}+{y}')
app.minsize(600, 250)  # Taille minimale de la fenêtre

img=ImageTk.PhotoImage(Image.open("logo1.png").resize((50, 50)))  # Assurez-vous que le chemin de l'image est correct
label_title = ctk.CTkLabel(app, text="Text of Random Facts app", font=("Segoe Print", 20, "bold"),bg_color="#01152B", text_color="#FFFFFF")
btn_nouvelle_info = ctk.CTkButton(app, text="Afficher Nouvelle Info", font=("Arial", 24, "bold"),fg_color="#01152B", command=afficher_info, image=img, compound="right")
message_info=tk.Message(app, relief="sunken", font=("Arial", 12), width=800)
btn_quiter = ctk.CTkButton(app, text="Quit", font=("Arial", 15, "bold"),fg_color="#2b0401", command=app.destroy)

#applications des widgets sur la fenêtre
label_title.pack(pady=20)
btn_nouvelle_info.pack(pady=10, padx=20)
message_info.pack(pady=10)
btn_quiter.pack(pady=10)


#lancement de l'application
tk.mainloop()
