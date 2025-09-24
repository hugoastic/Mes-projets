package make_a_network;

import java.util.ArrayList;
import java.util.Stack;
import java.util.HashMap;

public class Parcours_personne implements Parcours{
	/*
	 * 	Le parcours d'une personne est stocke dans une pile a l'aide d'arrets
	 * 
	 * Le parcours est initalise dans notre cas grace a Dijskra sur le graphe ce qui n'est pas la methode la plus performante
	 * Pour une methode plus performante il nous aurais fallu prevoir le trajet de chaque personne sur le reseau
	 */

	private Stack<Arret> pile;
	private ArrayList<Arret> liste_arret;
	
	@SuppressWarnings("unchecked")
	//Constructeur de basse
	public Parcours_personne(Stack<Arret> p) {
		pile = (Stack<Arret>) p.clone();
		liste_arret = new ArrayList<>();
		for(Arret a : p) {
			liste_arret.add(a);
		}
	}

	//Constructeur determinant le parcours
	public Parcours_personne(Arret n1, Arret n2, Map m) {

		liste_arret = new ArrayList<>();
		pile = new Stack<>();
		//Recuperation du parcours grace à Dijskra
		HashMap<Noeud, Noeud> predecesseur = m.dijskra(n1).predecesseur;
		
		//Mise en pile du parcours
		while(n2 != n1 && n2 != null) {
			liste_arret.add(n2);
			n2 = (Arret) predecesseur.get(n2);
		}
		liste_arret.add(n2);
		for(Arret a : liste_arret) {
			pile.push(a);
		}
	}
	
	public String toString() {
		String txt = "";
		for(Arret a : pile) {
			if(a != null) txt = txt + "|" + a.toString() + " ";
		}
		return txt;
	}
	
	public void empiler(Arret arret) {
		liste_arret.add(arret);
	}
	

	public Arret dernierArret() {
		return pile.firstElement();
	}
	
	public Arret prochainArret() {
		return pile.lastElement();
	}

	public ArrayList<Arret> listeArret() {
		return liste_arret;
	}
	
	@SuppressWarnings("unchecked")
	public Parcours_personne clone() {
		return new Parcours_personne((Stack<Arret>) pile.clone());
	}

	public Arret prochaineEtape() {
		return pile.pop();
	}
}
