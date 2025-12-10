import string 
import tkinter as tk
from functools import partial

# --- Constantes du jeu ---
PROFONDEURS = 3
TAILLE_GRILLE_VERTICAL = 5  # Correspond à A-E
TAILLE_GRILLE_HORIZONTAL = 10 # Correspond à 0-9

# --- Fonctions utilitaires ---

def init_grille():
    """Crée la structure 3D (Profondeur, Ligne (A-E), Colonne (0-9)) de la grille."""
    grille = []
    # ... (Le reste de la fonction init_grille reste le même) ...
    for prof in range(PROFONDEURS):
        profondeur = []
        for i in range(TAILLE_GRILLE_VERTICAL):
            ligne = []
            for y in range(TAILLE_GRILLE_HORIZONTAL):
                ligne.append(0) 
            profondeur.append(ligne)
        grille.append(profondeur)
    
    return grille

# La fonction 'choix_position' doit être remplacée par une saisie GUI plus tard,
# mais pour l'instant, on la garde telle quelle pour la phase de placement en console.
# ... (La fonction choix_position reste le même) ...
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
            if 'A' <= x <= 'E': 
                position.append([x, y])
                x = chr(ord(x) + 1) 
            else:
                pass 
        else: # Horizontal
            if y < TAILLE_GRILLE_HORIZONTAL: 
                position.append([x, y])
                y += 1
            else:
                pass
                
    # Ajout de l'indice de profondeur à la fin de la liste
    position.append(prof_index)
    
    return position
# --- La fonction print_grilles est supprimée ---


# --- Classe Joueur (Modifiée pour le GUI) ---

