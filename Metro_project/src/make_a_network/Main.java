package make_a_network;

import java.util.ArrayList;

public class Main {

	public static void main(String[] args) {
		// Creation des routes et arrets
		Arret A = new Arret("A");
		Arret B = new Arret("B");
		Arret C = new Arret("C");
		Arret D = new Arret("D");
		Arret E = new Arret("E");
		
		Arete route1=new Route(10, A, B);
		Arete route2=new Route(4, A, C);
		Arete route3=new Route(12, C, D);
		Arete route4=new Route(14, C, E);
		
		// Creation du Network
		Map network = new Map();
		network.addChemin(route1);
		network.addChemin(route2);
		network.addChemin(route3);
		network.addChemin(route4);
		
		//Creation des bus et de leurs parcours
		ArrayList<Arret> a = new ArrayList<>();
		a.add(B);
		a.add(A);
		a.add(C);
		a.add(E);
		a.add(C);
		a.add(A);
		Parcours_bus pb1 = new Parcours_bus(a);
		Bus b1 = new Bus_Double(pb1 ,network, "Bus Double 1");
		network.ajouterBus(b1);
		

		a.clear();
		a.add(D);
		a.add(C);
		a.add(E);
		a.add(C);
		Parcours_bus pb2 = new Parcours_bus(a);
		Bus b2 = new Bus_Double(pb2 ,network, "Bus Double 2");
		network.ajouterBus(b2);
		
		a.clear();
		a.add(B);
		a.add(E);
		a.add(D);
		Parcours_bus pb3 = new Parcours_bus(a);
		Bus b3 = new Bus_Double(pb3 ,network, "Bus Double 3");
		network.ajouterBus(b3);
		

		a.clear();
		a.add(A);
		a.add(C);
		Parcours_bus pbF = new Parcours_bus(a);
		Bus bF = new Bus_Fast(pbF ,network, "Bus Fast");
		network.ajouterBus(bF);
		
		Personne albert = new Personne("Albert", 0, B, D, 500, D, A, network);
		for(int i = 0; i < 12; i++) { network.ajouterPersonne(albert.clone("Albert"+(i+1)));}
		
		Personne bob = new Personne("Bob", 0, B, C, 500, C, B, network);
		for(int i = 0; i < 12; i++) { network.ajouterPersonne(bob.clone("Bob"+(i+1)));}

		Personne charles = new Personne("Charles", 0, B, C, 500, C, B, network);
		for(int i = 0; i < 12; i++) { network.ajouterPersonne(charles.clone("Charles"+(i+1)));}
		
		Personne damien = new Personne("Damien", 0, E, A, 600, A, E, network);
		for(int i = 0; i < 12; i++) { network.ajouterPersonne(damien.clone("Damien"+(i+1)));}
		//Edouard		
		Personne edouard = new Personne("Edouard", 0, A, C, 300, C, A, network);
		for(int i = 0; i < 12; i++) { network.ajouterPersonne(edouard.clone("Edouard"+(i+1)));}
		
		network.avancerMonde();
		
		
		//Affichage des differentes listes de personnes
		System.out.println("Liste d'attente des arrets : ");
		for(Noeud ar : network.getListNoeud()) {
			Arret arret = (Arret) ar;
			System.out.println(arret + " : " + arret.getCopyListAttente());
		}
		
		System.out.println("Liste des personnes dans les bus : ");
		for(Bus b : network.getListBusCopy()) {
			System.out.println(b + " : " + b.getListPersonneCopy());
		}
		
	}

}
