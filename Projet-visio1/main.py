"""
Point d'entrée de l'application
Gère le flux: Login → Application principale
"""

from auth_service import AuthService
from video_service import VideoService
from login_window import LoginWindow
from main_window import MainWindow

def main():
    """Fonction principale de l'application"""
    
    # Initialisation des services
    auth_service = AuthService("users.txt")
    video_service = VideoService()
    
    def on_login_success(username):
        """Callback appelé après une connexion réussie"""
        # Lancer l'application principale
        app = MainWindow(video_service, username)
        app.run()
    
    # Lancer la fenêtre de connexion
    login = LoginWindow(auth_service, on_login_success)
    login.run()

if __name__ == "__main__":
    main()