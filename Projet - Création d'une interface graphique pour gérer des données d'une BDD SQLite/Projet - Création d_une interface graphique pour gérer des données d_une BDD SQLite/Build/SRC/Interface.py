import bcrypt
from tkinter import*
import time
import sqlite3
from tkinter import ttk
from tkcalendar import*
import matplotlib.pyplot as plt 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import smtplib, ssl
import numpy as np
import datetime
import matplotlib.dates as mdates
import os



def login():
    global numeroStade #tout au long du programme le global permettra d'échanger des variables entre différentes fonctions
    global identifiant
    cnx=sqlite3.connect("..\\SRC\\stade.db")
    mdp = cnx.execute('select mdp from Authentification_interface')
    user = cnx.execute('select user from Authentification_interface')
    paswrd=password.get()#le mot de passe est velodrome pour marseille et prince pour paris
    
    listemdp=[]#création des listes de mdp et nom d'utilisateurs grâce aux données de la BDD
    for i in mdp:
        listemdp.append(i[0].encode())
    listename=[]
    for j in user:
       listename.append(j[0])
       
   
    
    #on va parcourir nos deux listes mdp et nom d'utilisateur et conparer  par rapport aux indices
    for k in range(len(listemdp)):
       for h in range(len(listename)):
           if k==h and identifiant==listename[h] and bcrypt.checkpw(paswrd.encode(), listemdp[k]):#on va decrypter le mot de passe pour la comparaison
               idname=str(identifiant)
               stade =cnx.execute('select idStade from Authentification_interface where user==?',(idname,))
               numeroStade=0
               for l in stade:
                   numeroStade+=l[0]
               time.sleep(0.5)
               login_screen.destroy()#on detruit cette première fenêtre
               interface_controle()#accès à l'interface de controle
           else:
               message.set("Mauvais mot de passe ou identifiant")
    cnx.close()


def interface_login():
    global login_screen
    
    login_screen = Tk()
    login_screen.resizable(width=False, height=False)
    login_screen.title("Anthentification Multistade App")
    login_screen.geometry("300x200")
    login_screen.iconbitmap("..\\SRC\\Icon_nlg_070815_17_174.ico")
    global message#pour le message d'erreur si mauvais mot de passe
    global password
    username=StringVar()#on crée 3 variables
    password=StringVar()
    message=StringVar()

    cnx=sqlite3.connect("..\\SRC\\stade.db")
    user = cnx.execute('select user from Authentification_interface')
    listename=[]
    listename.append(" ")
    for j in user: 
        listename.append(j[0])
    
    def actionliste(event):#information pour prendre l'identifiant'
        global identifiant
        identifiant = listename.get()
    # Création de la Combobox via la méthode ttk.Combobox()
    listename = ttk.Combobox(login_screen, values=listename,state='readonly')
    #  Choisir l'élément qui s'affiche par défaut
    listename.current(0)   
    listename.place(x=130,y=42)
    listename.bind("<<ComboboxSelected>>", actionliste)#au clic, récupère le nom du stade grâce au .get
    
    
    Label(login_screen, text="Nom d'utilisateur : ").place(x=20,y=40)
    Label(login_screen, text="Mot de passe : ").place(x=20,y=80)
    Entry(login_screen, textvariable=password ,show="*").place(x=110,y=82)
    Label(login_screen, text="",textvariable=message).place(x=95,y=100)
    Button(login_screen, text="Login", width=10, height=1, bg="grey",command=login).place(x=105,y=130)
    login_screen.mainloop()




