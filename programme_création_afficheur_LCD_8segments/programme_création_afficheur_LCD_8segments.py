# Initialisation
from tkinter import*
from tkinter import ttk
import time
import serial


def interface(): 
    global root,can,select,consigne 

    # Dessin du Canevas
    root=Tk()
    root.resizable(width=True, height=True)#on fixe la taille de la fenêtre pour faire en sorte que l'utilisateur ne puisse pas la grossir
    root.title("interface 7 segs")
    can=Canvas(width=400,height=200)
    can.pack()
    select=0

    def action(event):
        global select
        select = int(listeCombo.get())
        print("Vous avez sélectionné : '", select,"'",)
    
    def recup_entry():
        value=port_serie.readline()
        afficheur_7_segments(value)
        time.sleep(0.5)        #Période de rafraichissement

    precision=["0","1","2","3","4"]
    listeCombo = ttk.Combobox(root, values=precision)
    name = Label(root, text = "Précision")
    listeCombo.current(0)
    name.pack()
    listeCombo.pack()
    listeCombo.bind("<<ComboboxSelected>>", action)

    # Dessin des afficheurs
    can.create_rectangle(0,0,500,500,fill="white",outline="white")
    can.create_rectangle(0,30,400,170,width=2,fill="grey")
    can.create_oval(80,150,85,155,fill="white")
    can.create_oval(160,150,165,155,fill="white")
    can.create_oval(240,150,245,155,fill="white")
    can.create_oval(320,150,325,155,fill="white")

    # Création du bouton
    bouton = Button(root, text="Récupérer la valeur", command=recup_entry)
    bouton.pack()
    afficheur_7_segments("0")
    root.mainloop()


def afficheur_7_segments(consigne):
        global valeur_precedente
        chiffre={0:[1,2,3,4,5,6], 1:[2,3], 2:[1,2,7,5,4], 3:[1,2,3,4,7], 4:[6,7,2,3], 5:[1,6,7,3,4], 6:[1,6,5,4,3,7], 7:[1,2,3], 8:[1,2,3,4,5,6,7], 9:[1,2,3,4,6,7]}
        codedm={1:[10,50,70,50],7:[10,100,70,100],4:[10,150,70,150],6:[10,55,10,95],2:[70,55,70,95],3:[70,105,70,145],5:[10,105,10,145]}
        codem={1:[90,50,150,50],7:[90,100,150,100],4:[90,150,150,150],6:[90,55,90,95],2:[150,55,150,95],3:[150,105,150,145],5:[90,105,90,145]}
        codec={1:[170,50,230,50],7:[170,100,230,100],4:[170,150,230,150],6:[170,55,170,95],2:[230,55,230,95],3:[230,105,230,145],5:[170,105,170,145]}
        coded={1:[250,50,310,50],7:[250,100,310,100],4:[250,150,310,150],6:[250,55,250,95],2:[310,55,310,95],3:[310,105,310,145],5:[250,105,250,145]}
        codeu={1:[330,50,390,50],7:[330,100,390,100],4:[330,150,390,150],6:[330,55,330,95],2:[390,55,390,95],3:[390,105,390,145],5:[330,105,330,145]}

        precision_affichage={0:[0,0,0,0],4:[80,150,85,155],3:[160,150,165,155],2:[240,150,245,155],1:[320,150,325,155] }

        d=0
        u=0
        c=0
        m=0
        dm=0
        #Génération aléatoire, à supprimer pour afficher une acquisition
        # Digits au repos
        i=0
        while (i<=4):
            can.create_line(10+80*i,50,70+80*i,50,width=5,fill="white")
            can.create_line(10+80*i,100,70+80*i,100,width=5,fill="white")
            can.create_line(10+80*i,150,70+80*i,150,width=5,fill="white")
            can.create_line(10+80*i,55,10+80*i,95,width=5,fill="white")
            can.create_line(70+80*i,55,70+80*i,95,width=5,fill="white")
            can.create_line(10+80*i,105,10+80*i,145,width=5,fill="white")
            can.create_line(70+80*i,105,70+80*i,145,width=5,fill="white")
            i+=1
            root.update()
    
        #Décomposition de la valeur à afficher en unités et dixaines
        if consigne=='':consigne=0
        consigne=int(float(consigne))
        u=consigne%10
        consigne //= 10
        d = consigne% 10
        consigne //= 10
        c = consigne % 10
        consigne //= 10
        m = consigne% 10
        consigne //= 10
        dm = consigne % 10


        segu=list(chiffre [u])
        segd=list(chiffre [d])
        segc=list(chiffre [c])
        segm=list(chiffre [m])
        segdm=list(chiffre [dm])
        
        for h in precision_affichage:
            if select!=0 and h==select:
                can.create_oval(precision_affichage[h],fill="red")
            else:
                can.create_oval(precision_affichage[h],fill="white")

        # Digits allumés
        for i in segu:
            can.create_line(codeu[i],width=5,fill="red")
        
        for j in segd:
            can.create_line(coded[j],width=5,fill="red")

        for k in segc:
            can.create_line(codec[k],width=5,fill="red")
        
        for l in segm:
            can.create_line(codem[l],width=5,fill="red")

        for m in segdm:
            can.create_line(codedm[m],width=5,fill="red")
        

        root.update()            
        
def fenetre_serial():
    fenetre_principale = Tk()
    fenetre_principale.title("Interface Principale")
    def valider():
        valeur_port=label_entry.get()
        port_serie = serial.Serial(port = valeur_port, baudrate = 9600)
        interface()
        port_serie.close()
    # Création du bouton pour valider l'identifiant
    bouton_valider = Button(fenetre_principale, text="Valider", command=valider)
    bouton_valider.pack(pady=10)
    # Label pour afficher les messages d'erreur
    label_entry = Entry(fenetre_principale, text="", fg="red")
    label_entry.pack()
    # Lancement de la boucle principale
    fenetre_principale.mainloop()
    fenetre_principale.destroy()

fenetre_serial()