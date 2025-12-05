import main
import string

##########
#Méthodes#
##########

def choix_position():
    position = []
    size = int(input("Choisissez la taille du sous marin, entre 1 et 3 cases: "))
    orientation = input("Vertical (V) ou horizontal (H): ")
    profondeur = int(input("Choisissez une profondeur entre 100, 200 et 300 mètres: "))
    if(profondeur == 100) : profondeur = 0
    if(profondeur == 200) : profondeur = 1
    if(profondeur == 300) : profondeur = 2
    x = input('Choisissez la position X du début (de A à E): ')
    y = int(input('Choisissez la position Y du début (de 0 à 9): '))
    for j in range(size):
        if(orientation == 'V'):
            if(x != 'F') :
                position.append([x, y])
                x = chr(ord(x) + 1)
        else:
            if(y < 9) :
                position.append([x, y])
                y += 1
    position.append(profondeur)
    return position

def add_position(positions_sous_marin, grille):
    # L'indice de profondeur est le dernier élément de la liste
    prof_index = positions_sous_marin[-1]
   
    # Les coordonnées réelles sont tous les éléments sauf le dernier
    coords_seules = positions_sous_marin[:-1]

    for coord in coords_seules:
        # coord est de la forme ['Lettre', Nombre] (ex: ['A', 5])
        x = ord(coord[0]) - ord('A')
        y = coord[1]

        if grille[prof_index][x][y] == 'X':
            return False

    for coord in coords_seules:
        x = ord(coord[0]) - ord('A')
        y = coord[1]
       
        grille[prof_index][x][y] = 'X'

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
        print("")  # espace entre grilles


##########
#  Main  #
##########

print("=== Initialisation des grilles ===")
grille_joueur_1 = init_grille()
grille_joueur_2 = init_grille()

print("\n=== Joueur A : Choisissez vos positions ===")
nb_sousmarinA = int(input("Combien de sous marins voulez vous? >> "))
posJoueurA = []
for i in range(nb_sousmarinA):
    sous_marin = choix_position()
    if add_position(sous_marin, grille_joueur_1):
        posJoueurA.append(sous_marin)
        print("Sous-marin ajouté")
    else:
        print("Erreur : collision ! Veuillez recommencer")
        i -= 1


print("\n=== Joueur B : Choisissez vos positions ===")
nb_sousmarinB = int(input("Combien de sous marins voulez vous? >> "))
posJoueurB = []
for i in range(nb_sousmarinB):
    sous_marin = choix_position()
    if add_position(sous_marin, grille_joueur_2):
        posJoueurB.append(sous_marin)
        print("Sous-marin ajouté")
    else:
        print("Erreur : collision ! Veuillez recommencer")
        i -= 1

print("\n=== Grille Joueur 1 ===")
print_grilles(grille_joueur_1)

print("\n=== Grille Joueur 2 ===")
print_grilles(grille_joueur_2)
