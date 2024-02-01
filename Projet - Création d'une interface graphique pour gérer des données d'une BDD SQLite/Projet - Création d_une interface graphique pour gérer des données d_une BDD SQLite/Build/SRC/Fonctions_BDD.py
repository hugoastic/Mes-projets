import sqlite3
import bcrypt
import random
import math
import datetime
import os

def annee():
    """Generate a list of date using the list created before"""
    jm = [31,28,31,30,31,30,31,31,30,31,30,31]
    liste = []
    for mois in range(len(jm)): #pour chaque mois de l'anée
        for jour in range(jm[mois]): #pour chaque jour du mois
            liste.append(datetime.date(2020, mois+1, jour+1)) #ajoute la date au liste
    return(liste)

def genext(jour):
    """Generate a list of temperature trhoughout a day in a gaussian curve repartition rounded to 2 decimals with sigma = 6.
    It uses the .txt folder in the path 2 lines forward. """
    liste = []
    with open("temp ext 2021 moyenne par jour.txt", "r") as file: #importe le fichier en une variable nommée file
        newline_break = []
        for readline in file: #pour chaque ligne du fichier
            line = readline.strip() #enlève les espaces
            liste.append(float(line) - 2.5) #lie chaque ligne et les transforme en flottant (j'ai mit -5 pour garder une température 'réaliste' ) et les ajoute à une liste
    x = [round(random.gauss(int(round(liste[jour])),6),2) for y in range(48)] #Créer une liste de 48 températures autour de la température moyenne-5 sous forme de distribution Gaussienne avec un Sigma de 6
    x.sort() #Trie la liste de façon croissante pour l'utiliser plus tard dans notre gros programme
    return x

def gencapt(jour):
    """Generate a list of temperature trhoughout a day in a gaussian curve repartition rounded to 2 decimals with sigma = 2.
    It uses the .txt folder in the path 2 lines forward. """
    liste = []
    with open("temp ext 2021 moyenne par jour.txt", "r") as file: #importe le fichier en une variable nommée file
        newline_break = []
        for readline in file: #pour chaque ligne du fichier
            line = readline.strip() #enlève les espaces
            liste.append(float(line) - 7.5) #lie chaque ligne et les transforme en flottant (j'ai mit -5 pour garder une température 'réaliste' ) et les ajoute à une liste
    x = [round(random.gauss(int(round(liste[jour])),2),2) for y in range(48)] #Créer une liste de 48 températures autour de la température moyenne-5 sous forme de distribution Gaussienne avec un Sigma de 2
    x.sort() #Trie la liste de façon croissante pour l'utiliser plus tard dans notre gros programme
    return x

def reorga(listeaveragetemp,tempperday=48):
    """ Sort a list in a ascendant way for id 0 to n/2
       and in a descendant way from n/2+1 to n """
    liste = []
    """ Réparition des valeurs des relevés de température dans une journée type : """
    for i in range(int(tempperday / 2)) :
        liste.append(listeaveragetemp[i * 2])
    for i in range(int(tempperday / 2)):
        liste.append(listeaveragetemp[-(i * 2 + 1)])
    return liste

def generation(stadename):
    """Generate temperature data for a stade with a name 'stadename' """
    hour = ["00:00","00:30","01:00","01:30","02:00","02:30","03:00","03:30","04:00","04:30","05:00",
    "05:30","06:00","06:30","07:00","07:30","08:00","08:30","09:00","09:30","10:00","10:30","11:00",
    "11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00",
    "17:30","18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00","22:30","23:00","23:30"]
    listage = annee() #génère la liste des dates
    count = 0
    cnx = sqlite3.connect("..\\SRC\\stade.db") #connection à la BDD
    for date in listage: #pour chaque date
        listtempcaptor = reorga(gencapt(count)) #génère la liste des températures moyenne des capteur dans la journée
        listtempcaptorext = reorga(genext(count)) #génère la liste des températures moyenne extérieur sur la journée
        count += 1
        for horaire in range(len(hour)) : #pour chaque 30 min
            listeid = list(cnx.execute("Select idCapteur from Capteurs where idStade=(Select idStade from Stades where nomStade=?)",(stadename,))) #récupère la liste des id des capteurs
            for id in listeid:
                tempext = listtempcaptorext[horaire]
                tempcapt = round(listtempcaptor[horaire]+random.random(),2) #génère une température avec une petite variation (entre 0 et 1) pour chaque capteur
                cnx.execute("insert into Releve (idCapteur,datereleve,heurereleve,tempext,tempcapt) values (?,?,?,?,?)",(id[0],date,hour[horaire],tempext,tempcapt)) #insère les valeurs dans la BDD
    cnx.commit()
    cnx.close()

