import cv2
import numpy as np

class VideoController:
    def __init__(self):
        self.cap = None #objet de capture vidéo de OpenCV, utilisé pour lire les frames de la vidéo.
        self.fps = 30 #nombre de frames par seconde, utilisé pour calculer le temps correspondant à chaque frame.
        self.total_frames = 0
        self.current_index = 0
        self.times = []
        self.values = []

    def load_video(self, path):
        """Charge la vidéo et initialise les paramètres"""
        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            raise IOError("Impossible d'ouvrir la vidéo")

        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0 #récupère le nombre de frames par seconde de la vidéo, ou utilise 30.0 si la valeur n'est pas disponible.
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.current_index = 0 #index de la frame actuelle, initialisé à 0.
        self.times.clear() 
        self.values.clear()

    def get_frame(self, index=None):
        """
        Retourne la frame à l'index spécifié (ou la frame suivante si None)
        sous forme d'array RGB, ainsi que le temps correspondant.
        """
        if self.cap is None:
            return None, None

        if index is not None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, index)
            ret, frame = self.cap.read() #lit la frame à l'index spécifié et met à jour current_index.
            self.current_index = index
        else:
            ret, frame = self.cap.read()
            if ret:
                self.current_index += 1
            else:
                return None, None

        if not ret:
            return None, None

        time = self.current_index / self.fps
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), time

    def process_frame(self, frame_rgb):
        """
        Applique le traitement scientifique (ex: intensité moyenne).
        À adapter pour la microscopie électronique.
        """
        gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)
        # Mesure simple : moyenne des niveaux de gris
        value = np.mean(gray)#permet de calculer la moyenne des niveaux de gris de l'image, ce qui peut être utilisé comme une mesure d'intensité ou de luminosité globale de la frame.
        return value

    def add_measurement(self, time, value):
        """Ajoute une mesure aux listes"""
        self.times.append(time)
        self.values.append(value)

    def release(self):
        """Libère la ressource vidéo"""
        if self.cap:
            self.cap.release()