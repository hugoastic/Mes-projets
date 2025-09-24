package make_a_network;

public class Route implements Arete{
	
	private int distance;
	
	private Arret arret1;
	private Arret arret2;
	
	public Route(int distance, Arret arret1, Arret arret2) {
		this.distance=distance;
		this.arret1= arret1;
		this.arret2= arret2;	
	}

	public int getDistance() {
		return distance;
	}
	public Noeud getNoeud1() {
		return arret1;
	}
	public Noeud getNoeud2() {
		return arret2;
	}
	
	public String toString() {
		return arret1.getPoint()+" a "+arret2.getPoint()+" avec une distance de "+distance;
	}

}