def captorgenerator(stadename,nombrecapteur):
    """Generate 'nombre capteur' capteur data for a stade with a name 'stadename' """
    captorlist = []
    conn = sqlite3.connect("..\\SRC\\stade.db") #connection à la BDD
    cursor = conn.cursor()
    """delete existing captor of the stade"""
    cursor.execute("delete from Capteurs where idStade=(Select idStade from Stades where nomStade=?)",(stadename,)) #supprime les capteurs de la BDD
    cursor.execute("SELECT longueur,largeur FROM Stades WHERE nomStade=?",(stadename,)) #récupère les dimensions du stade
    longueur , largeur = cursor.fetchone()
    nx = round(math.sqrt((longueur / largeur) *nombrecapteur + (longueur-largeur) * (longueur-largeur) / (2 * largeur)) - ((longueur-largeur) / (2*largeur))) + 1 #calcule le nombre de capteur en x
    ny = round(nombrecapteur / nx) #calcule le nombre de capteur en y
    deltax = longueur / (nx + 1) #calcule la distance entre chaque capteur en x
    deltay = largeur / (ny + 1) #calcule la distance entre chaque capteur en y
    coordx = deltax #initialise les coordonnées en x
    coordy = deltay #initialise les coordonnées en y
    captorlist = []
    for i in range(nx): #pour chaque capteur en x
        for j in range(ny): #pour chaque capteur en y
            position ='pas def' #initialise la position
            if coordx >= 0 and coordx < longueur / 4: #si la coordonnée en x est dans le premier quart du stade
                position='externe gauche' #la position est externe gauche
            elif coordx >= longueur / 4 and coordx < longueur / 2: #de même pour les prochains positions
                position='centre gauche'
            elif coordx >= longueur / 2 and coordx < (3 * longueur / 4):
                position='centre droit'
            elif coordx >= (3 * longueur / 4) and coordx<= longueur:
                position='externe droit'
            captorlist.append((position,round(coordx),round(coordy))) #ajoute la position et les coordonnées du capteur dans la liste
            coordy += deltay #incrémente les coordonnées en y
        coordx += deltax #incrémente les coordonnées en x
        coordy = deltay #remet les coordonnées en y à 0
    conn.close()
    return captorlist

def implementcaptorindatabase(stadename,numbercaptor):
    """Implement "numbercaptor" captor in "stadename" into the database using captorlist function"""
    captorlist = captorgenerator(stadename,numbercaptor) #génère la liste des capteurs
    conn = sqlite3.connect("..\\SRC\\stade.db") #connection à la BDD
    cursor = conn.cursor()
    cursor.execute("SELECT idStade FROM Stades WHERE nomStade=?",(stadename,)) #récupère l'id du stade
    idStade = cursor.fetchone()[0]
    for captor in captorlist:
        cursor.execute("INSERT INTO Capteurs(Position, Cordx, Cordy, idStade) VALUES (?,?,?,?)",(captor[0],captor[1],captor[2],idStade)) #insère les capteurs dans la BDD
    conn.commit()
    conn.close()

def implementstadeindatabase(stadename,length,width):
    """Implement a stade with a name "stadename" and a length "length" and a width "width" into the database"""
    conn = sqlite3.connect("..\\SRC\\stade.db") #connection à la BDD
    conn.execute("INSERT INTO Stades (nomStade,longueur,largeur) VALUES(?,?,?)",(stadename,length,width)) #insère le stade dans la BDD
    conn.commit()
    conn.close()