def interface_controle():
    global interface,canvas
    global address
    global capteurinitial
    
    capteurinitial=12*numeroStade-11 #capteur initial pour afficher un premier graph au lancement
    
    interface = Tk()
    interface.resizable(width=False, height=False)#on fixe la taille de la fenêtre pour faire en sorte que l'utilisateur ne puisse pas la grossir
    interface.title("Multistade app")
    interface.geometry("950x600")
    interface.iconbitmap("..\\SRC\\Icon_nlg_070815_17_174.ico")
    
    LF1=LabelFrame(interface, text="Filtrage",labelanchor="nw").pack(fill="both", expand="yes")
    LF2=LabelFrame(interface, text="Gestion des données du graphique par capteur",labelanchor="nw").pack(fill="both", expand="yes")
    
    Frame(LF1, calendrier(190,50)).propagate(0)#début et fin pour les dates
    Label(LF1, text ="Debut").place(x=190,y=20)
    Label(LF1, text ="Fin").place(x=370,y=20)
    
    Frame(interface,listedéroulante()).propagate(0)
    Frame(interface,conversiontemp()).propagate(0)
    
    
    canvas = Canvas(interface, width=100, height=100).place(x=100,y=500)
    Frame(interface, graphique(capteur=capteurinitial,date1="2020-05-22",date2="2020-05-22",infoconversion="Celsius"))
    
    
    Label(interface,text="Adresse Gmail :").place(x=800,y=140)
    address = StringVar()
    Entry(interface,textvariable=address,width="30").place(x=750,y=160)
    
    Button(interface,text="Afficher toutes les zones",command=fonctionprintgraphzones).place(x=800,y=10)
    
    interface.mainloop()
    
       
    
def calendrier(a,b):
    global entry_date1,entry_date2
    def actioncalendrier(): #actualise le graphique avec les 2 nouvelles dates et les autres variables données par les autres fonctions du programme
        global listetemp,listecapteur
        global capteur,infoconversion
        date1=entry_date1.get()
        date2=entry_date2.get()
        infoconversion = listetemp.get()
        capteur=listecapteur.get()
        clear_plot()
        act_graphique(capteur,date1,date2,infoconversion)
    
    def actiontableaux():#permet d'afficher le tableau de donnée en fonction des exigences fournies par l'utilisateur
        date1=entry_date1.get()
        date2=entry_date2.get()
        infoconversion = listetemp.get()
        capteur=listecapteur.get()
        tableaux_print(capteur,date1,date2,infoconversion)
        
        
    entry_date1_label = Label(interface, text="Cliquer sur la date voulue")
    entry_date1 = DateEntry(interface,selectmode = 'day', date_pattern="y-mm-dd",
                   year = 2020, month = 5, 
                   day = 22)
    entry_date1.place(x=a,y=b)
    entry_date2_label = Label(interface, text="Cliquer sur la date voulue")
    entry_date2 = DateEntry(interface,selectmode = 'day', date_pattern="y-mm-dd",
                   year = 2020, month = 5, 
                   day = 22)
    entry_date2.place(x=a+150,y=b)
    
    btn_submit= Button(interface, text='Actualiser graphique',command= actioncalendrier).place(x=800,y=45)
    btn_submit2= Button(interface, text='Afficher le tableau ',command= actiontableaux).place(x=800,y=80)



def conversiontemp(): # cette fonction permet de créer une variable indiquant quelle est l'unité de température selectionnée par l'utilisateur
    global listetemp
    labelChoix = Label(interface, text = "Températures ").place(x=10,y=20)
    def actiontemp(event):#fonction pour prendre l'information de conversion
        global infoconversion
        infoconversion = listetemp.get()

    listetemp = ttk.Combobox(interface, values=["Celsius","Farenheit"])#liste déroulante
    listetemp.current(0)   
    listetemp.place(x=10,y=50)
    listetemp.bind("<<ComboboxSelected>>", actiontemp)
    



def listedéroulante():
    global listecapteur
    labelChoix = Label(interface, text = "Veuillez faire un choix de capteur ").place(x=500,y=20)
    
    def actionliste(event):#information pour prendre la valeur du capteur
        global capteur
        capteur = listecapteur.get()
           
        
    # création de la liste Python contenant les éléments de la liste Combobox
    cnx=sqlite3.connect("..\\SRC\\stade.db")
    z=cnx.cursor()
    idcapteur=z.execute('select idCapteur from Capteurs,Zones where Zones.idZone=Capteurs.idZone and Zones.idStade==?',(numeroStade,))
    listecapteur=[]
    i=1
    for j in idcapteur:
        if i<=12:
            listecapteur.append(j[0])
            i+=1
        
    # Création de la Combobox via la méthode ttk.Combobox()
    listecapteur = ttk.Combobox(interface, values=listecapteur,state='readonly')
    
    #  Choisir l'élément qui s'affiche par défaut
    listecapteur.current(0)
        
    listecapteur.place(x=500,y=50)
    listecapteur.bind("<<ComboboxSelected>>", actionliste)#au clic, récupère le numéro du capteur grâce au .get
    
    
    

