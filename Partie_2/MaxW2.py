
def Lns(N, largeurs):
    Lns = [[float('inf')] * (N+1) for _ in range(N+1)]
    for i in range(1, N+1):
        Lns[i][1] = min(largeurs[0:i])
        for j in range(1,i):
            premierCarton = sum(largeurs[:j])
            deuxiemeCarton = sum(largeurs[j:i]) 
            Lns[i][i] = min(Lns[i][i],max(premierCarton,deuxiemeCarton))
    
    for i in range(2, N+1):
        for j in range(2, i):
            largeur_max = float("inf")
            for k in range(0, j):
                #premierCarton = sum(largeurs[i-j:i-j+k])
                deuxiemeCarton = sum(largeurs[i-j+k:i])
                taille = len(largeurs[i-j:i-j+k])
                for m in range(0,i-j+k-taille+1):
                    premierCarton = sum(largeurs[m:m+taille])
                    largeur_max = min(largeur_max,max(premierCarton, deuxiemeCarton))
            Lns[i][j] = min(Lns[i][j],min(Lns[i-1][j], largeur_max))
    print(f"matrice Lns avec 2 carton {Lns}")            
    return Lns



def findW(lMax,largeurs):
    N = len(largeurs)
    L = Lns(N, largeurs)
    w = 0
    for j in range(1,N+1):
        if L[N][j] <= lMax:
            w = j
        
    print(f"la taille maximale d'un sous ensemble de largeur <= {lMax} avec un carton est {w}")
    return w 
largeurs = [1,2,1,2,2,1,3,2]
findW(5,largeurs)


"""def Lns(N, largeurs):
    Lns = [[float('inf')] * (N+1) for _ in range(N+1)]
    for i in range(1, N+1):
        Lns[i][1] = min(largeurs[0:i])
        for j in range(1,i):
            premierCarton = sum(largeurs[:j])
            deuxiemeCarton = sum(largeurs[j:i])
            Lns[i][i] = min(Lns[i][i],max(premierCarton,deuxiemeCarton))
    
     
   
    for i in range(2, N+1):
        for j in range(2, i):
            for k in range(0, j):
                premierCarton = sum(largeurs[i-j:i-j+k+1])
                deuxiemeCarton = sum(largeurs[i-j+k+1:i])
                largeur_max = max(premierCarton, deuxiemeCarton)
                Lns[i][j] = min(Lns[i-1][j], largeur_max)
    return Lns


def findW(lMax,largeurs):
    N = len(largeurs)
    L = Lns(N, largeurs)
    w = None
    for j in range(1,N+1):
        if L[N][j] <= lMax:
            w = j
        print(L[N][j])
    print(f"la taille maximale d'un sous ensemble de largeur <= {lMax} avec un carton est {w}")
    return w

largeurs = [1,2,1,2,2,1,3,2] 
findW(5,largeurs)
"""
