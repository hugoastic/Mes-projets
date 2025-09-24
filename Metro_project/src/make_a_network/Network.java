package make_a_network;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;

//La class Network est equivalente a un graphe
public class Network {
	
	private ArrayList<Arete> network;
	
	public Network() {
		this.network=new ArrayList<Arete>();
	}
	
	public ArrayList<Arete> getList() {
		return network;
	}
	
	public void addChemin(Arete chemin) {
		network.add(chemin);
	}
	public void removeChemin(Arete chemin) {
		network.remove(chemin);
	}
	
	private Noeud minDistance(ArrayList<Noeud> P, HashMap<Noeud, Integer> distance) {
		Noeud ret = P.get(0);
		for(Noeud n : distance.keySet()) {
			if(distance.get(ret) > distance.get(n) && P.contains(n)) ret = n;
		}
		return ret;
	}
	
	public Dijskra_Information dijskra(Noeud n1){
		HashMap<Noeud, Integer> distance = new HashMap<>();
		HashMap<Noeud, Noeud> predecesseur = new HashMap<>();
		
		ArrayList<Noeud> P = this.getListNoeud();
		for(Noeud n : P) {
			distance.put(n, 1000000);
			predecesseur.put(n, null);			
		}
		P.remove(n1);
		for(Noeud n : this.getVoisin(n1)) {
			distance.put(n, this.getDistanceVoisin(n1, n));
			predecesseur.put(n, n1);
			
		}
		while(P.isEmpty() == false) {
			Noeud a = minDistance(P, distance);
			P.remove(a);
			for(Noeud b : this.getVoisin(a)) {
				int newD = distance.get(a) + this.getDistanceVoisin(a, b);
				if(distance.get(b) > newD && P.contains(b)) {
					distance.put(b,  newD);
					predecesseur.put(b, a);
				}
			}
		}
		Dijskra_Information inf = new Dijskra_Information();
		inf.predecesseur = predecesseur;
		inf.distance = distance;
		inf.orgine = n1;
		return inf;
	}
	
	public ArrayList<Noeud> getListNoeud(){
		ArrayList<Noeud> list = new ArrayList<>();
		for(Arete arete : network) {
			list.add(arete.getNoeud1());
			list.add(arete.getNoeud2());
		}
		//On obtient une liste distincte
		HashSet<Noeud> set = new HashSet<>(list);
        ArrayList<Noeud> newList = new ArrayList<>(set);// Créer une nouvelle ArrayList à partir des éléments uniques
		return newList;
	}
	
	public void printAretes() {
		for ( Arete arete : network) {
			System.out.println(arete.toString());
		}
	}
	
	public ArrayList<Noeud> getVoisin(Noeud n){
		ArrayList<Noeud> voisin = new ArrayList<>();
		for(Arete a : network) {
			if(a.getNoeud1() == n) voisin.add(a.getNoeud2());
			else if(a.getNoeud2() == n) voisin.add(a.getNoeud1());
		}
		return voisin;
	}
	
	public int getDistanceVoisin(Noeud n1,Noeud n2) {
		int distance=0;
		for ( Arete n : network) {
			if ( ((n.getNoeud1()==n1) && (n.getNoeud2()==n2)) || ((n.getNoeud1()==n2) && (n.getNoeud2()==n1)) ){
				distance= n.getDistance();
			}
		}
		if (distance==0) {
			throw new Error ("Noeuds non voisin");
		}
		else {
			return distance;
		}
	}
	
	public int getDistance(Noeud n1, Noeud n2) {
		HashMap<Noeud, Integer> distance = this.dijskra(n1).distance;
		return distance.get(n2);
	}
	
}