def implementutilisatordatabase(username,password,stadename):
    """Implement a user of "stadename" with a username "username" and a password "password" into the database"""
    conn = sqlite3.connect("..\\SRC\\stade.db") #connection à la BDD
    """select id stade of stadename"""
    cursor = conn.cursor()
    cursor.execute("SELECT idStade FROM Stades WHERE nomStade=?",(stadename,)) #récupère l'id du stade
    idStade = cursor.fetchone()[0]
    conn.execute("""INSERT INTO Authentification_interface(user,mdp,idstade)
    VALUES(?,?,?)""",(username,password,idStade)) #insère l'utilisateur dans la BDD
    conn.commit()
    conn.close()

def updateforeignzones(stadename):
    """Update the foreign zones of the captor from a stade with a name "stadename" in the database"""
    cnx = sqlite3.connect("..\\SRC\\stade.db") #connection à la BDD
    listeid = list(cnx.execute("Select idCapteur, Cordx from Capteurs where idStade=(Select idStade from Stades where nomStade=?)",(stadename,))) #récupère les id et les coordonnées des capteurs de la BDD
    listezone = list(cnx.execute("Select idZone, longueurdébut, longueurfin from Zones where idStade=(Select idStade from Stades where nomStade=?)",(stadename,))) #récupère les id et les coordonnées des zones de la BDD
    for id in listeid: #pour chaque capteur
        for zone in listezone: #pour chaque zone
            if id[1] >= zone[1] and id[1] <= zone[2]: #si la coordonnée en x du capteur est dans la zone
                cnx.execute("UPDATE Capteurs SET idZone=? WHERE idCapteur=?",(zone[0],id[0])) #met l'id de la zone dans la BDD
    cnx.commit()
    cnx.close()

def updatezones(nombrezones,stadename):
    """Update 'nombrezones' zones in the stade with a name "stadename" in the database"""
    cnx = sqlite3.connect("..\\SRC\\stade.db") #connection à la BDD
    """select if of stade"""
    cursor = cnx.cursor()
    cursor.execute("SELECT idStade FROM Stades WHERE nomStade=?",(stadename,)) #récupère l'id du stade
    idStade = cursor.fetchone()[0]
    stade = list(cnx.execute("Select longueur from Stades where idStade=?",(idStade,))) #récupère la longueur du stade
    longueur = stade[0][0] #récupère longueur du stade
    cnx.execute("DELETE FROM Zones WHERE idStade=?",(idStade,)) #supprime les zones précédentes de la BDD
    for zone in range(nombrezones): #pour chaque zone
        """insert new zones in database"""
        cnx.execute("INSERT INTO Zones(idStade, longueurdébut, longueurfin) VALUES (?,?,?)",(idStade,zone * longueur / nombrezones,(zone + 1) * longueur / nombrezones)) #insère les zones dans la BDD
    cnx.commit()
    cnx.close()

def interactusertozone():
    """ask for stadename and ask they whant to change the zones"""
    while True :
        stadename = input("Tapez sur 'entrée' pour annuler. Veuillez entrer le nom de votre stade :") #demande le nom du stade
        if not type(stadename) == str: #si le nom n'est pas une chaine de caractère
            print("Le nom du stade devrait être une chaine de caractères.") #affiche un message d'erreur
            continue
        elif stadename == "": #si le nom est vide
            return
        else:
            cnx = sqlite3.connect("..\\SRC\\stade.db") #connecte la BDD
            idStade = cnx.execute("SELECT idStade FROM Stades WHERE nomStade=?",(stadename,)).fetchone() #récupère l'id du stade
            if idStade == None: #si le stade n'est pas dans la BDD
                print("Le stade n'est pas dans la BDD") #affiche un message d'erreur
                continue
            else:
                print("Nom du stade confirmé:",stadename)
                break
    while True :
        answer = input("Voulez-vous changer les zones ? Tapez 'oui' pour changer les zones, tapez 'non' pour continuer sans changer les zones :") #demande si l'utilisateur veut changer les zones
        if answer == 'oui': #si l'utilisateur veut changer les zones
            while True :
                nombrezones = int(input("Combien de zones voulez-vous ?")) #demande le nombre de zones
                if not type(nombrezones) == int: #si le nombre de zones n'est pas un entier
                    print("Le nombre de zones devrait être un entier.") #affiche un message d'erreur
                    continue
                else:
                    print("Nombre de zones confirmé:",nombrezones) #affiche le nombre de zones
                    break
            updatezones(nombrezones,stadename) #met à jour les zones
            updateforeignzones(stadename) #met à jour les zones pour les capteurs
            break
        elif answer == 'non': #si l'utilisateur ne veut pas changer les zones
            break
        else:
            print("Veuillez répondre par oui ou non") #affiche un message d'erreur
            continue

