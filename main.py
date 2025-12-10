import program
# import string # N'est plus nécessaire dans main.py


##########
#  Main  # 
##########

print("=== Initialisation des joueurs et des grilles ===")
# init des joueurs 
joueur_A = program.Joueur("Joueur A")
joueur_B = program.Joueur("Joueur B")


print("\n=== PHASE DE PLACEMENT ===")

# Joueur A
nb_sousmarinA = int(input(f"{joueur_A.nom}, combien de sous marins voulez-vous (taille 1 à 3)? >> "))
for i in range(nb_sousmarinA):
    while True:
        print(f"\n{joueur_A.nom}, placement du sous-marin n°{i+1}:")
        sous_marin_positions = program.choix_position() 
        if joueur_A.placer_bateau(sous_marin_positions):
            print("✅ Sous-marin ajouté.")
            break
        else:
            print("❌ Erreur : collision ou hors limites! Veuillez recommencer.")

joueur_A.afficher_grille() 


print("\n--- Changement de joueur ---")

# Joueur B 
nb_sousmarinB = int(input(f"{joueur_B.nom}, combien de sous marins voulez-vous (taille 1 à 3)? >> "))
for i in range(nb_sousmarinB):
    while True:
        print(f"\n{joueur_B.nom}, placement du sous-marin n°{i+1}:")
        sous_marin_positions = program.choix_position()
        if joueur_B.placer_bateau(sous_marin_positions):
            print("✅ Sous-marin ajouté.")
            break
        else:
            print("❌ Erreur : collision ou hors limites! Veuillez recommencer.")

joueur_B.afficher_grille()


# --- Jeu ---

joueurs = [joueur_A, joueur_B]
tour_joueur_index = 0

print("\n\n=== DÉBUT DE LA PARTIE ! ===")

# Le jeu continue tant qu'il reste des bateaux aux deux joueurs si un joueurs perd ses bateaux alors fin du jeu et le joueur d'en face gagne 
while joueurs[0].a_encore_bateaux() and joueurs[1].a_encore_bateaux():
    
    joueur_actif = joueurs[tour_joueur_index]
    joueur_cible = joueurs[1 - tour_joueur_index] # l'enemie

    print(f"\n--- 💣 TOUR de {joueur_actif.nom} (attaque {joueur_cible.nom}) ---")
    joueur_cible.afficher_grille_cible() 
    # --- Phase de Tir ---
    while True:
        try:
            # Saisie des coordonnées
            profondeur_tir = int(input("Profondeur du tir (100/200/300): "))
            if profondeur_tir == 100: prof = 0
            elif profondeur_tir == 200: prof = 1
            elif profondeur_tir == 300: prof = 2
            else: raise ValueError
            
            x_coord_tir = input("Position X du tir (A à E): ").upper()
            y_coord_tir = int(input("Position Y du tir (0 à 9): "))
                
            break 
        except (ValueError):
            print("Entrée invalide. Veuillez saisir des coordonnées valides (Profondeur: 100/200/300, X: A-E, Y: 0-9).")
            continue


    # Le joueur cible reçoit le tir
    resultat_tir = joueur_cible.recevoir_tir(prof, x_coord_tir, y_coord_tir)
    print(f"Résultat du tir sur {joueur_cible.nom} : **{resultat_tir}**")
    
    joueur_cible.afficher_grille_cible() 

    # Changement de joueur
    tour_joueur_index = 1 - tour_joueur_index


# --- Fin car sortie de la boucle while donc forcément un perdant ---
print("\n==============================")
if joueur_A.a_encore_bateaux():
    print(f" Le **{joueur_A.nom}** a coulé tous les sous-marins de l'adversaire et **GAGNE** la partie !")
else:
    print(f" Le **{joueur_B.nom}** a coulé tous les sous-marins de l'adversaire et **GAGNE** la partie !")
print("==============================")