"""
Interface principale d'analyse vidéo
Visionnage professionnel avec graphique et thème clair/sombre
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import cv2

class MainWindow:
    # Thèmes
    THEMES = {
        'light': {
            'bg': '#F5F5F5',
            'fg': '#212121',
            'frame_bg': '#FFFFFF',
            'button_bg': '#2196F3',
            'button_fg': '#FFFFFF',
            'graph_bg': '#FFFFFF',
            'graph_fg': '#000000'
        },
        'dark': {
            'bg': '#1E1E1E',
            'fg': '#E0E0E0',
            'frame_bg': '#2D2D2D',
            'button_bg': '#0D47A1',
            'button_fg': '#FFFFFF',
            'graph_bg': '#2D2D2D',
            'graph_fg': '#E0E0E0'
        }
    }
    
    def __init__(self, video_service, username):
        self.video_service = video_service
        self.username = username
        self.current_theme = 'light'
        
        # Création de la fenêtre
        self.root = tk.Tk()
        self.root.title(f"GPM - Analyse Vidéo Microscope Électronique - {username}")
        self.root.geometry("1400x800")
        
        # Centrer la fenêtre
        self._center_window()
        
        # Taille minimale
        self.root.minsize(1000, 600)
        
        # Interface
        self._create_ui()
        
        # Appliquer le thème initial
        self.apply_theme()
        
        # Gestion de la fermeture
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def _center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_ui(self):
        """Crée l'interface principale"""
        # === BARRE SUPÉRIEURE ===
        toolbar = tk.Frame(self.root, relief="flat", bd=1)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Boutons de contrôle
        btn_style = {'font': ("Arial", 9), 'padx': 15, 'pady': 6, 'cursor': 'hand2', 'relief': 'flat'}
        
        self.btn_load = tk.Button(
            toolbar, 
            text="📁 Charger vidéo", 
            command=self.load_video,
            **btn_style
        )
        self.btn_load.pack(side=tk.LEFT, padx=3)
        
        self.btn_next = tk.Button(
            toolbar, 
            text="▶ Frame suivante", 
            command=self.next_frame,
            state=tk.DISABLED,
            **btn_style
        )
        self.btn_next.pack(side=tk.LEFT, padx=3)
        
        self.btn_reset = tk.Button(
            toolbar, 
            text="⟲ Réinitialiser", 
            command=self.reset_video,
            state=tk.DISABLED,
            **btn_style
        )
        self.btn_reset.pack(side=tk.LEFT, padx=3)
        
        # Séparateur
        tk.Frame(toolbar, width=2, bg="#CCCCCC").pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Bouton thème
        self.btn_theme = tk.Button(
            toolbar,
            text="🌙 Thème sombre",
            command=self.toggle_theme,
            **btn_style
        )
        self.btn_theme.pack(side=tk.LEFT, padx=3)
        
        # Info utilisateur
        tk.Label(
            toolbar, 
            text=f"👤 {self.username}", 
            font=("Arial", 9, "bold")
        ).pack(side=tk.RIGHT, padx=10)
        
        # === ZONE PRINCIPALE ===
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configuration responsive
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        
        # --- PANNEAU VIDÉO ---
        self.video_frame = tk.LabelFrame(
            main_container, 
            text="Visualisation Microscope", 
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10
        )
        self.video_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        self.video_label = tk.Label(
            self.video_frame, 
            text="Aucune vidéo chargée\n\nCliquez sur 'Charger vidéo' pour commencer",
            font=("Arial", 11),
            width=50,
            height=20
        )
        self.video_label.pack(expand=True)
        
        # --- PANNEAU GRAPHIQUE ---
        self.graph_frame = tk.LabelFrame(
            main_container, 
            text="Analyse des données", 
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10
        )
        self.graph_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        # Matplotlib figure
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Évolution de la luminosité moyenne", fontsize=12, fontweight='bold')
        self.ax.set_xlabel("Temps (s)", fontsize=10)
        self.ax.set_ylabel("Valeur (niveaux de gris)", fontsize=10)
        self.ax.grid(True, alpha=0.3)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # === BARRE D'ÉTAT ===
        self.status_bar = tk.Label(
            self.root, 
            text="Prêt", 
            anchor="w", 
            font=("Arial", 9),
            relief="sunken",
            padx=5
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_video(self):
        """Charge une vidéo de microscope"""
        path = filedialog.askopenfilename(
            title="Sélectionner une vidéo de microscope",
            filetypes=[
                ("Vidéos", "*.mp4 *.avi *.mov *.mkv *.webm"),
                ("Tous les fichiers", "*.*")
            ]
        )
        
        if not path:
            return
        
        # Charger la vidéo via le service
        if self.video_service.load_video(path):
            self.status_bar.config(text=f"Vidéo chargée: {path.split('/')[-1]}")
            self.btn_next.config(state=tk.NORMAL)
            self.btn_reset.config(state=tk.NORMAL)
            
            # Réinitialiser le graphique
            self.ax.clear()
            self.ax.set_title("Évolution de la luminosité moyenne", fontsize=12, fontweight='bold')
            self.ax.set_xlabel("Temps (s)", fontsize=10)
            self.ax.set_ylabel("Valeur (niveaux de gris)", fontsize=10)
            self.ax.grid(True, alpha=0.3)
            self.canvas.draw()
            
            messagebox.showinfo("Succès", "Vidéo chargée avec succès")
        else:
            messagebox.showerror("Erreur", "Impossible de charger la vidéo")
    
    def next_frame(self):
        """Affiche la frame suivante et met à jour le graphique"""
        frame_rgb, time, value, success = self.video_service.get_next_frame()
        
        if not success:
            messagebox.showinfo("Fin", "Fin de la vidéo atteinte")
            self.btn_next.config(state=tk.DISABLED)
            return
        
        # Afficher la frame
        frame_resized = cv2.resize(frame_rgb, (640, 480))
        img = Image.fromarray(frame_resized)
        img_tk = ImageTk.PhotoImage(img)
        self.video_label.configure(image=img_tk, text="")
        self.video_label.image = img_tk
        
        # Mettre à jour le graphique
        times, values = self.video_service.get_data()
        self.ax.clear()
        self.ax.plot(times, values, marker='o', markersize=4, linewidth=1.5, color='#2196F3')
        self.ax.set_title("Évolution de la luminosité moyenne", fontsize=12, fontweight='bold')
        self.ax.set_xlabel("Temps (s)", fontsize=10)
        self.ax.set_ylabel("Valeur (niveaux de gris)", fontsize=10)
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()
        
        # Mettre à jour la barre d'état
        self.status_bar.config(text=f"Frame: {len(times)} | Temps: {time:.2f}s | Valeur: {value:.2f}")
    
    def reset_video(self):
        """Réinitialise la vidéo"""
        self.video_service.reset_video()
        self.btn_next.config(state=tk.NORMAL)
        
        # Réinitialiser l'affichage
        self.video_label.configure(
            image='',
            text="Vidéo réinitialisée\n\nCliquez sur 'Frame suivante'"
        )
        
        # Réinitialiser le graphique
        self.ax.clear()
        self.ax.set_title("Évolution de la luminosité moyenne", fontsize=12, fontweight='bold')
        self.ax.set_xlabel("Temps (s)", fontsize=10)
        self.ax.set_ylabel("Valeur (niveaux de gris)", fontsize=10)
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()
        
        self.status_bar.config(text="Vidéo réinitialisée")
    
    def toggle_theme(self):
        """Bascule entre thème clair et sombre"""
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.apply_theme()
        
        # Changer le texte du bouton
        if self.current_theme == 'dark':
            self.btn_theme.config(text="☀ Thème clair")
        else:
            self.btn_theme.config(text="🌙 Thème sombre")
    
    def apply_theme(self):
        """Applique le thème sélectionné"""
        theme = self.THEMES[self.current_theme]
        
        # Fenêtre principale
        self.root.config(bg=theme['bg'])
        
        # Frames
        self.video_frame.config(bg=theme['frame_bg'], fg=theme['fg'])
        self.graph_frame.config(bg=theme['frame_bg'], fg=theme['fg'])
        
        # Labels
        self.video_label.config(bg=theme['frame_bg'], fg=theme['fg'])
        self.status_bar.config(bg=theme['frame_bg'], fg=theme['fg'])
        
        # Boutons
        for btn in [self.btn_load, self.btn_next, self.btn_reset, self.btn_theme]:
            btn.config(bg=theme['button_bg'], fg=theme['button_fg'])
        
        # Graphique Matplotlib
        self.fig.patch.set_facecolor(theme['graph_bg'])
        self.ax.set_facecolor(theme['graph_bg'])
        self.ax.spines['bottom'].set_color(theme['graph_fg'])
        self.ax.spines['top'].set_color(theme['graph_fg'])
        self.ax.spines['left'].set_color(theme['graph_fg'])
        self.ax.spines['right'].set_color(theme['graph_fg'])
        self.ax.tick_params(colors=theme['graph_fg'])
        self.ax.xaxis.label.set_color(theme['graph_fg'])
        self.ax.yaxis.label.set_color(theme['graph_fg'])
        self.ax.title.set_color(theme['graph_fg'])
        self.canvas.draw()
    
    def on_close(self):
        """Fermeture propre de l'application"""
        self.video_service.close()
        self.root.destroy()
    
    def run(self):
        """Lance l'application principale"""
        self.root.mainloop()