def addstadeanduserinfo():
    """ask for stadename and ask they whant to add a stade and a user"""
    while True:
        stadename = input("Tapez sur 'entrée' pour annuler. Nom du stade: ") #demande le nom du stade
        if not type(stadename) == str: #si le nom n'est pas une chaine de caractère
            print("Le nom du stade devrait être une chaine de caractères.") #affiche un message d'erreur
            continue
        elif stadename == "": #si le nom est vide
            return
        else:
            cnx = sqlite3.connect("..\\SRC\\stade.db") #connecte la BDD
            idStade = cnx.execute("SELECT idStade FROM Stades WHERE nomStade=?",(stadename,)).fetchone() #récupère l'id du stade
            if idStade == None: #si le stade n'est pas dans la BDD
                print("Nom du stade confirmé:",stadename)
                break
            else:
                print("Stade déjà existant") #affiche un message d'erreur
                continue
    while True:
        length = input("Longueur: ") #demande la longueur du stade
        if not length.isdigit(): #si la longueur n'est pas un nombre
            print("Ceci n'est pas un nombre") #affiche un message d'erreur
            continue
        else:
            print("Longueur confirmée:",length) #affiche la longueur du stade
            break
    while True:
        width = input("Largeur: ") #demande la largeur du stade
        if not width.isdigit(): #si la largeur n'est pas un nombre
            print("Ceci n'est pas un nombre") #affiche un message d'erreur
            continue
        else:
            print("Largeur confirmée:",width) #affiche la largeur du stade
            break
    while True:
        username = input("Nom d'utilisateur: ") #demande le nom d'utilisateur
        if not type(username) == str: #si le nom d'utilisateur n'est pas une chaine de caractère
            print("Le nom d'utilisateur devrait être une chaine de caractères.") #affiche un message d'erreur
            continue
        else:
            print("Nom d'utilisateur confirmé:",username) #affiche le nom d'utilisateur
            break
    while True:
        password = input("Mot de passe crypé par l'utilisateur en bcrypt: ") #demande le mot de passe
        password2 = input("Confirmation du mot de passe bcrypt: ") #demande la confirmation du mot de passe
        if not password == password2: #si les mots de passe ne sont pas identiques
            print("Les mots de passe ne sont pas identiques.") #affiche un message d'erreur
            continue
        else:
            print("Mot de passe confirmé") #affiche le mot de passe
            break
    print("votre stade aura 4 zones et 12 capteurs par défaut") #affiche un message d'information
    while True :
        x = input("Appuyez sur entrer pour fermer la fenêtre") #demande l'appui sur entrer pour fermer la fenêtre
        break
    implementstadeindatabase(stadename,length,width) #implemente le stade dans la BDD
    implementutilisatordatabase(username,password,stadename) #implemente l'utilisateur dans la BDD
    implementcaptorindatabase(stadename,12) #implemente les capteurs dans la BDD
    updatezones(4,stadename) #met à jour les zones
    updateforeignzones(stadename) #met à jour les zones pour les capteurs

