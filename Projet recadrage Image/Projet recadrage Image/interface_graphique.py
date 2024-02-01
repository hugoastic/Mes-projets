# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 22:33:27 2023

@author: Hugo
"""

#Préliminaires:
    
from tkinter import*
from tkinter import ttk
import tkinter.messagebox
import tkinter.filedialog
from PIL import Image, ImageTk
import os
import numpy as np
import time
from math import *
import random
import sys#pour l'éxécution en .bat du fichier python


#Variables:
ROUGE=0
VERT=1
BLEU=2

#-----------------FONCTIONS--------------------------


def interface():
    #fonctions pour la gestion de l'interface graphique et l'affichage de toutes les fonctionnalités de l'appli
    global interface,canvas
    global datarecadr, datatassage, dataveines
    global typtassage
    global Photo_canvas
    global dimension
    
    interface = Tk()#création et définition  de l'interface
    interface.resizable(width=False, height=False)#on fixe la taille de la fenêtre pour faire en sorte que l'utilisateur ne puisse pas la grossir
    interface.title("Imag'app")
    interface.geometry("950x600")
    interface.iconbitmap("icon.ico")#on ne met pas le chemin en enteir car le module os permet ici de chercher le fichier dans le même dossier que le programme python
    
    LF1=LabelFrame(interface, text="Image",labelanchor="n",height=400).pack(fill="both", expand="yes")
    LF3=LabelFrame(interface, text="Recadrage",labelanchor="n",height=50).pack(fill="both", expand="yes")
    LF4=LabelFrame(interface,text="Tassage",labelanchor="n",height=50).pack(fill="both",expand="yes")
    LF5=LabelFrame(interface,text="Seam Carving",labelanchor="n",height=50).pack(fill="both",expand="yes")
    
    #On crée une barre de menu pour pouvoir importer et enregistrer des images mais aussi pour pouvoir quitter l'app
    menuBar = Menu (LF1)
    menuFichier  = Menu(menuBar, tearoff = 0)
    menuBar.add_cascade(label="Fichier",menu=menuFichier)
    menuFichier.add_command(label="Ouvrir",command=importer)
    menuFichier.add_command(label="Enregistrer sous",command=enregistrer)
    menuFichier.add_separator()
    menuFichier.add_command(label="Quitter",command=interface.destroy)
    
    menuEdition  = Menu(menuBar, tearoff = 1) 
    menuBar.add_cascade(label="Edition",menu=menuEdition)
    menuEdition.add_command(label="Retour image origine",command=annuler)
    menuEdition.add_separator()
    menuEdition.add_command(label="Afficher veines verticales",command=Afficher_veines_verticales)
    menuEdition.add_command(label="Afficher veines horizontales",command=Afficher_veines_horizontales)
    
    menuOutils  = Menu(menuBar, tearoff = 1) 
    menuBar.add_cascade(label="Outils",menu=menuOutils)
    menuOutils.add_command(label="Supprimer un objet",command=Supprimer_Objet)
    
    
    #Boutons pour recadrer l'image
    Button(interface, text="Recadrage Centre", width=20, height=1, bg="grey",command=recadrageCentre).place(x=30,y=430)
    Button(interface, text="Recadrage Droit", width=20, height=1, bg="grey",command=recadrageDroit).place(x=300,y=430)
    Button(interface, text="Recadrage Gauche", width=20, height=1, bg="grey",command=recadrageGauche).place(x=570,y=430)

    #Bouton pour le tassage de l'image
    Button(interface, text="Tassage", width=20, height=1, bg="grey",command=tassage).place(x=700,y=485)
    #Bouton pour passer en noir et blanc
    Button(interface, text="Mettre image en noir et blanc", width=25, height=1, bg="grey",command=TableauEnergie_vers_imageNB).place(x=15,y=542)
    
    Label(LF4, text ="Vertical ou horizontal").place(x=325,y=490)
    Frame(LF4,typetassage()).propagate(0)#Zone de sélection du tassage vertical ou horizontal
    
    #Zone de texte pour permettre à l'utilisateur de choisir la longueur du carré recadré
    datarecadr=IntVar()
    Label(LF3, text ="Largeur du carré ").place(x=780,y=430)
    Entry(interface,textvariable=datarecadr,width="7").place(x=880,y=430)
    
    
    #Zone de texte pour entrer le nombre de lignes à delete
    datatassage=IntVar()
    Label(LF4, text ="Enlever 1 ligne/colonne toutes les ").place(x=14,y=492)
    Entry(interface,textvariable=datatassage,width="5").place(x=200,y=492)
    
    #Boutons et zone texte pour les veines
    Button(interface, text="Effacer veines verticales", width=23, height=1, bg="grey",command=Veines).place(x=250,y=542)
    Button(interface, text="Effacer veines horizontales", width=25, height=1, bg="grey",command=Veines_horizontale).place(x=450,y=542)
    dataveines=IntVar()
    Label(LF5, text ="Nombre de veines:").place(x=700,y=544)
    Entry(interface,textvariable=dataveines,width="5").place(x=810,y=546)
    
    
    #Création du Canvas pour afficher l'image en cours de modification
    canvas = Canvas(interface, width=950, height=340)
    canvas.place(x=20,y=20)
    photo=PhotoImage(file="No_Image.ppm")
    Photo_canvas=canvas.create_image(450,180,anchor=CENTER,image=photo)
    
    #Affichage des dimensions de l'image en cours de modification
    dimension= StringVar()
    dimensions_image = Label(interface, textvariable=dimension)
    dimensions_image.place(x=457,y=375)
    dimension.set("0 x 0")
    
    
    interface.config(menu = menuBar)#on fait afficher la barre de menu
    interface.mainloop()#on affiche l'interface graphique
    
    
    
def afficher_image(lien):#programme pour modifier l'image du canvas et l'afficher dans le canvas
    global photo2
    photo2=PhotoImage(file=lien)
    if len(tableauf3)>340 or len(tableauf3[0])>950: #si la taille de l'image dépasse les dimensions du canvas
        photo2=photo2.subsample(2)#subsample(2) permet de dézoomer de moitié sur l'image
        canvas.update()
    canvas.itemconfigure(Photo_canvas,image=photo2)
    
   
    largeur=len(tableauf3[0])#on en profite pour mettre à jour les dimensions de l'image
    hauteur=len(tableauf3)
    dim=str(largeur)+"x"+str(hauteur)
    dimension.set(dim)
    

def importer():
    global lien,tableauf3#on partage le lien du dossier importé avec les autres fonctions
    lien = tkinter.filedialog.askopenfilename(title="Ouvrir une image",filetypes=[('all files','.*')]) 
    tableauf3=matrice_image(lien)   
    afficher_image(lien) 
    #De plus dans cette fonction on partage le tableauf3 pour que la matrice correspondante ne soit calculée que une seule fois et que chaque modificatio
    #ne se fasse que sur le tableau précédent
    
    
def annuler():#Si on veut retourner à l'image initiale on peut utiliser ce bouton 'ex: mauvaise manip)
    global tableauf3
    tableauf3=matrice_image(lien)   
    afficher_image(lien) 
    largeur=len(tableauf3[0])
    hauteur=len(tableauf3)
    dim=str(largeur)+"x"+str(hauteur)
    dimension.set(dim)
    

def lecture_hautlarg(lien):#on lit la hauteur et la largeur de l'image
    fichier=open(lien, "rb")
    lignes=[next(fichier) for x in range(3)]
    fichier.close()
    hlarg=lignes[1].split()
    return int(hlarg[0]),int(hlarg[1])


def lecture_image(lien):#on transforme les pixels de l'image pmp en tableau de valeur comprise entre 0 et 255
    fichier=open(lien, "rb")
    ligne=fichier.read()
    liste=[]
    for lignes in ligne:
        liste.append(lignes)
    fichier.close()

    indice=0
    for i in range(len(liste)):# on pose que les pixels sont précédes à chq fois du caractère 255 et d'un saut de ligne
        #on se sert de cela pour créer une séparation entre les dimensions et les pixels en ascii
        if liste[i-3]==50 and liste[i-1]==liste[i-2]==53 and liste[i]==liste[i-4]==10 and i>indice :
            indice=i
    del liste[0:indice+1]
    tableau=np.asarray(liste,dtype="ubyte")
    return tableau 



def matrice_image(lien):    #Pour ouvrir une image et créer un tableau de l'image
    larghaut=lecture_hautlarg(lien)
    tableau=lecture_image(lien)
    tableau2=tableau.reshape(larghaut[1],larghaut[0],3)#on modifie la taille de notre tableau de pixels
    return tableau2


def tableau_vers_image(tableauf3,lienw):#pour retransformer notre tableau en image
    with open(lienw, "wb") as fichier:
        fichier.write(b"P6")
        fichier.write(b'\n')
        fichier.write(str(tableauf3.shape[1]).encode('ascii'))#largeur
        fichier.write(b" ")
        fichier.write(str(tableauf3.shape[0]).encode('ascii'))#hauteur
        fichier.write(b"\n")
        fichier.write(b"255")
        fichier.write(b"\n")
        fichier.write(tableauf3.tobytes())
        fichier.close()

    
def enregistrer():
     #Pour enregistrer une image modifiée sous un nouveau fichier
     filename = tkinter.filedialog.asksaveasfilename(title="Enregistrer une image",filetypes=[('all files','.*')])
     tableau_vers_image(tableauf3,filename)




def recadrageCentre(): #en enlevant de chaque côté 
#Remarque: on aurait pu recadrer avec un rectanlge et donnant la possibilité à l'utilisateur de choisir la largeur mais aussi la longueur ici cela reviendrait juste à modifier la supprssion des pixels sur les colonnes
    global tableauf3#dans toute nos fonctions qui suivront le tableau final généré par ces fonctions s'appelera tableauf3 
    n=len(tableauf3)
    m=len(tableauf3[0])
    LongueurVoulue=datarecadr.get()
    if LongueurVoulue<=min(n,m) and LongueurVoulue>0:
        nbelemsup=(n-LongueurVoulue)//2+(n-LongueurVoulue)%2#nombre d'éléments à supprimer sur une ligne
        nbelemsup2=(m-LongueurVoulue)//2+(m-LongueurVoulue)%2#nombre d'éléments à supprimer sur une colonne
        tableauf3=np.delete(tableauf3,np.s_[:nbelemsup],0) # on supprime les lignes en trop avant le carré
        tableauf3=np.delete(tableauf3,np.s_[:nbelemsup2],1) # on supprime les colonnes en trop avant le carré
        tableauf3=np.delete(tableauf3,np.s_[LongueurVoulue:],0) # on supprime les lignes en trop après le carré
        tableauf3=np.delete(tableauf3,np.s_[LongueurVoulue:],1) # on supprime les colonnes en trop après le carré
        
        #on pré-enregistre l'image dans un fichie texte pour pouvoir l'afficher par la suite dans notre cadre canvas
        tableau_vers_image(tableauf3,"sauvegarde.txt")
        afficher_image("sauvegarde.txt")
    

        
def recadrageGauche(): #en enlevant du côté gauche, même processus que pour le recadrageCentre
    global tableauf3
    n=len(tableauf3)
    m=len(tableauf3[0])
    LongueurVoulue=datarecadr.get()
    if LongueurVoulue<=min(n,m) and LongueurVoulue>0:
        nbelemsup=n-LongueurVoulue#on determine le nombre de ligne de pixels à supprimer
        nbelemsup2=m-LongueurVoulue#et pour les colonnes...
        tableauf3=np.delete(tableauf3,np.s_[:nbelemsup],0)#on s'intéresse aux lignes à supprimer
        tableauf3=np.delete(tableauf3,np.s_[:nbelemsup2],1)#on s'intéresse aux colonnes à supprimer
        
        tableau_vers_image(tableauf3,"sauvegarde.txt")
        afficher_image("sauvegarde.txt")
    
         
def recadrageDroit(): #en enlevant du coté droit même programme que le recadrage gauche
    global tableauf3
    n=len(tableauf3)
    m=len(tableauf3[0])
    LongueurVoulue=datarecadr.get()
    if LongueurVoulue<=min(n,m) and LongueurVoulue>0:
        nbelemsup=n-LongueurVoulue
        nbelemsup2=m-LongueurVoulue
        tableauf3=np.delete(tableauf3,np.s_[n-nbelemsup:n],0)# on parcourt le tableau de la dernière ligne en revenant vers la première
        tableauf3=np.delete(tableauf3,np.s_[m-nbelemsup2:m],1)
        
        tableau_vers_image(tableauf3,"sauvegarde.txt")
        afficher_image("sauvegarde.txt")
    

def typetassage():
    global typtassage
    def action(event):#fonction pour prendre l'information du type de tassage
        global tassagevh
        tassagevh = typtassage.get()

    typtassage=ttk.Combobox(interface, values=["vertical","horizontal"])#liste déroulante   
    typtassage.place(x=460,y=490)      
    typtassage.bind("<<ComboboxSelected>>", action) #Permet de prendre en compte à chaque instant la modification de la combobox
    
    
def tassage():
    global tableauf3
    n=datatassage.get()#on récupère l'information donnée par la liste déroulant
    if tassagevh=="vertical":
        if n>=1:
            tableauf3=np.delete(tableauf3,np.s_[::n],1)#1 pour signifier qu'on travaille sur les colonnes, on supprime une colonne sur n
            tableau_vers_image(tableauf3,"sauvegarde.txt")
            afficher_image("sauvegarde.txt")
            
    if tassagevh=="horizontal":
        if n>=1:
            tableauf3=np.delete(tableauf3,np.s_[::n],0)#0 pour signifier qu'on travaille sur les lignes
            tableau_vers_image(tableauf3,"sauvegarde.txt")
            afficher_image("sauvegarde.txt")
        
    
def RVBx(tableau,x,y,couleur):#pour créer une moyenne d'énergie avec les pixels précédents et suivants (soit les pixels qui entourent ce pixel)
    l=len(tableau)-1
    i0=x-1
    i1=x+1
    if x==0:
        i0=l
    if x==l:
        i1=0
    a=tableau[i0,y,couleur]#les couleurs ont été définies au préalable en haut du programme dans variables
    b=tableau[i1,y,couleur]
    if a>b :
        c=a-b
    else:
        c=b-a
    return(c)#pour avoir un c positif

def RVBy(tableau,x,y,couleur):#pour créer une moyenne d'énergie avec les pixels du dessous et du dessus
    l=len(tableau[0])-1
    i0=y-1
    i1=y+1
    if y==0:
        i0=l
    if y==l:
        i1=0
    a=tableau[x,i0,couleur]
    b=tableau[x,i1,couleur]
    if a>b :
        c=a-b
    else:
        c=b-a
    return(c)


def TableauEnergie(tableau,mode="normal"):#on crée un tableau d'énergie(l'energie dépend des valeurs RVB de chaque pixel)
    global maxenergie

    if mode=="normal":#tableau d'énergie normal pour les  veines
        energie=0
        tabenerg=np.asarray([])
        maxenergie=0
        for ligne in range (0,len(tableau)):
            for colonne in range(0,len(tableau[ligne])):  # on calcule le pixel de la première ligne ayant la plus faible énergie
                energie=RVBx(tableau,ligne,colonne,ROUGE)**2+RVBx(tableau,ligne,colonne,BLEU)**2+RVBx(tableau,ligne,colonne,VERT)**2+RVBy(tableau,ligne,colonne,ROUGE)**2+RVBy(tableau,ligne,colonne,VERT)**2+RVBy(tableau,ligne,colonne,BLEU)**2
                #on utlises la formule du calcule d'énergie totale pour un pixel
                tabenerg=np.append(tabenerg,int(energie))
                if energie>maxenergie:
                    maxenergie=int(energie)#pour implémenter la valeur d'énergie maximale
        tabenerg=tabenerg.reshape(len(tableau),len(tableau[0]))
        tabenerg=np.asarray(tabenerg,dtype="int32")
        return tabenerg
    
    if mode=="suppression":#pour mettre des valeurs d'énergies très petite aux pixels rouge et ainsi permettre la suppresion de la zone en roige par la suite
        energie=0
        tabenerg=np.asarray([])
        maxenergie=0
        pixels_ref_todelete=np.array([255,0,0])#pixel de reference ici rouge
        for ligne in range (0,len(tableau)):
            for colonne in range(0,len(tableau[ligne])):  # on parcourt tout le tableau et dès que un pixel rouge est rencontré on lui met une energie très très faible
                if np.array_equal(tableau[ligne][colonne],pixels_ref_todelete)==True:
                    tabenerg=np.append(tabenerg,int(-300000))
                else:   
                    energie=RVBx(tableau,ligne,colonne,ROUGE)**2+RVBx(tableau,ligne,colonne,BLEU)**2+RVBx(tableau,ligne,colonne,VERT)**2+RVBy(tableau,ligne,colonne,ROUGE)**2+RVBy(tableau,ligne,colonne,VERT)**2+RVBy(tableau,ligne,colonne,BLEU)**2
                    #on utlises la formule du calcule d'énergie totale pour un pixel
                    tabenerg=np.append(tabenerg,int(energie))
                if energie>maxenergie:#on récupère la valeur d'energie max
                    maxenergie=int(energie)
            
        tabenerg=tabenerg.reshape(len(tableau),len(tableau[0]))
        tabenerg=np.asarray(tabenerg,dtype="int32")
        return tabenerg



def TableauEnergie_vers_imageNB():
    #transformer la matrice energie vers un tableau Noir et Blanc 
    global tableauf3
    tableauf=TableauEnergie(tableauf3)
    tableauf3=np.array([])
    for ligne in range(0,len(tableauf)):
        for colonne in range(0,len(tableauf[0])):
            RVB=0
            RVB=1000*(int(tableauf[ligne][colonne]))//maxenergie#on peut augmenter le 255 pour augmenter la visibilité du blanc
            #la formule précédente est un simple produit en croix
            for compteur in range(0,3):
                tableauf3=np.append(tableauf3,int(RVB))
    tableauf3=tableauf3.reshape(len(tableauf),len(tableauf[0]),3)
    tableauf3=np.asarray(tableauf3,dtype="ubyte")
    #on pré-enregistre l'image dans un fichie texte pour pouvoir l'afficher par la suite dans notre cadre canvas
    tableau_vers_image(tableauf3,"sauvegarde.txt")
    afficher_image("sauvegarde.txt")



def Recherche_Veine(tableau):#on procède ici par dijstra et on mettra comme tableau d'entrée le tableau d'énergie
    tableau_energie_tot=np.copy(tableau)
    tableau_energie_tot=np.asarray(tableau_energie_tot,dtype="int32")
    #Dans cette partie on crée un nouveau tableau d'energie correspondant à la somme minimale des energies précedentes
    for ligne in range(0,len(tableau)):
        for colonne in range(0,len(tableau[0])):
            if ligne==0:
                pass
            elif colonne==0:
                energie_pixel=int(tableau_energie_tot[ligne][colonne])+min(int(tableau_energie_tot[ligne-1][colonne]),int(tableau_energie_tot[ligne-1][colonne+1]))
                tableau_energie_tot[ligne][colonne]=energie_pixel
                    
            elif colonne==(len(tableau[0])-1):
                energie_pixel=int(tableau_energie_tot[ligne][colonne])+min(int(tableau_energie_tot[ligne-1][colonne-1]),int(tableau_energie_tot[ligne-1][colonne]))
                tableau_energie_tot[ligne][colonne]=energie_pixel
            
            else:
                energie_pixel=int(tableau_energie_tot[ligne][colonne])+min(int(tableau_energie_tot[ligne-1][colonne-1]),int(tableau_energie_tot[ligne-1][colonne]),int(tableau_energie_tot[ligne-1][colonne+1]))
                tableau_energie_tot[ligne][colonne]=energie_pixel

    #on remonte dans le tableau pour trouver la veine optimale
    liste_coord_min=np.array([])
    for ligne in reversed(range(0,len(tableau_energie_tot))):#on parcourt dans le sens inverse pour la remontée du dikjstra
        
        #On récupère la plus petite energie et l'indice de la colonne qui a été sommé donc on parcourt le tableau d'énergie dans le sens inverse
        if ligne==len(tableau_energie_tot)-1:
            min_energie=tableau_energie_tot[len(tableau_energie_tot)-1][0]
            ligne_actuelle=ligne
            liste_energmin_colonne=np.array([])
            for colonne in range(0,len(tableau_energie_tot[0])):
                if tableau_energie_tot[len(tableau_energie_tot)-1][colonne]<=min_energie:
                    min_energie=tableau_energie_tot[len(tableau_energie_tot)-1][colonne]

             #on a récupéré précedemment la plus petite energie possible dans le tableau
             #maintenant on va regarder si il y a plusieurs veines avec cette même energie pour en choisir une aléatoirement
            for colonne in range(0,len(tableau_energie_tot[0])):
                if tableau_energie_tot[len(tableau_energie_tot)-1][colonne]==min_energie:
                    liste_energmin_colonne=np.append(liste_energmin_colonne,colonne)
            min_colonne=np.random.choice(liste_energmin_colonne,1)
            colonne_actuelle=int(min_colonne[0])
            liste_coord_min=np.append(liste_coord_min,(ligne_actuelle,colonne_actuelle))
        #on remonte ici les lignes du tableau en prenant en compte les 3 cas possibles: si on est sur un des bords de l'image ou pas   
        elif colonne_actuelle==0:
            for rang in range(0,2):
                if tableau_energie_tot[ligne_actuelle][colonne_actuelle]==tableau[ligne_actuelle][colonne_actuelle]+tableau_energie_tot[ligne_actuelle-1][colonne_actuelle+rang]:
                    liste_coord_min=np.append(liste_coord_min,(ligne_actuelle-1,colonne_actuelle+rang))
                    ligne_actuelle=ligne_actuelle-1
                    colonne_actuelle=colonne_actuelle+rang
                    break#pour éviter de faire cette boucle plusieurs fois si le programme peut passer par 2 chemins de même énergie
        
                    
        elif colonne_actuelle==(len(tableau_energie_tot[0])-1):
            for rang in range(0,2):
                if tableau_energie_tot[ligne_actuelle][colonne_actuelle]==tableau[ligne_actuelle][colonne_actuelle]+tableau_energie_tot[ligne_actuelle-1][colonne_actuelle+rang-1]:
                    liste_coord_min=np.append(liste_coord_min,(ligne_actuelle-1,colonne_actuelle+rang-1))
                    ligne_actuelle=ligne_actuelle-1
                    colonne_actuelle=colonne_actuelle+rang-1
                    break
        else:
              
            for rang in range(0,3): 
                if tableau_energie_tot[ligne_actuelle][colonne_actuelle]==tableau[ligne_actuelle][colonne_actuelle]+tableau_energie_tot[ligne_actuelle-1][colonne_actuelle+rang-1]:
                    liste_coord_min=np.append(liste_coord_min,(ligne_actuelle-1,colonne_actuelle+rang-1))
                    ligne_actuelle=ligne_actuelle-1
                    colonne_actuelle=colonne_actuelle+rang-1
                    break
                    
    liste_coord_min=np.asarray(liste_coord_min,dtype="int32")
    liste_coord_min=liste_coord_min.reshape(len(tableau),2)
    return liste_coord_min      #on retourne la liste de coordonnées de plus petite energie
   
        
def Afficher_veines_verticales(): #on crée une copie de tableauf3 pour ne pas le modifier mais seulement afficher les veines 
    veines_voulues=dataveines.get()
    tableauveines=np.copy(tableauf3)
   
    for veines in range(0,veines_voulues):
        coord_veines=Recherche_Veine(TableauEnergie(tableauveines))
        #Pour afficher les veines en rouge
        for longueur in range (0,len(coord_veines)):
            x=int(coord_veines[longueur][0])
            y=int(coord_veines[longueur][1])
            tableauveines[x,y,ROUGE]=255
            tableauveines[x,y,VERT]=0
            tableauveines[x,y,BLEU]=0
    tableau_vers_image(tableauveines,"sauvegarde.txt")
    afficher_image("sauvegarde.txt")
    
    
def Afficher_veines_horizontales(): #on procède de la même manière par rapport à au dessus sauf qu'il faut bien penser à inverser en utilisant la transposée notre tableau car la fonction 
                                    #Recherche veine ne trouve les veines qu'à la verticale
    veines_voulues=dataveines.get()
    tableauveines=np.copy(tableauf3)
    tableauveines=np.transpose(tableauveines,(1,0,2))#on transopose les lignes et les colonnes sans touché à la 3e dimension d'où le (1,0,2)
    
    for veines in range(0,veines_voulues):
        coord_veines=Recherche_Veine(TableauEnergie(tableauveines))
         #Pour afficher les veines en rouge
        for longueur in range (0,len(coord_veines)):
            x=int(coord_veines[longueur][0])
            y=int(coord_veines[longueur][1])
            tableauveines[x,y,ROUGE]=255
            tableauveines[x,y,VERT]=0
            tableauveines[x,y,BLEU]=0
    tableauveines=np.transpose(tableauveines,(1,0,2))#une fois la veine trouvée on "retourne" notre tableau pour retrouver le tableau initial
    tableau_vers_image(tableauveines,"sauvegarde.txt")
    afficher_image("sauvegarde.txt")





def Veines(typeveine="verticale"):#supprimer les selon le type choisit par l'utilisatuer mais ici on le met par défault en mode vertical
    global tableauf3    
    veines_voulues=dataveines.get()

    if typeveine=="suppression":
        veines_voulues=1 #on initialise le nombre de veines voules pour la suppression à 1 car le programme sera appélé en récursif

    for veines in range(0,veines_voulues):
        global tableauf3
        if typeveine=="horizontale":#en mode horizontale on pense bien à transposé le tableau
            tableauf3=np.transpose(tableauf3,(1,0,2))
            
        if typeveine=="suppression":#on veut supprimer les veines verticales avec le mode suppression d'objet donc avec le tableau d'energie spécifique à la suppression d'objets
            coord_veines=Recherche_Veine(TableauEnergie(tableauf3,"suppression"))

        else:
            coord_veines=Recherche_Veine(TableauEnergie(tableauf3))
            
        #Maintenant on veut supprimer les veines
        hauteur=len(tableauf3)
        largeur=len(tableauf3[0])
        coord_veines=np.flip(coord_veines)#on inverse le tableau pour le faire commencer par le début de notre image cependant notre liste de coordonées ne sera plus (ligne,colonne) mais (colonne,ligne)
        
        tableau_modif=np.array([])
        for coord in range(0,len(coord_veines)):#on va copier chaque ligne de notre tableau dans un nouveau tableau
        #avant de copier la ligne dans le nouveau tableau, on récupère seulement la ligne et on va enlever le pixel de la ligne en cours de traitement correspondant à la veine calculée. 
            ligne_en_cours=np.array([])
            ligne_en_cours=np.append(ligne_en_cours,tableauf3[coord])
            ligne_en_cours=ligne_en_cours.reshape(len(tableauf3[0]),3)
            ligne_en_cours=np.delete(ligne_en_cours,coord_veines[coord][0],0)
            tableau_modif=np.append(tableau_modif,ligne_en_cours) 
           
        if typeveine=="horizontale":
            tableau_modif=np.asarray(tableau_modif,dtype="int32")
            tableauf3=np.copy(tableau_modif)
            tableauf3=tableauf3.reshape(hauteur,largeur-1,3)
            tableauf3=np.transpose(tableauf3,(1,0,2))#on pense bien ici à transposer notre tableau car nous avons travaillé précedemment sur un tableau transposé
            tableauf3=np.asarray(tableauf3,dtype="ubyte")
            tableau_vers_image(tableauf3,"sauvegarde.txt")
            afficher_image("sauvegarde.txt")
            
        elif typeveine=="verticale" or typeveine=="suppression":
            tableau_modif=np.asarray(tableau_modif,dtype="int32")
            tableauf3=np.copy(tableau_modif)
            tableauf3=tableauf3.reshape(hauteur,largeur-1,3)
            tableauf3=np.asarray(tableauf3,dtype="ubyte")
            if typeveine=="suppression" :
                pixels_ref_todelete=np.array([255,0,0])#pixel de reference ici rouge
                for ligne in range (0,len(tableauf3)):
                    for colonne in range(0,len(tableauf3[0])):  #tant que un pixel rouge est dans le tableau on appelle la fonction en récursif pour supprimer des veines
                        if np.array_equal(tableauf3[ligne][colonne],pixels_ref_todelete)==True:#on cherche les pixels rouges
                            Veines("suppression")
                        else:pass
            tableau_vers_image(tableauf3,"sauvegarde.txt")
            afficher_image("sauvegarde.txt")
                        
    
def Veines_horizontale():
    global tableauf3
    Veines("horizontale")#suppression des veines en mode horizontal


def Supprimer_Objet():
    #L'objectif est de supprimer un objet qui a été colorié en rouge ou autre couleur différentiable des autres par l'utilisateur au préalable sur un éditeur d'image
    global tableauf3
    Veines("suppression")
    
    


#--------------------------Programme principal----------------------------------  
    
interface()
    
    
