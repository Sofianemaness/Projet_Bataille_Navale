def choix_position():
    position = []
    size = int(input("Choisissez la taille de votre sous marin, entre 1 et 3 cases: "))
    orientation = input("Vertical (V) ou horizontal (H): ")
    x = input('Choisissez la position X du début (de A à E): ')
    y = int(input('Choisissez la position Y du début (de 0 à 9): '))
    for i in range(size):
        position.append([x, y])
        if(orientation == 'V'):
            if(chr(ord(x) + 1) != 'F') : x = chr(ord(x) + 1) 
        else:
            if(y < 9) : y += 1
    return position

posJoueurA = choix_position()
posJoueurB = choix_position()