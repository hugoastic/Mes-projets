package make_a_network;

import java.util.ArrayList;

public class Map extends Network{
	
	private ArrayList <Bus> bus = new ArrayList<Bus>();
	private ArrayList <Personne> personne = new ArrayList<Personne>();
	
	public final static int heure_final = 100000;
	private int horloge;

	public Map() {
		super();
		horloge = 0;
	}

	public void avancerMonde() {
		//Recuperation des arrets
		ArrayList<Noeud> list_noeud = this.getListNoeud();
		ArrayList<Arret> list_arret = new ArrayList<>();
		for(Noeud n : list_noeud) list_arret.add((Arret) n);
		
		while(horloge <= heure_final) {
			
			//Permet de recuperer les personnes qui ne sont ni dans les bus et ni aux arrets
			@SuppressWarnings("unchecked")
			ArrayList<Personne> personne_restant = (ArrayList<Personne>) personne.clone();
			
			//On fait avancer chaque bus et chaque personne dans les bus
			for(Bus b : bus) {
				b.appliquerProchaineEtape();
				ArrayList<Personne> temp = b.getListPersonneCopy();
				for(Personne p : temp) {
					personne_restant.remove(p);
					p.appliquerProchaineEtape(null, horloge, b);
				}
			}
			
			//On fait avancer toutes les personnes presententes a des arrets
			for(Arret arret : list_arret) {
				ArrayList<Personne> temp = arret.getCopyListAttente();
				for(Personne p : temp) {
					personne_restant.remove(p);
					p.appliquerProchaineEtape(arret, horloge, null);
				}
			}
			
			//et on fait avancer toutes les personnes presententes nul part
			@SuppressWarnings("unchecked")
			ArrayList<Personne> temp = (ArrayList<Personne>) personne_restant.clone();
			for(Personne p : temp) {
				p.appliquerProchaineEtape(null, horloge, null);
			}
			
			horloge++;
		}
	}

	public void ajouterPersonne(Personne p) {
		personne.add(p);
	}
	
	public void retirerPersonne(Personne p) {
		personne.remove(p);
	}
	
	public void ajouterBus(Bus b) {
		bus.add(b);
	}
	
	public void retirerBus(Bus b) {
		bus.remove(b);
	}
	
	public int get_horloge() {
		return horloge;
	}
	
	public ArrayList<Bus> getListBusCopy(){
		return this.bus;
	}
}
