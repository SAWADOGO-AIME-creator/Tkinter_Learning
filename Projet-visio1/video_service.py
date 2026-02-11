"""
Service de traitement vidéo
Gère l'analyse scientifique des vidéos de microscope
"""

import cv2
import numpy as np

class VideoService:
    def __init__(self):
        self.cap = None
        self.times = []
        self.values = []
        self.frame_index = 0
        self.fps = 30
        self.current_frame = None
    
    def load_video(self, video_path):
        """Charge une vidéo et réinitialise les données"""
        if self.cap is not None:
            self.cap.release()
        
        self.cap = cv2.VideoCapture(video_path)
        
        if not self.cap.isOpened():
            return False
        
        # Récupérer le FPS réel de la vidéo
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        if self.fps == 0:
            self.fps = 30
        
        # Réinitialiser les données
        self.times.clear()
        self.values.clear()
        self.frame_index = 0
        self.current_frame = None
        
        return True
    
    def get_next_frame(self):
        """
        Lit la frame suivante et effectue l'analyse
        Retourne: (frame_rgb, time, measured_value, success)
        """
        if self.cap is None:
            return None, None, None, False
        
        ret, frame = self.cap.read()
        
        if not ret:
            return None, None, None, False
        
        # Analyse scientifique (luminosité moyenne en niveaux de gris)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        measured_value = np.mean(gray)
        
        # Calcul du temps
        time = self.frame_index / self.fps
        
        # Sauvegarde des données
        self.times.append(time)
        self.values.append(measured_value)
        self.frame_index += 1
        
        # Conversion pour affichage
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.current_frame = frame_rgb
        
        return frame_rgb, time, measured_value, True
    
    def reset_video(self):
        """Retourne au début de la vidéo"""
        if self.cap is not None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.frame_index = 0
            self.times.clear()
            self.values.clear()
    
    def get_data(self):
        """Retourne les données d'analyse"""
        return self.times.copy(), self.values.copy()
    
    def close(self):
        """Libère les ressources"""
        if self.cap is not None:
            self.cap.release()
            self.cap = None