def Lns(N, largeurs):
    Lns = [[float('inf')] * (N+1) for _ in range(N+1)]
    for i in range(1, N+1):
        Lns[i][1] = min(largeurs[0:i])
        Lns[i][i] = sum(largeurs[:i])
    
    for i in range(2, N+1):
        for j in range(2, i):
            Lns[i][j] = min(Lns[i-1][j], sum(largeurs[i-j:i]))
    print(f"Lns : {Lns}")      
    return Lns


def findW(lMax,largeurs):
    N = len(largeurs)
    L = Lns(N, largeurs)
    w = None
    for j in range(1,N+1):
        if L[N][j] <= lMax:
            w = j
    print(f"matriceMaxW la taille maximale d'un sous ensemble de largeur <= {lMax} avec un carton est {w} \n ")

largeurs = [1,2,1,1,2,1,3,1]
findW(5,largeurs)
