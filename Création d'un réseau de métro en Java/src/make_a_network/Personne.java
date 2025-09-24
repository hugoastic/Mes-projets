package make_a_network;

public class Personne{

	private String name;
	private int heure_aller_depart;
	private Arret arret_aller_depart;
	private Arret arret_aller_arrivee;
	private int heure_retour_depart;
	private Arret arret_retour_depart;
	private Arret arret_retour_arrivee;
	
	private Parcours_personne parcours_aller;
	private Parcours_personne parcours_retour;
	private boolean retour;
	private boolean fini;
	
	private Map m;
	
	public Personne(String name, int heure_aller_depart,Arret arret_aller_depart, Arret arret_aller_arrivee,int heure_retour_depart,
	Arret arret_retour_depart,Arret arret_retour_arrivee, Map m) {
		this.name=name;
		this.heure_aller_depart=heure_aller_depart;
		this.arret_aller_depart=arret_aller_depart;
		this.arret_aller_arrivee=arret_aller_arrivee;
		this.heure_retour_depart=heure_retour_depart;
		this.arret_retour_depart=arret_retour_depart;
		this.arret_retour_arrivee=arret_retour_arrivee;
		
		this.parcours_aller = new Parcours_personne(this.arret_aller_depart, this.arret_aller_arrivee, m);
		this.parcours_retour = new Parcours_personne(this.arret_retour_depart, this.arret_retour_arrivee, m);
		this.m = m;
		
		retour = false;
		fini = false;
		//System.out.println(this.name + ">>Je suis pret !");
	
	}
	
	public Personne(String name, int heure_aller_depart,Arret arret_aller_depart, Arret arret_aller_arrivee,int heure_retour_depart,
			Arret arret_retour_depart,Arret arret_retour_arrivee, Map m, Parcours_personne p_aller, Parcours_personne p_retour) {
		this.name=name;
		this.heure_aller_depart=heure_aller_depart;
		this.arret_aller_depart=arret_aller_depart;
		this.arret_aller_arrivee=arret_aller_arrivee;
		this.heure_retour_depart=heure_retour_depart;
		this.arret_retour_depart=arret_retour_depart;
		this.arret_retour_arrivee=arret_retour_arrivee;
		
		this.parcours_aller = p_aller.clone();
		this.parcours_retour = p_retour.clone();
		this.m = m;
		
		retour = false;
		fini = false;
		
		retour = false;
		fini = false;
		
	}	
	public Personne clone(String name) {
		return new Personne(name, heure_aller_depart, arret_aller_depart, arret_aller_arrivee, heure_retour_depart, arret_retour_depart, arret_retour_arrivee, m, parcours_aller, parcours_retour);
	}
	
	public Noeud getArretDepart() {
		return arret_aller_depart;
	}
	
	public Noeud getArretArrivee() {
		if(retour) return parcours_retour.dernierArret();
		return parcours_aller.dernierArret();
	}
	
	public void  appliquerProchaineEtape(Arret arret_actuel, int horloge, Bus bus) {
		if(fini) return;
		//Phase d'initialisation du parcours alle ou retour
		if((arret_actuel == null) && (retour == false) && (horloge >= heure_aller_depart) && (bus == null)) {//Parcours alle
			arret_actuel = (Arret) parcours_aller.prochaineEtape();
			arret_actuel.addPersonne(this);
			System.out.println(this.name + "(" + horloge + ")>>Je suis a l'arret " + arret_actuel + " pour mon chemin aller");
		}
		else if((arret_actuel == null) && (retour == true) && (horloge >= heure_retour_depart) && (bus == null)) {//Parcours retour
			arret_actuel = (Arret) parcours_retour.prochaineEtape();
			arret_actuel.addPersonne(this);
			System.out.println(this.name + "(" + horloge + ")>>Je suis a l'arret " + arret_actuel + " pour mon chemin retour");
		}
		
		//Si la personne se trouve a un arret
		if(arret_actuel != null) {
			Arret arret = (Arret) arret_actuel;
			//Elle cherche a monter dans un bus
			for(Bus b : arret.getListBus()) {
				//Chemin aller
				if(retour == false) {
					//La personne regarde si le bus lui correspond
					if(b.prochainArret() == parcours_aller.prochainArret()) {
						//La personne regarde si elle peut monter dans le bus
						if(b.monter(this)) {
							//Dans ce cas elle monte dans le bus et quitte l'arret
							arret.removePersonne(this);
							System.out.println(this.name + "(" + horloge + ")>>Je monte dans le bus " + b + "(arret : " + arret_actuel + ")");
						}
					}
				}
				//Chemin retour
				else {
					//La personne regarde si le bus lui correspond
					if(b.prochainArret() == parcours_retour.prochainArret()) {
						//La personne regarde si elle peut monter dans le bus
						if(b.monter(this)) {
							//Dans ce cas elle monte dans le bus et quitte l'arret
							arret.removePersonne(this);;
							System.out.println(this.name + "(" + horloge + ")>>Je monte dans le bus " + b+ "(arret : " + arret_actuel + ")");
						}
					}
				}
			}
		}
		//Si la personne n'est pas dans un arret elle est dans un bus
		else if(bus != null) {
			//On commence par regarder si le bus se trouve a un arret
			for(Noeud a : m.getListNoeud()) {
				Arret arret = (Arret) a;
				if(arret.busEstPresent(bus)) {
					//Si on est a un arret on regarde si cet arret nous correspond
					if(retour == false && arret == parcours_aller.prochainArret()) {
						//Cas du chemin aller
						parcours_aller.prochaineEtape();
						//On regarde si on est arrive
						if(arret == this.arret_aller_arrivee) {
							//La personne quitte le bus et se declare arrivee
							if(bus.descendre(this)) {
								System.out.println(this.name + "(" + horloge + ")>>Je descend du bus " + bus+ "(arret : " + arret + ")");
								retour = true;
								System.out.println(this.name + "(" + horloge + ")>>Je suis arrive !!");
							}
						}
						//Sinon je regarde si il est necessaire que la personne descende du bus
						else if(bus.prochainArret() != parcours_aller.prochainArret()) {
							if(bus.descendre(this)) {
								arret.addPersonne(this);
								System.out.println(this.name + "(" + horloge + ")>>Je descend du bus " + bus+ "(arret : " + arret + ")");
							}
							else {
								System.out.println(this.name + "(" + horloge + ")>>Erreur pas reussi a quitter le bus");
							}					
						}
					}
					else if(retour == true && arret == parcours_retour.prochainArret()) {
						parcours_retour.prochaineEtape();
						if(arret == this.arret_retour_arrivee) {
							if(bus.descendre(this)) {
								System.out.println(this.name + "(" + horloge + ")>>Je descend du bus " + bus+ "(arret : " + arret + ")");
								System.out.println(this.name + "(" + horloge + ")>>Je suis arrive !!");
								fini = true;
							}
						}
						else if(bus.prochainArret() != parcours_retour.prochainArret()) {
							if(bus.descendre(this)) {
								arret.addPersonne(this);
								System.out.println(this.name + "(" + horloge + ")descend du bus " + bus+ "(arret : " + arret + ")");
							}
							else {
								System.out.println(this.name + "(" + horloge + ")>>Erreur pas reussi a quitter le bus");
							}
						}
					}
				}
			}
		}
		
	}
	public String toString() {
		return name;
	}
}
