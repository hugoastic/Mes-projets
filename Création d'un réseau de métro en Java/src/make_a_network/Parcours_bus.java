package make_a_network;

import java.util.ArrayList;
import java.util.Stack;

public class Parcours_bus implements Parcours{
	/*Le parcour de bus fonctionne avec deux piles
	 * 	Une pile qui contient les arrets qu'il doit faire
	 * 	Une autre qui contient les arrets qu'il a fait
	 * Quand le bus arrive a un terminus le role des pile s'inverse
	 */

	private int pile_actif;
	private Stack<Arret> pile1;
	private Stack<Arret> pile2;
	private ArrayList<Arret> liste_arret;
	
	
	@SuppressWarnings("unchecked")
	public Parcours_bus(ArrayList<Arret> listArret) {
		pile1 = new Stack<Arret>();
		pile2 = new Stack<Arret>();
		pile_actif = 1;
		this.liste_arret = (ArrayList<Arret>) listArret.clone();
		int len = listArret.size();
		for(int i = len-1; i >= 0; i--) {
			pile1.push(listArret.get(i));
		}
	}
	
	public Arret prochaineEtape() {//Applique la prochaine etape
		if(pile_actif == 1) {
			Arret a = pile1.pop();
			if(pile1.isEmpty()) {
				pile_actif = 2;
				pile1.push(a);
			}
			else pile2.push(a);
			return a;
		}
		Arret a = pile2.pop();
		if(pile2.isEmpty()) {
			pile_actif = 1;
			pile2.push(a);
		}
		else pile1.push(a);
		return a;
	}

	public Arret prochainArret() {
		if(pile_actif == 1) return pile1.lastElement();
		return pile2.lastElement();
	}

	public ArrayList<Arret> listeArret() {
		return liste_arret;
	}
	
	public Parcours_bus clone() {
		return new Parcours_bus(liste_arret);
	}
	
	public String toString() {
		return ("Parcours bus :\n" + "\tP1 : " + pile1.toString() + "\n\tP2 : " + pile2.toString());
	}

}
