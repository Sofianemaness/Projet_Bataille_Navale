# --- 1. CONSTANTES DE CONFIGURATION ---

# Définition de la taille de la grille 
# Exemple: 5x10x3 (5 lignes, 5 colonnes, 5 profondeurs)
TAILLE_GRILLE_VERTICAL = 5
TAILLE_GRILLE_HORIZONTAL=10
PROFONDEURS = 3 

# Définition des sous-marins avec leur nom et leur taille (longueur)
# Une liste de tuples (Nom, Taille)
SOUS_MARINS = [
    ("Nautilus", 3),  # Sous-marin de longueur 3
    ("Triton", 2),    # Sous-marin de longueur 2
    
]

# Codes pour l'affichage/l'état de la grille
GRILLE_VIDE = 0      # Cellule vide/non touchée
GRILLE_SOUS_MARIN = 1 # Partie de sous-marin
GRILLE_TOUCHE = 2    # Coup ayant touché un sous-marin (X)
GRILLE_MANQUE = 3    # Coup dans l'eau (O)

TOUR_UTILISATEUR = 0   # 0 si utilisateur 1 / 1 pour utilisateur 2 