from easygopigo3 import EasyGoPiGo3
import socket
import time
import os
from math import *
import threading
from threading import Thread, Lock, Event

#pour les sockets et la communication avec le serveur
Adresse = "192.168.0.2"
Port = 12345


#initialisation des coordonnées initiales utilisées par la suite pour optimiser la fonction orientation()
xnext,ynext=0,0

#Ici on definit un prefixe plus court que EasyGoPiGo3 pour notre programme
gpg = EasyGoPiGo3()

#premièrement on initialise le sensor de distance du robot et le moteur pour faire tourner le capteur de distance
#initialisation de la variable problem_capt si probème de détection du capteur
distance = gpg.init_distance_sensor()
    
servo=gpg.init_servo("SERVO1")
servo.reset_servo()

#ensuite on va definir pour notre programme une distance de sécurité qui si elle est dépassée fera s'arreter le robot 
safe_distance=120

#on fixe la vitesse du robot
gpg.set_speed(400)


########Programmes récupération données du routeur#######

def GetTargetPosition():
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.connect((Adresse,Port))
    GTP = bytes("GTP","utf-8")
    serveur.send(GTP)

    f = serveur.recv(100)
    f = f.decode()

    f = f.split()
    f[0] =f[0][0:len(f[0])-1]
    f[0] = float(f[0])
    f[1] = float(f[1])
    return f

def GetBluePosition():
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.connect((Adresse,Port))
    GBP = bytes("GBP","utf-8")
    serveur.send(GBP)

    f = serveur.recv(100)
    f = f.decode()

    f = f.split()
    f[0] =f[0][0:len(f[0])-1]
    f[0] = float(f[0])
    f[1] = float(f[1])
    return f

def GetGreenPosition():
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.connect((Adresse,Port))
    GGP = bytes("GGP","utf-8")
    serveur.send(GGP)

    f = serveur.recv(100)
    f = f.decode()

    f = f.split()
    f[0] =f[0][0:len(f[0])-1]
    f[0] = float(f[0])
    f[1] = float(f[1])
    return f

def GetStarted():
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serveur.connect((Adresse,Port))
    GBS = bytes("GBS","utf-8")
    serveur.send(GBS)

    f = serveur.recv(100)
    f = f.decode()

    return int(f)



def orientation():
    global xnext,ynext
    #ici si c les premiers pas du robot on calcule une première fois les deux vecteurs pour le calcul
    #sinon on utilise la position précédente pour éviter de réavancer de 10 cm à chaque fois et ainsi perdre du temps
    if xnext==0 and ynext==0:
        x0,y0=GetBluePosition()[0],GetBluePosition()[1]
        gpg.drive_cm(7)  
        x1,y1=GetBluePosition()[0],GetBluePosition()[1]
        xt,yt=GetTargetPosition()[0],GetTargetPosition()[1]
    else:
        x0,y0=xnext,ynext
        x1,y1=GetBluePosition()[0],GetBluePosition()[1]
        xt,yt=GetTargetPosition()[0],GetTargetPosition()[1]
        
    v1,v2=(x1-x0),(y1-y0)
    w1,w2=(xt-x1),(yt-y1)
    teta2_rad=atan2((w2*v1-w1*v2),(w1*v1+w2*v2))#angle entre le vecteur v(vecteur robot) vers le vecteur w (vecteur cible)
    teta2=((180/pi)*teta2_rad)
    
    xnext,ynext=x1,y1
    gpg.turn_degrees(teta2*1.02)#on prend en compte les imprécisions mécaniques (moteurs) en appliquant un coeff multiplicatuer de 1,02
   

#######Programme mode threading#########

event=Event()

def jeu():
    global xtcible, ytcible
    gpg.set_eye_color((0,0,255))#allumer notre robot avec du bleu pour la détection via la webcam
    gpg.open_eyes()
    if GetStarted()==1:
        xtcible,ytcible=GetTargetPosition()[0],GetTargetPosition()[1]
        print(cible.is_alive(), evitement.is_alive(),ringthread.is_alive())
        if not cible.is_alive() or not evitement.is_alive() or not ringthread.is_alive():#si il y a un problème avec un des threads on passe alors en mode itératif avec la fonction de secours
            if not evitement.is_alive():#si le problème concerne le capteur de distance
                probleme_capt=1
            jeu_secours()
        while True:
            if event.is_set():
                break
            orientation()
            gpg.drive_cm(40)



xtcible,ytcible=GetTargetPosition()[0],GetTargetPosition()[1]