class Joueur:
    def __init__(self, nom_joueur):
        self.nom = nom_joueur 
        self.grille = init_grille() 
        self.positions_bateaux = [] 
        # Nouveau : Stockage des objets Bouton Tkinter
        self.boutons_ui = {} # Clé: (prof, ligne, colonne) -> Valeur: objet Button

    def placer_bateau(self, positions_sous_marin):
        """Valide et place le sous-marin sur la grille du joueur."""
        # ... (La logique de placer_bateau reste la même pour la grille interne) ...
        prof_index = positions_sous_marin[-1]
        coords_seules = positions_sous_marin[:-1] 

        # 1. Vérification de collision 
        for coord in coords_seules:
            x = ord(coord[0]) - ord('A') 
            y = coord[1]
            if not (0 <= x < TAILLE_GRILLE_VERTICAL and 0 <= y < TAILLE_GRILLE_HORIZONTAL):
                return False # Hors limite
            if self.grille[prof_index][x][y] != 0: 
                return False 
        
        # 2. Ajout des positions 
        for coord in coords_seules:
            x = ord(coord[0]) - ord('A') 
            y = coord[1]
            self.grille[prof_index][x][y] = 'B'
            self.positions_bateaux.append((prof_index, x, y)) 
        
        # 3. Mettre à jour l'affichage GUI si les boutons existent déjà
        # Lors de l'initialisation, cela n'est pas utilisé, mais lors d'un éventuel placement GUI oui.
        # Pour l'instant, on laisse l'affichage être géré par afficher_grille_proprietaire après la phase console.
        
        return True

    def a_encore_bateaux(self):
        """Vérifie si le joueur a encore des parties de bateaux intactes ('B')."""
        # ... (La logique de a_encore_bateaux reste la même) ...
        for profondeur in self.grille :
            for ligne in profondeur:
                if 'B' in ligne: 
                    return True
        return False

    # ... (le reste de la classe Joueur) ...

    def recevoir_tir(self, prof_base, x_coord, y_coord):
        """
        Traite un tir reçu, affectant la position de base, les cases adjacentes 
        (N, S, E, W) sur la même profondeur, et la même position sur les 
        profondeurs adjacentes.
        """
        x_base = ord(x_coord) - ord('A')
        y_base = y_coord
        
        # Liste pour stocker toutes les coordonnées [prof, x, y] à vérifier
        coords_a_verifier = []
        
        # 1. Coordonnées dans la PROFONDEUR DE BASE (3x3 en 2D)
        # On vérifie la case ciblée et ses 8 voisines (N, S, E, W, NE, NW, SE, SW)
        # Note : Par simplicité, on va seulement considérer N, S, E, W pour commencer
        
        # Décalages à appliquer (Profondeur, Ligne (X), Colonne (Y))
        # [0, 0, 0] = Position de base
        # [0, 0, +/-1] = Gauche/Droite
        # [0, +/-1, 0] = Haut/Bas
        # [+/-1, 0, 0] = Profondeur adjacente
        
        # Décalages (dProf, dX, dY)
        decalages = [
            (0, 0, 0),    # Position de base
            (0, 0, -1),   # Zone Ouest (Y-1)
            (0, 0, 1),    # Zone Est (Y+1)
            (0, -1, 0),   # Zone Nord (X-1)
            (0, 1, 0),    # Zone Sud (X+1)
            (1, 0, 0),    # Profondeur Supérieure
            (-1, 0, 0)    # Profondeur Inférieure
        ]

        # on va ici stocket la liste des positions à check en prenant en compte les limites
        for dProf, dX, dY in decalages:
            prof_new = prof_base + dProf
            x_new = x_base + dX
            y_new = y_base + dY
            
            est_valide = (0 <= prof_new < PROFONDEURS) and \
                         (0 <= x_new < TAILLE_GRILLE_VERTICAL) and \
                         (0 <= y_new < TAILLE_GRILLE_HORIZONTAL)
                         
            if est_valide:
                coords_a_verifier.append((prof_new, x_new, y_new))

        # --- Traitement des Impacts ---
        
        impact_total = "Dans l'eau !"
        nbre_touches = 0
        
        # ensemble pour éviter la redondance de traitement de la coordonnée
        coords_a_verifier = list(set(coords_a_verifier))
        
        for prof, x, y in coords_a_verifier:
            cible = self.grille[prof][x][y]
            key = (prof, x, y)
            
            # 1. Mise à jour de la grille interne
            if cible == 'B':
                self.grille[prof][x][y] = 'X' # Bateau touché
                impact_total = "Touché !"
                nbre_touches += 1
                
                # Mise à jour du bouton GUI correspondant (affichage propriétaire/cible)
                if key in self.boutons_ui:
                    bouton = self.boutons_ui[key]
                    bouton.config(text='X', bg="red", state=tk.DISABLED)

            elif cible == 0:
                # Tir raté sur l'eau : Marquer 'O' pour les tirs ratés
                self.grille[prof][x][y] = 'O'
                
                # Mise à jour du bouton GUI correspondant
                if key in self.boutons_ui:
                    bouton = self.boutons_ui[key]
                    bouton.config(text='O', bg="lightgrey", state=tk.DISABLED)
            
        # 2. Détermination du Résultat final
        if nbre_touches > 0:
            if nbre_touches == 1:
                return "Touché !"
            else:
                return f"Touché {nbre_touches} fois !"
        else:
            return impact_total # "Dans l'eau !" (si toutes les cibles étaient '0', 'X', ou 'O')
        
    # --- Nouvelles fonctions GUI ---
    
    def afficher_grille_proprietaire(self, root_frame):
        """Affiche la grille du joueur avec ses propres bateaux ('B' visibles).
        Utilisée après la phase de placement.
        """
        self._creer_grille_ui(root_frame, mode_proprietaire=True, fonction_clic=None)
        
    def afficher_grille_cible(self, root_frame, fonction_clic_parent):
        """Affiche la grille du joueur pour l'attaquant avec bateaux 'B' cachés.        """
        self._creer_grille_ui(root_frame, mode_proprietaire=False, fonction_clic=fonction_clic_parent)


    def _creer_grille_ui(self, root_frame, mode_proprietaire, fonction_clic):
        """Fonction interne pour générer l'interface Tkinter de la grille."""
        lettres = string.ascii_uppercase
        profondeurs_labels = ["100m", "200m", "300m"]
        
        # Nettoyer l'ancienne interface si elle existe (pour changer de joueur)
        for widget in root_frame.winfo_children():
            widget.destroy()
        self.boutons_ui = {} # Réinitialiser les références de boutons

        # Création de 3 Frame (une par profondeur)
        for prof in range(PROFONDEURS):
            # Frame pour cette profondeur
            frame_prof = tk.LabelFrame(root_frame, text=f"{profondeurs_labels[prof]}", padx=5, pady=5)
            # Les placer côte à côte
            frame_prof.grid(row=0, column=prof, padx=10, pady=10, sticky="n") 
            
            # --- Entête des colonnes (0-9) ---
            for col in range(TAILLE_GRILLE_HORIZONTAL):
                tk.Label(frame_prof, text=str(col), width=3).grid(row=0, column=col + 1)
                
            # --- Boucle des lignes (A-E) et des colonnes (0-9) ---
            for ligne in range(TAILLE_GRILLE_VERTICAL):
                x_char = lettres[ligne]
                # Entête de ligne (A, B, C...)
                tk.Label(frame_prof, text=x_char, width=3).grid(row=ligne + 1, column=0) 
                
                for colonne in range(TAILLE_GRILLE_HORIZONTAL):
                    y = colonne
                    
                    val_interne = self.grille[prof][ligne][colonne]
                    
                    # Détermination de l'affichage initial
                    if mode_proprietaire:
                        text_bouton = 'B' if val_interne == 'B' else '~'
                        bg_color = "green" if val_interne == 'B' else "blue"
                    else: # Mode cible (cache les 'B')
                        text_bouton = 'X' if val_interne == 'X' else ('O' if val_interne == 'O' else '~')
                        bg_color = "red" if val_interne == 'X' else ("lightgrey" if val_interne == 'O' else "blue")
                        
                    # Création du bouton
                    bouton = tk.Button(
                        frame_prof,
                        text=text_bouton,
                        width=3,
                        height=1,
                        bg=bg_color,
                        fg="white"
                    )
                    
                    # Gestion du clic
                    if fonction_clic and not mode_proprietaire and val_interne in (0, 'B'):
                        # Le clic n'est actif que si on est en mode cible ET que la case n'a pas été touchée ('X' ou 'O')
                        # On utilise partial pour lier les coordonnées au clic
                        action_tir = partial(fonction_clic, prof, x_char, y)
                        bouton.config(command=action_tir)
                        bouton.config(state=tk.NORMAL)
                    else:
                         # Désactiver si c'est la grille propriétaire, ou si c'est déjà touché
                        bouton.config(state=tk.DISABLED)

                    # Placer le bouton dans la frame
                    bouton.grid(row=ligne + 1, column=colonne + 1, padx=1, pady=1)
                    
                    # Stocker la référence
                    self.boutons_ui[(prof, ligne, colonne)] = bouton
