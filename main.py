import program
import tkinter as tk
from tkinter import simpledialog # Pour la saisie des sous-marins (temporaire)

# --- Variables Globales du Jeu ---
joueur_A = program.Joueur("Joueur A")
joueur_B = program.Joueur("Joueur B")
joueurs = [joueur_A, joueur_B]
tour_joueur_index = 0
tour_actif = True # Indique si un tour est en cours (pour bloquer le jeu)

# --- Initialisation Tkinter ---
root = tk.Tk()
root.title("Bataille Navale 3D")
# Frame principale pour le plateau de jeu (où les grilles seront affichées)
game_frame = tk.Frame(root) 
game_frame.pack(padx=20, pady=20) 

# Zone de message pour les instructions/résultats
message_var = tk.StringVar()
message_label = tk.Label(root, textvariable=message_var, font=('Arial', 14, 'bold'))
message_label.pack(pady=10)

# --- Fonctions de Jeu GUI ---

def debuter_placement():
    """Gère la phase de placement en utilisant des boîtes de dialogue simples."""
    global joueur_A, joueur_B
    
    message_var.set(f"PHASE DE PLACEMENT : {joueur_A.nom}")
    
    # Placement Joueur A (Utilisation temporaire de simpledialog)
    try:
        nb_sousmarinA = simpledialog.askinteger("Placement", f"{joueur_A.nom}, combien de sous-marins voulez-vous (1 à 3)?",
                                               minvalue=1, maxvalue=3, parent=root)
        if nb_sousmarinA is None: # Annulé
            root.destroy()
            return

        for i in range(nb_sousmarinA):
            while True:
                # Utilise toujours la fonction console `choix_position` pour la saisie
                print(f"\nPlacement Joueur A - Sous-marin n°{i+1}:")
                sous_marin_positions = program.choix_position() 
                if joueur_A.placer_bateau(sous_marin_positions):
                    print("✅ Sous-marin ajouté.")
                    break
                else:
                    print("❌ Erreur : collision ou hors limites! Veuillez recommencer.")

        # Afficher la grille du joueur A (Propriétaire)
        message_var.set(f"Placement terminé. Grille de {joueur_A.nom}.")
        joueur_A.afficher_grille_proprietaire(game_frame)
        tk.messagebox.showinfo("Changement de Joueur", "Cliquez sur OK. Au tour de l'autre joueur pour placer ses bateaux.")
        
        # Placement Joueur B
        nb_sousmarinB = simpledialog.askinteger("Placement", f"{joueur_B.nom}, combien de sous-marins voulez-vous (taille 1 à 3)?",
                                               minvalue=1, maxvalue=3, parent=root)
        if nb_sousmarinB is None: # Annulé
            root.destroy()
            return
            
        for i in range(nb_sousmarinB):
            while True:
                print(f"\nPlacement Joueur B - Sous-marin n°{i+1}:")
                sous_marin_positions = program.choix_position()
                if joueur_B.placer_bateau(sous_marin_positions):
                    print("✅ Sous-marin ajouté.")
                    break
                else:
                    print("❌ Erreur : collision ou hors limites! Veuillez recommencer.")
                    
        # Afficher la grille du joueur B (Propriétaire)
        message_var.set(f"Placement terminé. Grille de {joueur_B.nom}.")
        joueur_B.afficher_grille_proprietaire(game_frame)
        tk.messagebox.showinfo("Prêt !", "La partie va commencer. Le joueur A commence.")

        # Passer au jeu
        prochain_tour()
        
    except Exception as e:
        # Gère l'erreur si l'utilisateur ferme la boîte de dialogue Tkinter
        print(f"Erreur/Annulation lors du placement : {e}")
        root.destroy()


def prochain_tour():
    """Prépare l'affichage et l'interaction pour le joueur actif."""
    global tour_joueur_index, tour_actif
    
    if not joueur_A.a_encore_bateaux() or not joueur_B.a_encore_bateaux():
        terminer_partie()
        return
        
    joueur_actif = joueurs[tour_joueur_index]
    joueur_cible = joueurs[1 - tour_joueur_index]
    
    message_var.set(f"💣 TOUR de {joueur_actif.nom}. Attaquez la grille de {joueur_cible.nom}!")
    
    # Afficher la grille CIBLE (boutons cliquables)
    joueur_cible.afficher_grille_cible(game_frame, tir_par_clic)
    
    tour_actif = True # Prêt à recevoir un clic
    

def tir_par_clic(prof, x_coord_tir, y_coord_tir):
    """Gère le tir après un clic sur un bouton de la grille cible."""
    global tour_joueur_index, tour_actif
    
    if not tour_actif:
        return # Empêche un double clic
        
    joueur_actif = joueurs[tour_joueur_index]
    joueur_cible = joueurs[1 - tour_joueur_index] 
    
    # Le joueur cible reçoit le tir
    resultat_tir = joueur_cible.recevoir_tir(prof, x_coord_tir, y_coord_tir)
    
    # Mise à jour du message
    message_var.set(f"Résultat du tir sur {joueur_cible.nom} en ({x_coord_tir}{y_coord_tir}, Prof {prof*100+100}): **{resultat_tir}**")
    
    # Désactiver les clics en attendant le changement de tour
    tour_actif = False
    
    # Vérification et passage au joueur suivant
    root.after(1500, lambda: passer_tour(joueur_cible)) # Attend 1.5 seconde avant de changer


def passer_tour(joueur_cible):
    """Termine le tour et passe au joueur suivant."""
    global tour_joueur_index
    
    # Vérification si la partie est terminée
    if not joueur_cible.a_encore_bateaux():
        terminer_partie()
        return

    # Changement de joueur
    tour_joueur_index = 1 - tour_joueur_index
    
    # Message de transition
    tk.messagebox.showinfo("Fin du Tour", f"Fin du tour. Au tour de {joueurs[tour_joueur_index].nom}.\nCliquez sur OK pour afficher sa grille d'attaque.")
    
    # Lancement du tour suivant
    prochain_tour()


def terminer_partie():
    """Affiche le gagnant et ferme l'application."""
    if joueur_A.a_encore_bateaux():
        gagnant = joueur_A.nom
    else:
        gagnant = joueur_B.nom
        
    message_var.set(f"PARTIE TERMINÉE ! Le **{gagnant}** GAGNE !")
    tk.messagebox.showinfo("FIN DE PARTIE", f"Félicitations au {gagnant} !")
    root.after(5000, root.destroy) # Ferme après 5 secondes

# --- Lancement du Programme ---

# Démarrer la phase de placement avant de lancer la boucle principale Tkinter
root.after(100, debuter_placement) 
root.mainloop() # Lance la fenêtre Tkinter