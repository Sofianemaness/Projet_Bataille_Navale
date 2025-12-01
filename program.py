import main
import string

##########
#Méthodes# 
##########

def choix_position():
    position = []
    size = int(input("Choisissez la taille de votre sous marin (1 à 3 cases) : "))
    orientation = input("Vertical (V) ou horizontal (H) : ").upper()
    x = input('Choisissez la position X (A à E) : ').upper()
    y = int(input('Choisissez la position Y (0 à 9) : '))

    for i in range(size):
        position.append([0, x, y])  # temporaire profondeur=0

        if orientation == 'V':
            if chr(ord(x) + 1) != 'F':
                x = chr(ord(x) + 1)
        else:
            if y < 9:
                y += 1

    return position


def add_position(position, grille):
    """
    position = [
        [profondeur, 'A', 5],
        [profondeur, 'B', 5],
        ...
    ]
    """
    for coord in position:
        prof = coord[0]
        x = ord(coord[1]) - ord('A')  # convertit 'A' en 0 etc...
        y = coord[2]

        # Case occupée ?
        if grille[prof][x][y] == 'X':
            return False

    # Placement si tout est libre
    for coord in position:
        prof = coord[0]
        x = ord(coord[1]) - ord('A')
        y = coord[2]
        grille[prof][x][y] = 'X'

    return True


def init_grille():
    grille = []

    for prof in range(main.PROFONDEURS):
        profondeur = []
        for i in range(main.TAILLE_GRILLE_VERTICAL):
            ligne = []
            for y in range(main.TAILLE_GRILLE_HORIZONTAL):
                ligne.append(0)
            profondeur.append(ligne)
        grille.append(profondeur)
    
    return grille


def print_grilles(grille):
    lettres = string.ascii_uppercase
    profondeurs = ["100 mètres", "200 mètres", "300 mètres"]

    for prof in range(main.PROFONDEURS):
        print(f"\n=== Profondeur {profondeurs[prof]} ===")

        print("   ", end="")
        for col in range(main.TAILLE_GRILLE_HORIZONTAL):
            print(col, end=" ")
        print()

        print("  +" + "--" * main.TAILLE_GRILLE_HORIZONTAL + "+")

        for i in range(main.TAILLE_GRILLE_VERTICAL):
            print(f"{lettres[i]} |", end=" ")
            for y in range(main.TAILLE_GRILLE_HORIZONTAL):
                print(grille[prof][i][y], end=" ")
            print("|")

        print("  +" + "--" * main.TAILLE_GRILLE_HORIZONTAL + "+")


##########
#  Main  # 
##########

print("=== Initialisation des grilles ===")
grille_joueur_1 = init_grille()
grille_joueur_2 = init_grille()

print("\n=== Joueur A : Choisissez vos positions ===")
posJoueurA = choix_position()
if add_position(posJoueurA, grille_joueur_1):
    print("\nPositions ajoutées avec succès pour le joueur A")
else:
    print("\nÉchec : Une des cases est déjà occupée pour le joueur A")

print("\n=== Joueur B : Choisissez vos positions ===")
posJoueurB = choix_position()
if add_position(posJoueurB, grille_joueur_2):
    print("\nPositions ajoutées avec succès pour le joueur B")
else:
    print("\nÉchec : Une des cases est déjà occupée pour le joueur B")

print("\n=== Grille Joueur 1 ===")
print_grilles(grille_joueur_1)

print("\n=== Grille Joueur 2 ===")
print_grilles(grille_joueur_2)
