import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk


class VideoAnalysisApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Analyse vidéo scientifique – GPM")

        # Données
        self.cap = None
        self.times = []
        self.values = []
        self.frame_index = 0

        # --- Interface Tkinter ---
        control_frame = tk.Frame(root)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Button(control_frame, text="Charger vidéo", command=self.load_video).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Image suivante", command=self.next_frame).pack(side=tk.LEFT)

        # Zone vidéo
        self.video_label = tk.Label(root)
        self.video_label.pack(side=tk.LEFT, padx=10, pady=10)

        # --- Figure Matplotlib ---
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Évolution du paramètre mesuré")
        self.ax.set_xlabel("Temps (s)")
        self.ax.set_ylabel("Valeur")

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def load_video(self):
        path = filedialog.askopenfilename(filetypes=[("Videos", "*.mp4 *.avi *.webm")])
        if path:
            self.cap = cv2.VideoCapture(path)
            self.times.clear()
            self.values.clear()
            self.frame_index = 0
            self.ax.clear()
            self.ax.set_title("Évolution du paramètre mesuré")
            self.ax.set_xlabel("Temps (s)")
            self.ax.set_ylabel("Valeur")
            self.canvas.draw()

    def next_frame(self):
        if self.cap is None:
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        # --- Traitement scientifique (EXEMPLE) ---
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        measured_value = np.mean(gray)

        time = self.frame_index * (1 / 30)  # fps supposé = 30
        self.times.append(time)
        self.values.append(measured_value)
        self.frame_index += 1

        # --- Affichage vidéo ---
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.resize(frame_rgb, (300, 300))

        img = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(img)

        self.video_label.configure(image=img_tk)
        self.video_label.image = img_tk

        # --- Mise à jour du graphe ---
        self.ax.clear()
        self.ax.plot(self.times, self.values, marker="o")
        self.ax.set_xlabel("Temps (s)")
        self.ax.set_ylabel("Valeur mesurée")
        self.canvas.draw()


# Lancement
root = tk.Tk()
app = VideoAnalysisApp(root)
root.mainloop()
