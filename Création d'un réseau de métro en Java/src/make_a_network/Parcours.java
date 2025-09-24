package make_a_network;

import java.util.ArrayList;

public interface Parcours{
	
	public Arret prochaineEtape();
	public Arret prochainArret();
	public ArrayList<Arret> listeArret();
	public Parcours clone();
	
}