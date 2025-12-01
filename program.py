import main
import string

##########
#Méthodes# 
##########
def choix_position():
    position = []
    while(size > 3 | size < 1):
        size = int(input("Choisissez la taille de votre sous marin, entre 1 et 3 cases: "))
    orientation = input("Vertical (V) ou horizontal (H): ")
    
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

grille = init_grille()
print_grilles(grille)