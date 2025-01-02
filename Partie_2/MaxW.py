def calculer_Lns_2_cartons(N, L, largeurs):
    # Initialisation de la table Lns avec des valeurs infinies
    Lns = [[[float('inf')] * 3 for _ in range(N + 1)] for _ in range(N + 1)]

    # Initialisation des cas de base
    for i in range(1, N + 1):
        # Cas 1 : Ranger un seul objet (j = 1) dans un carton (k = 1)
        Lns[i][1][1] = min(largeurs[:i])
        
        # Cas 2 : Ranger tous les objets (j = i) dans un carton (k = 1)
        Lns[i][i][1] = sum(largeurs[:i])
        
        # Cas 3 : Ranger tous les objets (j = i) dans deux cartons (k = 2)
        for k in range(1, i):  # Essayer toutes les partitions
            largeur_1 = sum(largeurs[:k])  # Somme des objets dans le premier carton
            largeur_2 = sum(largeurs[k:])  # Somme des objets dans le second carton
            Lns[i][i][2] = min(Lns[i][i][2], max(largeur_1, largeur_2))

    # Remplissage pour k = 1 (un seul carton)
    for i in range(1, N + 1):
        for j in range(2, i + 1):
            for k in range(1, i - j + 2):
                Lns[i][j][1] = min(Lns[i][j][1], Lns[k][j - 1][1] + largeurs[i - 1])

    # Remplissage pour k = 2 (deux cartons)
    for i in range(1, N + 1):
        for j in range(2, i + 1):
            for k in range(1, i):  # Point de séparation
                for m in range(1, j):  # Objets dans le premier carton
                    largeur_1 = Lns[k][m][1]  # Largeur du premier carton
                    largeur_2 = Lns[i - k][j - m][1]  # Largeur du second carton
                    Lns[i][j][2] = min(Lns[i][j][2], max(largeur_1, largeur_2))

    # Trouver le maximum j tel que Lns(N, j, 2) <= L
    for j in range(N, 0, -1):
        if Lns[N][j][2] <= L:
            return j  # Nombre maximal d'objets pouvant être rangés dans 2 cartons

    return 0  # Si aucun objet ne peut être rangé
    
largeurs = [1, 2, 1, 2, 2,1,3,2]  # Largeurs des objets
L = 5  # Largeur maximale d'un carton
N = len(largeurs)

max_objets = calculer_Lns_2_cartons(N, L, largeurs)
print("Nombre maximal d'objets pouvant être rangés dans 2 cartons :", max_objets)
