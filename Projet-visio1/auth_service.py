"""
Service d'authentification
Gère la lecture/écriture des identifiants dans un fichier texte
"""

class AuthService:
    def __init__(self, users_file="users.txt"):
        self.users_file = users_file
        self._init_file()
    
    def _init_file(self):
        """Crée le fichier users.txt s'il n'existe pas"""
        try:
            with open(self.users_file, 'x') as f:
                # Créer avec des utilisateurs par défaut
                f.write("admin:admin123\n")
                f.write("user:password\n")
        except FileExistsError:
            pass
    
    def authenticate(self, username, password):
        """
        Vérifie si l'utilisateur existe dans le fichier
        Retourne True si authentifié, False sinon
        """
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    stored_user, stored_pass = line.split(':')
                    if stored_user == username and stored_pass == password:
                        return True
            return False
        except Exception as e:
            print(f"Erreur d'authentification: {e}")
            return False
    
    def add_user(self, username, password):
        """Ajoute un nouvel utilisateur (optionnel)"""
        if self.user_exists(username):
            return False
        
        try:
            with open(self.users_file, 'a') as f:
                f.write(f"{username}:{password}\n")
            return True
        except Exception as e:
            print(f"Erreur d'ajout d'utilisateur: {e}")
            return False
    
    def user_exists(self, username):
        """Vérifie si un utilisateur existe déjà"""
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    stored_user = line.strip().split(':')[0]
                    if stored_user == username:
                        return True
            return False
        except Exception:
            return False