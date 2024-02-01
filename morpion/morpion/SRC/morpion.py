# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 19:23:36 2022

@author: Hugo ASTIC
"""
from random import*
import time
import sys


def afficher_grille(Grille):
    print("    a   b   c")
    for j in range(0, 3):
        print("   --- --- ---")
        print("  |   |   |   |")
        print(j+1, end='')
        for i in range(3):
            print(" | "+str(Grille[j][i]), end='')
        print(" |")
        print("  |   |   |   |")
    print("   --- --- ---")


def grille_complete(Grille):
    a = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if Grille[i][j] != "-":
                a += 1
    if a == 9:
        return True
    else:
        return False


def grille_gagnante(Grille):
    if Grille[0] == ["x", "x", "x"] or Grille[0] == ["o", "o", "o"]:  # sur les lignes
        return True
    elif Grille[1] == ["x", "x", "x"] or Grille[1] == ["o", "o", "o"]:
        return True
    elif Grille[2] == ["x", "x", "x"] or Grille[2] == ["o", "o", "o"]:
        return True

    elif Grille[0][0] == Grille[1][0] == Grille[2][0] == "x" or Grille[0][0] == Grille[1][0] == Grille[2][0] == "o":  # sur les colonnes
        return True
    elif Grille[0][1] == Grille[1][1] == Grille[2][1] == "x" or Grille[0][1] == Grille[1][1] == Grille[2][1] == "o":
        return True
    elif Grille[0][2] == Grille[1][2] == Grille[2][2] == "x" or Grille[0][2] == Grille[1][2] == Grille[2][2] == "o":
        return True

    elif Grille[0][0] == Grille[1][1] == Grille[2][2] == "x" or Grille[0][0] == Grille[1][1] == Grille[2][2] == "o":  # sur les deux diagonales
        return True
    elif Grille[0][2] == Grille[1][1] == Grille[2][0] == "x" or Grille[0][2] == Grille[1][1] == Grille[2][0] == "o":
        return True
    else:
        return False


def process(s):
    c, l = 4, 4
    for i in s:#on parcourt notre chaine de caractères pour trouver toutes les occurences ou les fautes de frappe
        if i not in "abcABC,;.123":
            return False
        elif i in "a" or i in "A":
            c = 0
        elif i in "b" or i in "B":
            c = 1
        elif i in "c" or i in "C":
            c = 2
        elif i in "1":
            l = 0
        elif i in "2":
            l = 1
        elif i in "3":
            l = 2
    if c == 4 or l == 4:
        return False
    else:
        tup = (l, c)
        return tup


def jouer_à_2():
    Grille = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]
    joueur1 = input("Entrer nom du joueur 1:")
    joueur2 = input("Entrer nom du joueur 2:")
    aleat = randint(1, 2) #un petit tirage au sort pour éviter la dispute entre les deux joueurs
    if aleat == 1:
        début = str(joueur1)
        fin = str(joueur2)
    else:
        début = str(joueur2)
        fin = str(joueur1)
    print("C'est", début, "qui commence\n")
    afficher_grille(Grille)

    tour = 0
    while (grille_complete(Grille) == False) and (grille_gagnante(Grille) == False):

        if (tour % 2) == 0:  # tour du joueur sélectionné en prems
            print(début, end=", \n")
            s = input(
                "veuillez entrer les coordonées souhaitées pour placer votre x:")
            coord = process(s)
            while coord == False or Grille[coord[0]][coord[1]] != "-":
                s = input(
                    "Veuillez entrer les coordonées correctes souhaitées pour placer votre x:")
                coord = process(s)
            Grille[coord[0]][coord[1]] = "x"

        elif (tour % 2) != 0:  # tour du second joueur
            print(fin, end=",\n")
            s = input(
                "veuillez entrer les coordonées souhaitées pour placer votre o:")
            coord = process(s)
            while coord == False or Grille[coord[0]][coord[1]] != "-":
                s = input(
                    "veuillez entrer les coordonées correctes souhaitées pour placer votre o:")
                coord = process(s)
            Grille[coord[0]][coord[1]] = "o"

        afficher_grille(Grille)
        # pour éviter certains bug d'affichages dans la console...
        time.sleep(1)
        tour += 1

    if grille_gagnante(Grille) == True:
        if (tour % 2) == 0:  # on prend en compte le tour+=1 après que le joueur ait joué et avant de sortir de la boucle while
            gagnant = fin
        else:
            gagnant = début
        print("bien joué joueur", gagnant)
        time.sleep(1)
        sys.exit()#pour éviter de retourner, si une grille gagante est complète que le joueur a gagné et qu'il y a égalité

    elif grille_complete(Grille) == True:
        print("You're both too strong!!")
        time.sleep(1)






# CONTRE IA


def fils(grilleIA, evalMax):  # créeation des grille de jeux i+1 pour le noeud i
    grillefils = []
    listecoord = []
    if evalMax == False:#joueur qui joue
        car = "x"
    elif evalMax == True:#ordi qui joue
        car = "o"
    for i in range(len(grilleIA)):
        for j in range(len(grilleIA[i])):
            if grilleIA[i][j] == "-":#on récupère les coordonnées des emplacements vides
                listecoord.append([i, j])

    for k in range(len(listecoord)):
        grillecopie = []
        for l in range(3):  # on copie la liste des sous listes de la grille pour ne pas modifier notre grille initiale
            grillecopie.append(grilleIA[l][:])
        grillecopie[listecoord[k][0]][listecoord[k][1]] = car#on rajoute notre croix ou rond
        grillefils.append(grillecopie)#on retourne une liste de tous les fils possibles pour un noeud

    return grillefils,listecoord


# notre grille gagnante ne marche pas pour le minmax car il vérifie si l'ordi OU LE JOUEUR ont gagné

    
def grille_gagne_perdIA(Grille,car):
    if Grille[0] == [car,car,car]:  # sur les lignes
        return True
    elif Grille[1] == [car,car,car]:
        return True
    elif Grille[2] == [car,car,car]:
        return True

    elif Grille[0][0] == Grille[1][0] == Grille[2][0] == car:  # sur les colonnes
        return True
    elif Grille[0][1] == Grille[1][1] == Grille[2][1] == car:
        return True
    elif Grille[0][2] == Grille[1][2] == Grille[2][2] == car:
        return True

    elif Grille[0][0] == Grille[1][1] == Grille[2][2] == car:  # sur les deux diagonales
        return True
    elif Grille[0][2] == Grille[1][1] == Grille[2][0] == car:
        return True
    else:
        return False


def evaluation(noeud):
    if grille_gagne_perdIA(noeud,"o"):#si l'IA a gagné
        return 1
    elif grille_gagne_perdIA(noeud,"x"):#si le joueur a gagné
        return -1
    elif grille_complete(noeud):
        return 0


def nombre_fils(Grille):  # on compte le nombre de fils possible pour pouvoir faire pour tous l'appel récursif avec Minmax
    a = 0
    for i in range(len(Grille)):
        for j in range(len(Grille[i])):
            if Grille[i][j] == "-":
                a += 1
    return a


def Minmax(grille, profondeur, evalMax:bool):
    
    if profondeur == 0 or grille_gagnante(grille) or grille_complete(grille):
        return evaluation(grille),None #on rajoute None pour éviter si évaluation ne retourne rien que le programme plante
    else:
        I=[]
        
        for i in range(nombre_fils(grille)):#appel récursif du minmax du fils suivant ici les indices permettent de ne choisir que les listes possibles de fils
            I.append(Minmax(fils(grille, evalMax)[0][i], profondeur-1, not evalMax)[0])#car dans fils()on renvoi et les coordonnées et la liste de fils
            
        if evalMax:
            
            for i in range(len(I)):
                if I[i]==max(I):
                    return max(I), fils(grille, evalMax)[1][i]#on retourne maintenant les coordonnées renvoyées par fils()
                    
        else:
            for i in range(len(I)):
                if I[i]==min(I):
                    return min(I),fils(grille, evalMax)[1][i]
              




def jouer_contre_ordi():
    Grille = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]  # grille de jeu
    début = str(input("Entrer nom du joueur :"))
    fin = "Fabrice l'IA"
    afficher_grille(Grille)
    tour = 0
    
    
    while (grille_complete(Grille) == False) and (grille_gagnante(Grille) == False):

        if (tour % 2) == 0:  # tour du joueur début qui joue "x"
            print(début, end=", \n")
            s = input(
                "veuillez entrer les coordonées souhaitées pour placer votre x:")
            coord = process(s)
            while coord == False or Grille[coord[0]][coord[1]] != "-":
                s = input("Veuillez entrer les coordonées correctes souhaitées pour placer votre x:")
                coord = process(s)
            Grille[coord[0]][coord[1]] = "x"

        elif (tour % 2) != 0:  # tour de l'ordi qui joue "o"
            print(fin, end=",\n")
            a=Minmax(Grille, 8, True)[1]
            Grille[a[0]][a[1]] = "o"

        afficher_grille(Grille)
        # pour éviter certains bug d'affichages dans la console...
        time.sleep(1)
        tour += 1


    if grille_gagnante(Grille) == True:
        if (tour % 2) == 0:  # on prend en compte le tour+=1 après que le joueur ait joué et avant de sortir de la boucle while
            gagnant = fin
        else:
            gagnant = début
        print("bien joué joueur", gagnant)
        time.sleep(1)
        sys.exit()#on ferme la fenêtre


    elif grille_complete(Grille) == True:
        print("You're both too strong!!")
        time.sleep(1)

        


def type_jeux():
    jeu=str(input("Jouer contre ordi  ou  Jouer à deux:"))
    if jeu=="Jouer contre ordi":
        jouer_contre_ordi()
    elif jeu=="Jouer à deux":
        jouer_à_2()
        
type_jeux()