def clear_plot():#fonction permettant de clear le graphique pour en afficher un nouveau
    global output
    if output:
        output.get_tk_widget().destroy()
      
    
    
    
def graphique(capteur,date1="2020-05-22",date2="2020-05-22",infoconversion="Celsius"):
    global fig,output
    global maxtemp,mintemp
    global temp2
    
    if capteur==None:
        capteur=capteurinitial
    
    date=(capteur,numeroStade,date1,date2)
    cnx=sqlite3.connect("..\\SRC\\stade.db")
    z=cnx.cursor()
    z.execute('select dateReleve,heurereleve,tempcapt from Releve,Capteurs,Zones where Zones.idZone=Capteurs.idZone and Capteurs.idCapteur=Releve.idCapteur and Releve.idCapteur==? and Zones.idStade==? and dateReleve between ? and ?  order by Releve.idCapteur ASC',date)
    
    data=z.fetchall()#récupère les valeurs voulues et crée une liste de tuplets de valeurs
    
    jour_heure= [date+hour for (date, hour, value) in data]
    temp = [value for (date, hour, value) in data]
    

    #on convertit ou non les températures en fonction de ce que l'utilisateur a indiqué à l'interface
    temp2=[] 
    if str(infoconversion)==str("Farenheit"):
        temp2.clear()
        for i in range(len(temp)):
            a=(temp[i]*1.8)+32
            temp2.append(a)
    
    elif str(infoconversion)==str("Celsius"):
        temp2.clear()
        temp2=temp
    
    #Tracé du graph
    fig = Figure(figsize = (50,5), dpi = 70)
    plot1 = fig.add_subplot(111)
    plot1.set_ylabel("Température")
    
    #affichage propre des dates qur l'axe des abscisses
    date=jour_heure[:]#copie de liste
    #transformation du format de la date en np.datetime64
    for i in range (len(date)):
        date[i]=date[i][:10]+"T"+date[i][10:]+":00Z"
        date[i]=np.datetime64(date[i])
    #pour incliner les labels
    for label in plot1.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')
    #gestion des label x
    cdf = mdates.ConciseDateFormatter(plot1.xaxis.get_major_locator())
    
    plot1.set_title("Graphique de l'évolution de la température pour un capteur",loc="left")
    plot1.plot(date,temp2)
    plot1.plot(date,temp2,"o",label=capteur) 
    plot1.legend(loc="upper left")#légende et label du graph pour indiquer de quel capteur il s'agit
    
    output = FigureCanvasTkAgg(fig, master = interface)   
    output.draw() 
    output.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(output , interface).place(x=550,y=250)#pour afficher une barre de naviguation
    
    #Minimum, Max et moyenne et affichage de ces données
    mintemp=round(min(temp2),1)
    maxtemp=round(max(temp2),1)
    s=0
    for i in range (len(temp2)):
        s+=temp2[i]
    moytemp=round(s/i,1)
    Label(interface, text=maxtemp).place(x=150,y=160)
    Label(interface, text="Maximum").place(x=50,y=160)
    Label(interface, text=moytemp).place(x=150,y=180)
    Label(interface, text="Moyenne").place(x=50,y=180)
    Label(interface, text=mintemp).place(x=150,y=200)
    Label(interface, text="Minimum").place(x=50,y=200)
    
    debord()#fonction pour créer une limite pour les valeurs min et max
    
    cnx.close()
    
    
    
