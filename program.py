import string 

# --- Constantes du jeu (Doivent être ici pour être utilisées par les fonctions) ---
PROFONDEURS = 3
TAILLE_GRILLE_VERTICAL = 5  # Correspond à A-E
TAILLE_GRILLE_HORIZONTAL = 10 # Correspond à 0-9

# --- Fonctions utilitaires ---

def init_grille():
    """Crée la structure 3D (Profondeur, Ligne (A-E), Colonne (0-9)) de la grille."""
    grille = []

    for prof in range(PROFONDEURS):
        profondeur = []
        for i in range(TAILLE_GRILLE_VERTICAL):
            ligne = []
            for y in range(TAILLE_GRILLE_HORIZONTAL):
                ligne.append(0) 
            profondeur.append(ligne)
        grille.append(profondeur)
    
    return grille


def choix_position():
    """Gère l'entrée utilisateur pour définir les positions d'un sous-marin."""
    position = []
    
    # Taille
    while True:
        try:
            size = int(input("Choisissez la taille du sous marin, entre 1 et 3 cases: "))
            if 1 <= size <= 3:
                break
            else:
                print("Taille invalide. Veuillez choisir entre 1 et 3.")
        except ValueError:
            print("Entrée invalide.")

    # orientation
    while True:
        orientation = input("Vertical (V) ou horizontal (H): ").upper()
        if orientation in ('V', 'H'):
            break
        print("Orientation invalide. Entrez 'V' ou 'H'.")

    # profondeur
    while True:
        try:
            profondeur = int(input("Choisissez une profondeur entre 100, 200 et 300 mètres: "))
            if profondeur == 100: 
                prof_index = 0
                break
            elif profondeur == 200: 
                prof_index = 1
                break
            elif profondeur == 300: 
                prof_index = 2
                break
            else:
                print("Profondeur invalide. Choisissez 100, 200 ou 300.")
        except ValueError:
            print("Entrée invalide.")

    # Validation des coordonnées de départ
    while True:
        x_char = input('Choisissez la position X du début (de A à E): ').upper()
        if 'A' <= x_char <= 'E':
             break
        print("Position X invalide. Choisissez entre A et E.")

    while True:
        try:
            y = int(input('Choisissez la position Y du début (de 0 à 9): '))
            if 0 <= y <= 9:
                break
            print("Position Y invalide. Choisissez entre 0 et 9.")
        except ValueError:
            print("Entrée invalide.")

    # Calcul des positions du sous-marin
    x = x_char
    for j in range(size):
        if orientation == 'V':
            if 'A' <= x <= 'E': # Vérification des limites pour la verticale
                position.append([x, y])
                x = chr(ord(x) + 1) 
            else:
                # Si le bateau sort, on annule (ce cas est géré par 'placer_bateau' si vous adaptez)
                # Mais pour l'instant, on se base sur votre logique initiale
                pass 
        else: # Horizontal
            if y < TAILLE_GRILLE_HORIZONTAL: # Vérification des limites pour l'horizontale
                position.append([x, y])
                y += 1
            else:
                pass
                
    # Ajout de l'indice de profondeur à la fin de la liste
    position.append(prof_index)
    
    return position


def print_grilles(grille):
    """Affiche une grille formatée."""
    lettres = string.ascii_uppercase
    profondeurs_labels = ["100 mètres", "200 mètres", "300 mètres"]

    for prof in range(PROFONDEURS):
        print(f"\n=== Profondeur {profondeurs_labels[prof]} ===")

        print("   ", end="")
        for col in range(TAILLE_GRILLE_HORIZONTAL):
            print(col, end=" ")
        print()

        print("  +" + "--" * TAILLE_GRILLE_HORIZONTAL + "+")

        for i in range(TAILLE_GRILLE_VERTICAL):
            print(f"{lettres[i]} |", end=" ")
            for y in range(TAILLE_GRILLE_HORIZONTAL):
                val = grille[prof][i][y]
                print(val if val != 0 else '~', end=" ")
            print("|")

        print("  +" + "--" * TAILLE_GRILLE_HORIZONTAL + "+")
        print("")