def interactusertocaptor():
    """ask for stadename and ask they whant to change the captor"""
    while True :
        stadename = input("Tapez sur 'entrée' pour annuler. Veuillez entrer le nom de votre stade :") #demande le nom du stade
        if not type(stadename) == str: #si le nom n'est pas une chaine de caractère
            print("Le nom du stade devrait être une chaine de caractères.") #affiche un message d'erreur
            continue
        elif stadename == '': #si l'utilisateur a annulé
            return
        else:
            cnx = sqlite3.connect("..\\SRC\\stade.db") #connecte la BDD
            idStade = cnx.execute("SELECT idStade FROM Stades WHERE nomStade=?",(stadename,)).fetchone() #récupère l'id du stade
            if idStade == None: #si le stade n'est pas dans la BDD
                print("Le stade n'est pas dans la BDD") #affiche un message d'erreur
                continue
            else:
                print("Nom du stade confirmé:",stadename)
                break
    while True :
        nombrecapteurs = int(input("Combien de capteurs possède votre stade ?")) #demande le nombre de capteurs
        if not type(nombrecapteurs) == int: #si le nombre de capteurs n'est pas un entier
            print("Le nombre de capteurs devrait être un entier.") #affiche un message d'erreur
            continue
        else:
            print("Nombre de capteurs confirmé:",nombrecapteurs) #affiche le nombre de capteurs
            break
    print("veuillez notez que les températures seront mises à 0") #affiche un message d'information
    while True :
        reponse = input("Appuyez sur entrer pour fermer la fenêtre, pour annulez tapez 'annuler' ") #demande l'appui sur entrer pour fermer la fenêtre
        if reponse == 'annuler': #si l'utilisateur veut annuler
            break #sort de la boucle
        elif reponse == "": #si l'utilisateur appuie sur entrer
            cnx = sqlite3.connect("..\\SRC\\stade.db") #connecte la BDD
            idStade = cnx.execute("SELECT idStade FROM Stades WHERE nomStade=?",(stadename,)).fetchone()[0] #récupère l'id du stade
            """delete temperature of soon deleted captors"""
            cnx.execute("DELETE FROM Releve WHERE idCapteur IN (SELECT idCapteur FROM Capteurs WHERE idStade=?)",(idStade,)) #supprime les relevés des capteurs supprimés
            cnx.execute("DELETE FROM Capteurs WHERE idStade=?",(idStade,)) #supprime les capteurs
            cnx.commit() #sauvegarde les changements
            cnx.close() #ferme la BDD
            implementcaptorindatabase(stadename,nombrecapteurs) #implemente les capteurs dans la BDD
            updateforeignzones(stadename) #met à jour les zones pour les capteurs
            break

def interactusertotemperaturedata():
    """generate data temperature for test purposes on your stade"""
    while True :
        stadename = input("Tapez sur 'entrée' pour annuler. Veuillez entrer le nom de votre stade :") #demande le nom du stade
        if not type(stadename) == str: #si le nom n'est pas une chaine de caractère
            print("Le nom du stade devrait être une chaine de caractères.") #affiche un message d'erreur
            continue
        elif stadename == '': #si l'utilisateur a annulé
            return
        else:
            cnx = sqlite3.connect("..\\SRC\\stade.db") #connecte la BDD
            idStade = cnx.execute("SELECT idStade FROM Stades WHERE nomStade=?",(stadename,)).fetchone() #récupère l'id du stade
            if idStade == None: #si le stade n'est pas dans la BDD
                print("Le stade n'est pas dans la BDD") #affiche un message d'erreur
                continue
            else:
                print("Nom du stade confirmé:",stadename)
                break
    while True :
        test = input("voulez vous générer une année type de données ? (oui/non)") #demande si l'utilisateur veut générer des données
        if test == 'oui': #si l'utilisateur veut générer des données
            generation(stadename)
            break
        elif test == 'non': #si l'utilisateur ne veut pas générer des données
            break
        else:
            print("veuillez entrer 'oui' ou 'non'") #affiche un message d'erreur
            continue

def getpath(dbname): #Cette fonction est gardée de côté si le chemin d'accès de la BDD ne fonctionne pas
    """get the path of the BDD for a sqlite database"""
    path = os.path.dirname(os.path.abspath(__file__)) #get the path of the file
    path = os.path.join(path,dbname) #join the path of the file and the name of the BDD
    return path #return the path of the BDD





