package make_a_network;
import java.util.ArrayList;

public class Arret implements Noeud{

	private String point;//Nom du noeud
	private ArrayList<Personne> liste_attente;
	private ArrayList<Bus> list_bus;
	
	public Arret(String point) {
		this.point=point;
		liste_attente= new ArrayList<Personne>();
		list_bus = new ArrayList<Bus>();
	}
	
	public String getPoint() {
		return point;
	}
	
	public void addPersonne(Personne personne) {
		liste_attente.add(personne);
	}
	
	public void removePersonne(Personne personne) {
		liste_attente.remove(personne);
	}
	
	public void arriverBus(Bus b) {
		list_bus.add(b);
	}
	
	public void quitterBus(Bus b) {
		list_bus.remove(b);
	}
	
	@SuppressWarnings("unchecked")
	public ArrayList<Personne> getCopyListAttente(){
		return (ArrayList<Personne>) liste_attente.clone();
	}
	
	public boolean busEstPresent(Bus b) {
		return this.list_bus.contains(b);
	}
	
	@SuppressWarnings("unchecked")
	public ArrayList<Bus> getListBus(){
		return (ArrayList<Bus>) this.list_bus.clone();
	}
	
	public String toString() {
		return point;
	}
	
}