class Joueur:
    def __init__(self, nom_joueur):
        self.nom = nom_joueur 
        self.grille = init_grille() 
        self.positions_bateaux = [] # stockage des bateaux

    def placer_bateau(self, positions_sous_marin):
        """Valide et place le sous-marin sur la grille du joueur."""
        
        # utilise self.grille au lieu de seulement 'grille'
        prof_index = positions_sous_marin[-1]
        coords_seules = positions_sous_marin[:-1] 

        # Vérification de collision (lecture de la grille)
        for coord in coords_seules:
            x = ord(coord[0]) - ord('A') 
            y = coord[1]
            if self.grille[prof_index][x][y] != 0: # 0 = vide, 'X' = bateau
                return False 
        
        # 2. Ajout des positions (écriture sur la grille)
        for coord in coords_seules:
            x = ord(coord[0]) - ord('A') 
            y = coord[1]
            self.grille[prof_index][x][y] = 'B'
            self.positions_bateaux.append((prof_index, x, y)) 
        
        return True

    def afficher_grille(self):
        """Affiche la grille du joueur."""
        print_grilles(self.grille) 

    def a_encore_bateaux(self):
        """Vérifie si le joueur a encore des parties de bateaux intactes ('B')."""
        
        # On ne vérifie pas 'grille' en argument, on vérifie self.grille
        for profondeur in self.grille :
            for ligne in profondeur:
                if 'B' in ligne: 
                    return True
        return False
    
    def recevoir_tir(self, prof, x_coord, y_coord):
        """Traite un tir reçu par l'adversaire"""
        
        x = ord(x_coord) - ord('A')
        y = y_coord
        
        cible = self.grille[prof][x][y]
        
        # Case actuelle
        if cible == 'B':
            self.grille[prof][x][y] = 'X'
            return "Touché !"

        # Profondeurs voisines (si valides)
        positions = []

        if prof == 100:   # profondeur +100 possible
            positions.extend([(prof + 100, x, y)])
        if prof == 200:   # profondeur -100 et +100 possible
            positions.extend([(prof + 100, x, y)])
            positions.extend([(prof - 100, x, y)])
        if prof == 300:   # profondeur -100 possible
            positions.extend([(prof - 100, x, y)])

        # Voisins horizontaux/verticaux
        positions.extend([
            (prof, x - 1, y),
            (prof, x + 1, y),
            (prof, x, y - 1),
            (prof, x, y + 1),
        ])

        # Parcours de toutes les positions possibles
        for p, i, j in positions:
            print(self.grille[p][i][j])
            if self.grille[p][i][j] == 'B':
                self.grille[p][i][j] = 'X'
                return "Touché !"

        # Déjà touché ?
        if cible == 'X':
            return "Déjà touché !"

        # Rien trouvé = dans l'eau
        return "Dans l'eau !"
        
    def afficher_grille_cible(self):
        lettres = string.ascii_uppercase
        profondeurs_labels = ["100 mètres", "200 mètres", "300 mètres"]

        for prof in range(PROFONDEURS):
            print(f"\n=== Profondeur {profondeurs_labels[prof]} ===")

            print("   ", end="")
            for col in range(TAILLE_GRILLE_HORIZONTAL):
                print(col, end=" ")
            print()

            print("  +" + "--" * TAILLE_GRILLE_HORIZONTAL + "+")

            for i in range(TAILLE_GRILLE_VERTICAL):
                print(f"{lettres[i]} |", end=" ")
                for y in range(TAILLE_GRILLE_HORIZONTAL):
                    val = self.grille[prof][i][y]
                    print(val if (val != 0 and val !='B') else '~', end=" ")
                print("|")

            print("  +" + "--" * TAILLE_GRILLE_HORIZONTAL + "+")
            print("")