def debord():
    global temp2,mintemp,maxtemp
    
    def afficherDebord():
        
        selectedMax=str(varMax.get())
        selectedMin=str(varMin.get())
        c=0
        for i in range(len(temp2)): #on compare les valeurs de débords voulues par l'utilisateur avec les valeurs min et max calculées avec le capteur sur une période
            
            if (float(temp2[i])>float(selectedMax)): 
                c+=1
            if (float(temp2[i])<float(selectedMin)):
                c+=1
        if c!=0:
            send_message()
                
    varMax=DoubleVar()
    varMin=DoubleVar()
    
    Label(interface, text="Débords des valeurs de température").place(x=340,y=140)
    
    #on créer les deux échelles pour selectionner les valeurs min et max de débord
    Label(interface, text="Maximum").place(x=510,y=160)
    scaleMax = Scale(interface,orient='horizontal',variable=varMax, from_=mintemp-10,to=maxtemp+10,resolution=0.1,length=150).place(x=480,y=180)
   
    Label(interface, text="Minimum").place(x=310,y=160)
    scaleMin = Scale(interface,orient='horizontal',variable=varMin, from_=mintemp-10,to=maxtemp+10,resolution=0.1,length=150).place(x=280,y=180)
   
    Button(interface, text="Prendre débords", command=afficherDebord).place(x=800,y=190)
    
    
    
def send_message():#aeehkvreverwrsow   est le mot de passe créé pour ma boite mail google
    global address
    address_info = address.get()
    email_body_info = "Attention_capteurs_stades"
    print(address_info,email_body_info)
    sender_email = "hugo.astic07@gmail.com"  
    sender_password = "aeehkvreverwrsow" # pour ma boite mail et non mdp de mon compte google
    #ce mot de passe se trouve en allant dans les paramètres du compte google puis ensuite il faut trouver
    #l'onglet créer un mdp d'applications
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(sender_email,sender_password)
    print("Login successful")
    server.sendmail(sender_email,address_info,email_body_info)
    print("Message sent")




