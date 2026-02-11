import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from video_controller import VideoController

class VideoAnalysisApp:
    def __init__(self, root):
        self.root = root #root pourquoi ? c'est la fenêtre principale de l'application, qui contiendra tous les éléments graphiques et les contrôles.
        self.root.title("Analyseur de Videos")
        self.controller = VideoController()
        self.dark_theme = False
        self.center_window()
        
        # Construction de l'interface
        self.create_widgets()
        self.apply_theme()
        
        # Variable pour l'animation
        self.play_id = None
        
    def center_window(self):
        #Centre la fenêtre et je la rend responsive"
        self.root.update_idletasks()
        w = 1400
        h = 800
        self.root.geometry(f"{w}x{h}")
        x = (self.root.winfo_screenwidth() // 2) - (w // 2) 
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f'{w}x{h}+{x}+{y}')
        self.root.minsize(1000, 600)
        
    def create_widgets(self):
        #je cree tous ce qui est composants(widgets ...)
        
        #Barre de menu 
        menubar = tk.Menu(self.root) 
        self.root.config(menu=menubar)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)#tearoff=0 pourdésactiver le détachement du menu
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Ouvrir vidéo", command=self.load_video, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Menu Affichage
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Affichage", menu=view_menu)
        view_menu.add_command(label="Thème clair", command=lambda: self.set_theme(False))
        view_menu.add_command(label="Thème sombre", command=lambda: self.set_theme(True))
        
        # Barre outils principale
        toolbar = tk.Frame(self.root, height=50, relief=tk.RAISED, bd=1) #RAISED pour donner un effet de relief, bd=1 pour une bordure fine
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)
        
        # Boutons avec icônes texte
        self.btn_load = tk.Button(toolbar, text="📁 Charger", command=self.load_video,
                                  font=("Arial", 10, "bold"), padx=10)
        self.btn_load.pack(side=tk.LEFT, padx=2, pady=5) 
        
        self.btn_play = tk.Button(toolbar, text="▶ Lire", command=self.play_video,
                                  font=("Arial", 10), state=tk.DISABLED, padx=10)
        self.btn_play.pack(side=tk.LEFT, padx=2, pady=5)
        
        self.btn_pause = tk.Button(toolbar, text="⏸ Pause", command=self.pause_video,
                                   font=("Arial", 10), state=tk.DISABLED, padx=10) 
        self.btn_pause.pack(side=tk.LEFT, padx=2, pady=5)
        
        self.btn_prev = tk.Button(toolbar, text="⏪ Précédent", command=self.prev_frame,
                                  font=("Arial", 10), padx=10)
        self.btn_prev.pack(side=tk.LEFT, padx=2, pady=5)
        
        self.btn_next = tk.Button(toolbar, text="⏩ Suivant", command=self.next_frame,
                                  font=("Arial", 10), padx=10)
        self.btn_next.pack(side=tk.LEFT, padx=2, pady=5)
        
        # Séparateur |
        tk.Frame(toolbar, width=2, bd=1, relief=tk.SUNKEN).pack(side=tk.LEFT, padx=10, pady=5, fill=tk.Y)
        
        # Bouton de them acces rapide
        self.theme_btn = tk.Button(toolbar, text="🌓 Thème", command=self.toggle_theme,
                                   font=("Arial", 10), padx=10) 
        self.theme_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Panneau principal de video et graphique
        main_panel = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=5)
        main_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)#BOTH=plein X et Y
        
        # Panneau video
        video_frame = tk.Frame(main_panel, relief=tk.SUNKEN, bd=2)
        main_panel.add(video_frame, width=700)
        
        # Label pour le titre de la video
        self.video_title = tk.Label(video_frame, text="Aucune vidéo chargée", 
                                    font=("Arial", 10, "italic"))
        self.video_title.pack(pady=2)
        
        # Zone d'affichage video
        self.video_label = tk.Label(video_frame, bg='black')
        self.video_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Informations video
        self.video_info = tk.Label(video_frame, text="", font=("Arial", 9))
        self.video_info.pack(pady=2)
        
        #Panneau graphique
        graph_frame = tk.Frame(main_panel, relief=tk.SUNKEN, bd=2)
        main_panel.add(graph_frame, width=700)
        
        # Titre du graphique
        tk.Label(graph_frame, text="Évolution du paramètre mesuré", 
                font=("Arial", 11, "bold")).pack(pady=5)
        
        # Figure Matplotlib
        self.fig = Figure(figsize=(7, 6), dpi=100) #pdi=resolution
        self.ax = self.fig.add_subplot(111) 
        self.ax.set_xlabel("Temps (s)")
        self.ax.set_ylabel("Intensité moyenne")
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame) #ppour interger la figure dans un cadreTkinter 
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        #Barre d'état
        self.status_bar = tk.Label(self.root, text="Prêt | Ouvrez une vidéo pour commencer",
                                   bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        #Raccourcis clavier
        self.root.bind('<Control-o>', lambda e: self.load_video())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<space>', lambda e: self.toggle_play_pause())
        self.root.bind('<Right>', lambda e: self.next_frame())
        self.root.bind('<Left>', lambda e: self.prev_frame())
        
    def load_video(self, event=None):
        #Charge une video
        path = filedialog.askopenfilename(
            title="Sélectionner une vidéo",
            filetypes=[("Vidéos", "*.mp4 *.avi *.mov *.webm *.mkv"), ("Tous", "*.*")]
        )
        
        if not path:
            return
            
        try:
            self.controller.load_video(path)
            
            # Activer les boutons
            self.btn_play.config(state=tk.NORMAL)
            self.btn_pause.config(state=tk.NORMAL)
            self.btn_prev.config(state=tk.NORMAL)
            self.btn_next.config(state=tk.NORMAL)
            
            # Mettre à jour les infos
            filename = path.split('/')[-1]
            self.video_title.config(text=f"📹 {filename}")
            self.status_bar.config(text=f"Vidéo chargée : {filename} | {self.controller.total_frames} images | {self.controller.fps:.1f} fps")
            
            # Afficher la 1ere frame
            self.next_frame()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger la vidéo : {e}")
    
    def next_frame(self, event=None):
        #pass à image suivate
        if self.controller.cap is None:
            return
            
        frame_rgb, time = self.controller.get_frame()
        if frame_rgb is None:
            self.status_bar.config(text="Fin de la vidéo")
            self.pause_video()
            return
            
        # Traitement et mesure
        value = self.controller.process_frame(frame_rgb)
        self.controller.add_measurement(time, value)
        
        # Affichage
        self.display_frame(frame_rgb)
        self.update_plot()
        
        # Mise à jour de la barre d'état
        self.video_info.config(text=f"Image: {self.controller.current_index}/{self.controller.total_frames} | Temps: {time:.2f}s | Valeur: {value:.1f}")
        self.status_bar.config(text=f"Image {self.controller.current_index}/{self.controller.total_frames} | t={time:.2f}s | I={value:.1f}")
    
    def prev_frame(self, event=None):
        #Recule d'une image#
        if self.controller.cap is None or self.controller.current_index <= 1:
            return
            
        # Aller à l'index précédent
        target = max(0, self.controller.current_index - 2)
        frame_rgb, time = self.controller.get_frame(target)
        
        if frame_rgb is not None:
            value = self.controller.process_frame(frame_rgb)
            
            # Remplacer la dernière mesure
            if self.controller.times:
                self.controller.times[-1] = time
                self.controller.values[-1] = value
            else:
                self.controller.add_measurement(time, value)
            
            self.display_frame(frame_rgb)
            self.update_plot()
            self.video_info.config(text=f"Image: {self.controller.current_index}/{self.controller.total_frames} | Temps: {time:.2f}s | Valeur: {value:.1f}")
    
    def play_video(self):
        # #Lance la lecture continue#
        if self.controller.cap is None:
            return
            
        self.btn_play.config(state=tk.DISABLED)
        self.btn_pause.config(state=tk.NORMAL)
        self._play_loop()
    
    def _play_loop(self):
        #Boucle de lecture#
        if self.controller.cap is None:
            return
            
        self.next_frame()
        
        if self.controller.current_index < self.controller.total_frames - 1:
            delay = int(1000 / self.controller.fps)
            self.play_id = self.root.after(delay, self._play_loop)
        else:
            self.pause_video()
    
    def pause_video(self, event=None):
        #Met en pause la lecture#
        if self.play_id:
            self.root.after_cancel(self.play_id)
            self.play_id = None
        self.btn_play.config(state=tk.NORMAL)
        self.btn_pause.config(state=tk.DISABLED)
    
    def toggle_play_pause(self):
        #Bascule lecture/pause (espace)#
        if self.btn_play['state'] == tk.NORMAL and self.controller.cap is not None:
            self.play_video()
        else:
            self.pause_video()
    
    def display_frame(self, frame_rgb):
        #Affiche une image RGB#
        h, w, _ = frame_rgb.shape
        
        # Redimensionnement pour garder les proportions
        max_size = 500
        if w > max_size or h > max_size:
            ratio = min(max_size / w, max_size / h)
            new_w = int(w * ratio)
            new_h = int(h * ratio)
            frame_resized = cv2.resize(frame_rgb, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
        else:
            frame_resized = frame_rgb
        
        img = Image.fromarray(frame_resized)
        img_tk = ImageTk.PhotoImage(img)
        self.video_label.configure(image=img_tk)
        self.video_label.image = img_tk
    
    def update_plot(self):
        # Met à jour le graphique avec les nouvelles mesures
        self.ax.clear()
        
        if self.controller.times:
            self.ax.plot(self.controller.times, self.controller.values,
                        marker='o', linestyle='-', markersize=4, 
                        linewidth=1.5, color='#1f77b4')
            
            # Ajouter une ligne de tendance si assez de points
            if len(self.controller.times) > 1:
                z = np.polyfit(self.controller.times, self.controller.values, 1)
                p = np.poly1d(z)
                self.ax.plot(self.controller.times, p(self.controller.times), 
                           "--", color='red', alpha=0.7, linewidth=1, 
                           label=f'Tendance (pente={z[0]:.2f})')
                self.ax.legend()
        
        self.ax.set_xlabel("Temps (s)",fg_color="white")
        self.ax.set_ylabel("Intensité moyenne",fg_color="white")
        self.ax.grid(True, linestyle='--', alpha=0.6)
        
        # Ajustement automatique des limites
        if self.controller.times:
            self.ax.set_xlim(min(self.controller.times), max(self.controller.times) + 0.1)
            self.ax.set_ylim(min(self.controller.values) - 5, max(self.controller.values) + 5)
        
        self.canvas.draw()
    
    def set_theme(self, dark):
        #defini e theme
        self.dark_theme = dark
        self.apply_theme()
    
    def toggle_theme(self):
        #Bascule entre thème clair et sombre
        self.dark_theme = not self.dark_theme
        self.apply_theme()
    
    def apply_theme(self):
        #theme
        if self.dark_theme:
            # Thème sombre
            bg_color = "#1e1e1e"
            fg_color = "#ffffff"
            widget_bg = "#2d2d2d"
            widget_fg = "#ffffff"
            toolbar_bg = "#252526"
            status_bg = "#252526"
            
            # Matplotlib sombre
            self.fig.patch.set_facecolor('#1e1e1e')
            self.ax.set_facecolor('#2d2d2d')
            self.ax.tick_params(colors='white')
            self.ax.xaxis.label.set_color('white')
            self.ax.yaxis.label.set_color('white')
            self.ax.title.set_color('white')
            self.ax.grid(color='#404040')
        else:
            # Thème clair
            bg_color = "#f0f0f0"
            fg_color = "#000000"
            widget_bg = "#ffffff"
            widget_fg = "#000000"
            toolbar_bg = "#e0e0e0"
            status_bg = "#e0e0e0"
            
            # Matplotlib clair
            self.fig.patch.set_facecolor('white')
            self.ax.set_facecolor('white')
            self.ax.tick_params(colors='black')
            self.ax.xaxis.label.set_color('black')
            self.ax.yaxis.label.set_color('black')
            self.ax.title.set_color('black')
            self.ax.grid(color='lightgray')
        
        # Application des couleurs
        self.root.configure(bg=bg_color)
        
        # Toolbar
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and widget != self.video_label:
                widget.configure(bg=toolbar_bg)
        
        # Labels
        self.video_title.configure(bg=widget_bg, fg=fg_color)
        self.video_info.configure(bg=widget_bg, fg=fg_color)
        self.status_bar.configure(bg=status_bg, fg=fg_color)
        self.video_label.configure(bg='black')
        
        self.canvas.draw()
    
    def on_closing(self):
        #nettoyage
        self.controller.release()
        self.root.destroy()

# Point d'entrée
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoAnalysisApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()