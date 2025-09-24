package make_a_network;

import java.util.ArrayList;

public abstract class Bus {
	
	private String nom;
	private int nb_personnes_max;
	private int tps_charge_decharge;
	private double metre_par_tps_deplacement;
	private Parcours parcours;
	private ArrayList<Personne> liste_personne;
	
	private Map map;

	private int tps_attente;
	private Arret arret_actuel;
	private double distance;
	
	public Bus(int nb_personnes_max,int tps_charge_decharge, double v, Parcours parcours, Map map, String nom) {
		this.nb_personnes_max=nb_personnes_max;
		this.tps_charge_decharge=tps_charge_decharge;
		this.metre_par_tps_deplacement=v;
		this.parcours=parcours;
		this.liste_personne = new ArrayList<Personne>();
		this.map = map;
		this.nom = nom;
		
		this.arret_actuel = null;
		distance = 0;
	}
	
	public Arret prochainArret() {
		return (Arret) this.parcours.prochainArret();
	}
	
	public void appliquerProchaineEtape() {
		//Initialisation du bus
		if(arret_actuel == null) {
			arret_actuel = (Arret) parcours.prochaineEtape();
			arret_actuel.arriverBus(this);
		}
		//Bus en cours de fonctionnement
		else {
			Noeud arretProchain = parcours.prochainArret();
			//Si temps d'attente > 0 alors le bus est a un arret et doit attendre
			if(tps_attente > 0) {
				tps_attente -= 1;
			}
			//Le bus n'a aucune raison d'attendre donc il part
			if(tps_attente == 0 && distance == 0) {
				arret_actuel.quitterBus(this);
				distance = map.getDistance(arret_actuel, arretProchain);
			}
			//Le bus parcours la distance qu'il doit parcourir
			else if(distance > 0) {
				distance = distance - metre_par_tps_deplacement;
				//Si la distance est atteinte le bus annonce qu'il arrive a un arret
				if(distance <= 0) {
					distance = 0;
					arret_actuel = (Arret) parcours.prochaineEtape();
					arretProchain = parcours.prochainArret();
					arret_actuel.arriverBus(this);
				}
			}
		}
	}
	
	//Si une personne arrive a monter dans le bus la methode renvoie vrai sinon elle renvoie faux
	public boolean monter(Personne p) {
		if (distance>0) {
			throw new Error("On ne peut pas se téléporter dans le bus (enfin pas encore)");
		}
		if(this.liste_personne.size() < this.nb_personnes_max) {
			this.liste_personne.add(p);
			tps_attente += tps_charge_decharge;
			return true;
		}
		return false;
	}
	
	//Si une personne est dans le bus la personne est retire du bus et la methode renvoie vrai sinon faux
	public boolean descendre(Personne p) {
		if (distance>0) {
			throw new Error("C'est une tentative de suicide!");
		}
		if(this.liste_personne.contains(p)) {
			this.liste_personne.remove(p);
			tps_attente += tps_charge_decharge;
			return true;
		}
		return false;
	}
	
	@SuppressWarnings("unchecked")
	public ArrayList<Personne> getListPersonneCopy(){
		return (ArrayList<Personne>) this.liste_personne.clone();
	}
	
	public String toString() {
		return nom;
	}

}
