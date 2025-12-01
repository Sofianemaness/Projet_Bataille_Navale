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
    lettres = string.ascii_uppercase  # A, B, C...

    for prof in range(main.PROFONDEURS):
        print(f"Profondeur {prof}")

        # Affichage des numéros de colonnes
        print("   ", end="")
        for col in range(main.TAILLE_GRILLE_HORIZONTAL):
            print(col, end=" ")
        print()

        print("  +" + "--" * main.TAILLE_GRILLE_HORIZONTAL + "+")

        # Affichage des lignes
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

print("JOUEUR A: ")
nb_sousmarinA = int(input("Combien de sous marins voulez vous? >> "))
posJoueurA = []
for i in range(nb_sousmarinA):
    posJoueurA.append(choix_position())
print("JOUEUR B: ")
nb_sousmarinB = int(input("Combien de sous marins voulez vous? >> "))
posJoueurB = []
for i in range(nb_sousmarinB):
    posJoueurB.append(choix_position())
print("Joueur A: ", posJoueurA)
print("Joueur B: ", posJoueurB)
grille = init_grille()
print_grilles(grille)