def tableaux(capteur,date1="2020-05-22",date2="2020-05-22",infoconversion="Celsius"):  
    

    if capteur==None: #si pas de valeur de capteur alors on prend la première valeur de capteur de stade calculée dans une fonction précédente
        capteur=capteurinitial    

    tableau = Tk()
    tableau .title('Tableaux de valeurs')
    tableau .geometry('1220x225')
    tableau.iconbitmap("..\\SRC\\Icon_nlg_070815_17_174.ico")
    tableau .resizable(width=False, height=False)
    columns = ('Capteur','Zone', 'date','heure','tempcapt', 'tempext')
    
    tree = ttk.Treeview(tableau , columns=columns, show='headings')
    
    tree.heading('Capteur', text='Capteur')
    tree.heading('Zone', text='Zone')
    tree.heading('date', text='date a-m-j')
    tree.heading('heure', text='heure')
    tree.heading('tempcapt', text='température capteur')
    tree.heading('tempext', text='température extérieure')
    
    
    date=(capteur,numeroStade,date1,date2)
    cnx=sqlite3.connect("..\\SRC\\stade.db")
    z=cnx.cursor()
    z.execute('select Releve.idCapteur,Capteurs.idZone,dateReleve,heurereleve,tempcapt,tempext from Releve,Capteurs,Zones where Zones.idZone=Capteurs.idZone and Capteurs.idCapteur=Releve.idCapteur and Releve.idCapteur==? and Zones.idStade==? and dateReleve between ? and ?  order by dateReleve ASC ',date)
    capteur=z.fetchall()
    idcapteur=[idcap for (idcap,idZ,date, hour, tempcap,tempext) in capteur]
    idzone=[idZ for (idcap,idZ,date, hour, tempcap,tempext) in capteur]
    datejma = [date for (idcap,idZ,date, hour, tempcap,tempext) in capteur]
    heure=[hour for (idcap,idZ,date, hour, tempcap,tempext) in capteur]
    tempcapteur = [tempcap for (idcap,idZ,date, hour, tempcap,tempext) in capteur]
    tempexterne=[tempext for (idcap,idZ,date, hour, tempcap,tempext) in capteur]
    
    #conversion des températures en Celsius ou Farenheit selon la variable infoconversion
    tcapteur=[] 
    texterieure=[] 
    if str(infoconversion)==str("Farenheit"):
        tcapteur.clear()
        for i in range(len(tempcapteur)):
            a=(tempcapteur[i]*1.8)+32
            tcapteur.append(round(a,2))
        texterieure.clear()
        for i in range(len(tempexterne)):
            a=(tempexterne[i]*1.8)+32
            texterieure.append(round(a,2))

    elif str(infoconversion)==str("Celsius"):
        tcapteur.clear()
        texterieure.clear()
        tcapteur=tempcapteur
        texterieure=tempexterne
    
    
    donnee=list(zip(idcapteur,idzone,datejma,heure,tcapteur,texterieure)) #on crée une liste de tuplets des valeurs de température en fonction des dates et heures
    
    # add data to the treeview
    for donnee in donnee:
        tree.insert('', END, values=donnee)
        
        
    tree.grid(row=0, column=0, sticky='nsew')
                
    scrollbar = ttk.Scrollbar(tableau , orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    tableau.mainloop()
    
    
    
    
def act_graphique(capteur,date1,date2,infoconversion): #actualisation du tableaux et du graphique
    graphique(capteur,date1,date2,infoconversion)
    tableaux(capteur,date1,date2,infoconversion)
    

def tableaux_print(capteur,date1,date2,infoconversion): #on appelle cette fonction grâce au bouton situé dans une autre fonction pour actualiser le tableau avec les nouvelles exigences de date ou capteurs ou conversion de températures
    tableaux(capteur,date1,date2,infoconversion) 

    

    
def fonctionprintgraphzones(date1="2020-05-22",date2="2020-05-22",infoconversion="Celsius"):
    global fig,output
    
    date1=entry_date1.get()
    date2=entry_date2.get()
    infoconversion = listetemp.get()
    
    date=(date1,date2)
    
    
    cnx=sqlite3.connect("..\\SRC\\stade.db")
    #génération date/heure
    z=cnx.cursor()
    z.execute('select dateReleve,heurereleve from Releve where  Releve.idcapteur==1 and (dateReleve between ? and ?)',date)
    data=z.fetchall()
    jh = [date+hour for (date, hour) in data] 
    
    
    #création des listes contenant les capteurs en fonction du stade (multistade)
    x=cnx.cursor()
    idcapteur=x.execute('select Releve.idCapteur from Releve,Capteurs,Zones where Zones.idZone=Capteurs.idZone and Capteurs.idCapteur=Releve.idCapteur and Zones.idStade==? and dateReleve between ? and ?',(numeroStade,date1,date2))
    captstade=[]
    for i in idcapteur:
        captstade.append(i[0])
    
    datazone1=(captstade[0],captstade[1],date1,date2) #on crée une liste de tuplets des valeurs de température en fonction des dates et heures
    datazone2=(captstade[2],captstade[3],captstade[4],captstade[5],date1,date2) 
    datazone3=(captstade[6],captstade[7],captstade[8],captstade[9],date1,date2)
    datazone4=(captstade[10],captstade[11],date1,date2)
    
    
    
    #zone 1
    x=cnx.cursor()
    x.execute('select tempcapt from Releve where  (Releve.idCapteur==? or Releve.idCapteur==?) and (dateReleve between ? and ?)',datazone1)
    Zone1=x.fetchall()
    group1=[]
    i=0
    while i<=len(Zone1)-2:
        group1.append(round(sum(Zone1[i]+Zone1[i+1])/2,2))
        i+=2
    
    temp1 = [value for (value) in group1]
    
    Ftemp1=[] 
    if str(infoconversion)==str("Farenheit"):
        Ftemp1.clear()
        for i in range(len(temp1)):
            a=(temp1[i]*1.8)+32
            Ftemp1.append(a)
    
    elif str(infoconversion)==str("Celsius"):
        Ftemp1.clear()
        Ftemp1=temp1
    
    
    #zone 2
    x=cnx.cursor()
    x.execute('select tempcapt from Releve where  (Releve.idCapteur==? or Releve.idCapteur==? or Releve.idCapteur==? or Releve.idCapteur==?) and (dateReleve between ? and ?)',datazone2)
    Zone2=x.fetchall()
    group2=[]
    i=0
    while i<=len(Zone2)-4:
        group2.append(round(sum(Zone2[i]+Zone2[i+1]+Zone2[i+2]+Zone2[i+3])/4,2))
        i+=4
    
    temp2 = [value for (value) in group2]
    
    Ftemp2=[] 
    if str(infoconversion)==str("Farenheit"):
        Ftemp2.clear()
        for i in range(len(temp2)):
            a=(temp2[i]*1.8)+32
            Ftemp2.append(a)
    
    elif str(infoconversion)==str("Celsius"):
        Ftemp2.clear()
        Ftemp2=temp2
    
    
    
    #zone 3
    x=cnx.cursor()
    x.execute('select tempcapt from Releve where  (Releve.idCapteur==? or Releve.idCapteur==? or Releve.idCapteur==? or Releve.idCapteur==?) and (dateReleve between ? and ?)',datazone3)
    Zone3=x.fetchall()
    group3=[]
    i=0
    while i<=len(Zone3)-4:
        group3.append(round(sum(Zone3[i]+Zone3[i+1]+Zone3[i+2]+Zone3[i+3])/4,2))
        i+=4
    
    temp3 = [value for (value) in group3]
    
    Ftemp3=[] 
    if str(infoconversion)==str("Farenheit"):
        Ftemp3.clear()
        for i in range(len(temp3)):
            a=(temp3[i]*1.8)+32
            Ftemp3.append(a)
    
    elif str(infoconversion)==str("Celsius"):
        Ftemp3.clear()
        Ftemp3=temp3
    
    
    
    #zone 4
    x=cnx.cursor()
    x.execute('select tempcapt from Releve where  (Releve.idCapteur==? or Releve.idCapteur==? ) and (dateReleve between ? and ?)',datazone4)
    Zone4=x.fetchall()
    group4=[]
    i=0
    while i<=len(Zone4)-2:
        group4.append(round(sum(Zone4[i]+Zone4[i+1])/2,2))
        i+=2
    
    temp4 = [value for (value) in group4]
    Ftemp4=[] 
    if str(infoconversion)==str("Farenheit"):
        Ftemp4.clear()
        for i in range(len(temp4)):
            a=(temp4[i]*1.8)+32
            Ftemp4.append(a)
    
    elif str(infoconversion)==str("Celsius"):
        Ftemp4.clear()
        Ftemp4=temp4
    
    
    clear_plot()
    fig = Figure(figsize = (30,5), dpi = 70)
    plot1 = fig.add_subplot(111)
    plot1.set_ylabel("Température")
    
    #affichage propre des dates qur l'axe des abscisses
    date=jh[:]#vraie copie de liste
    #transformation du format de la date en np.datetime64
    for i in range (len(date)):
        date[i]=date[i][:10]+"T"+date[i][10:]+":00Z"
        date[i]=np.datetime64(date[i])
        #pour incliner les labels
    for label in plot1.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')
        #gestion des label x
    cdf = mdates.ConciseDateFormatter(plot1.xaxis.get_major_locator())
    

    plot1.set_title("Graphique de l'évolution de la température pour toutes les zones",loc="left")
    plot1.plot(date,Ftemp1,"-b",label='zone1')
    plot1.plot(date,Ftemp2,"-r",label="zone2")
    plot1.plot(date,Ftemp3,"-g",label="zone3")
    plot1.plot(date,Ftemp4,"-y",label="zone4")
    plot1.legend(loc="upper left")
    output = FigureCanvasTkAgg(fig, master = canvas)   
    output.draw() 
    output.get_tk_widget().pack() 
    toolbar = NavigationToolbar2Tk(output , interface).place(x=550,y=250) 
    
    cnx.close()