def changer_cible(x=xtcible,y=ytcible):
    global xtcible,ytcible,xnext,ynext
    time.sleep(0.1)
    if GetStarted()==1:
        time.sleep(0.15)
        xt2,yt2=GetTargetPosition()[0],GetTargetPosition()[1]
        time.sleep(0.05)
        if xt2!=x or yt2!=y:#on vérifie à chaque instant que la cible n'a pas bougé d'endroit
            print("cible")
            event.set()
            time.sleep(0.3)
            event.clear()
            with lock:
                gpg.stop()
                xtcible,ytcible=GetTargetPosition()[0],GetTargetPosition()[1]
                xnext,ynext=0,0 #pour éviter le problème avec l'orientation en même temps que le changement de cible
                jouer=threading.Thread(target=jeu)#on relance le threading de jeu
                jouer.start()
            changer_cible(xtcible,ytcible)
        else:
            time.sleep (0.2)
            changer_cible(xt2,yt2)


#initialisation de la variable problem_capt si problème de détection du capteur
probleme_capt=0

def manoeuvre_evitement():
    global probleme_capt, xnext,ynext
    if GetStarted()==1:
        dist=distance.read_mm()
    
        #si le capteur ne fonctionne pas on s'en passe
        if dist==type(None) and (probleme_capt==0):
            probleme_capt=1
            print("problem capt")
        
        xb,yb=GetBluePosition()[0],GetBluePosition()[1]
        xg,yg=GetGreenPosition()[0],GetGreenPosition()[1]
    
    #on veut éviter les collisions entre robots.
        if -120+xb<xg<120+xb and -120+yb<yg<120+yb and robot_presence==1:
            print("autre robot")
            event.set()
            time.sleep(0.3)
            with lock:
                gpg.drive_cm(-5)
                time.sleep(0.5)
                gpg.turn_degrees(90)
                xnext,ynext=0,0
                time.sleep(0.5)
                event.clear()
                jouer=threading.Thread(target=jeu)
                jouer.start()
            manoeuvre_evitement()
                
    #si on est proche d'un obstacle
        elif dist<safe_distance and probleme_capt==0:
            print('passé par là')
            gpg.stop()
            event.set()
            time.sleep(0.2)
            with lock:
                gpg.stop()
                servo.rotate_servo(50)#on fait bouger le capteur de distance à droite
                time.sleep(0.2)
                alpha=distance.read_mm()
                time.sleep(0.3)
                servo.rotate_servo(130)#on fait bouger le capteur de distance à gauche
                time.sleep(0.2)
                beta=distance.read_mm()
                time.sleep(0.3)
                servo.rotate_servo(90)#on remet le capteur à sa position initiale
                time.sleep(0.5)
                servo.reset_servo()
                if beta>alpha: #on choisit de trourner vers l'obstacle le plus loin
                    gpg.turn_degrees(-90)
                    gpg.drive_cm(30)
                else:
                    gpg.turn_degrees(90)
                    gpg.drive_cm(30)
                    
                time.sleep(0.5)
                event.clear()
                jouer=threading.Thread(target=jeu)
                jouer.start()
            manoeuvre_evitement()
        else:
            time.sleep(0.2)
            manoeuvre_evitement()


def ring():#On fait en sorte que le robot ne sorte pas du ring
    if GetSarted()==1:
        xb,yb=GetBluePosition()[0],GetBluePosition()[1]
        if xb>1180 or yb >750 or xb<46 or yb<46:#utilisation de mesures faites sur le ring projeté sur le sol
            print("ring")
            event.set()
            time.sleep(0.3)
            with lock:
                gpg.turn_degrees(180)
                time.sleep(0.15)
                gpg.drive_cm(40)
                time.sleep(0.5)
                event.clear()
                jouer=threading.Thread(target=jeu)
                jouer.start()
            ring()
        else:
            time.sleep(0.2)
            ring()
            

########Programme de secours#############

def jeu_secours():
    global probleme_capt,xnext,ynext
    print("fonctions de secours")
    xnext,ynext=0,0
    event.set()
    with lock:
        while GetStarted()==1:
            orientation()
            gpg.drive_cm(5)
            if probleme_capt==0:
                dist = distance.read_mm()
                if dist < safe_distance:
                    evitement_objets_version_secours()
            

def evitement_objets_version_secours():
        gpg.stop()
        servo.rotate_servo(50)
        time.sleep(0.2)
        alpha=distance.read_mm()
        time.sleep(0.3)
        servo.rotate_servo(130)
        time.sleep(0.2)
        beta=distance.read_mm()
        time.sleep(0.3)
        servo.rotate_servo(90)
        time.sleep(0.5)
        print('passé par là')
        servo.reset_servo()
        if beta > alpha:
            gpg.turn_degrees(-90)
            gpg.drive_cm(10)
        else:
            gpg.turn_degrees(90)
            gpg.drive_cm(10)


robot_presence=int(input("Eviter les collisions avec le robot adverse? Si oui tapez 1 sinon 0"))

lock=Lock()

def Wait_start():#on attend que le programme nous dises de démarrer
    while True:
        if GetStarted()==1:
            break
Wait_start()

cible=threading.Thread(target=changer_cible)
cible.start()

evitement=threading.Thread(target= manoeuvre_evitement)
evitement.start()

ringthread=threading.Thread(target=ring)
ringthread.start()

jouer=threading.Thread(target=jeu)
jouer.start()
