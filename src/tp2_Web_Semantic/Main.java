package tp2_Web_Semantic;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Property;
import org.apache.jena.riot.RDFDataMgr;
import org.apache.jena.util.FileManager;

public class Main {

	public static void main(String[] args) {

		Model model = ModelFactory.createDefaultModel();

		RDFDataMgr.read(model, "file1.ttl");


		List<Property> properties = new ArrayList<>();
		model.listStatements().forEachRemaining(stmt -> {
			Property prop = stmt.getPredicate();
			if (!properties.contains(prop)) {
				properties.add(prop);
			}
		});


		properties.forEach(prop -> System.out.println(prop.getLocalName()));

		Scanner lire=new Scanner(System.in);
		int choix=0;
		int choixMesureSimilarite=0;
		System.out.println("Choisir le numéro correspondant à l'action que vous voulez effectuer");
		System.out.println("1- Choix de propriétés à comparer\n"
				+ "2- choix de mesure(s) de similarité entre les valeurs de ces propriétés\n"
				+ "3- combinaison de plusieurs mesures de similarité (afin de prendre, par exemple, leur moyenne pondérée comme mesure finale)\n"
				+ "4-choix du seuil de similarité");
		choix=lire.nextInt();

		switch (choix) {
			case 1:
	
	
				break;
	
			case 2:
				System.out.println("Choisir la mesure de  similarité");
				choixMesureSimilarite=lire.nextInt();
				switch (choixMesureSimilarite) {
					case 1:
		
						break;
					case 2:
		
						break;
					case 3:
		
						break;
					case 4:
		
						break;
		
					default:
						break;
				}
				break;
			case 3:
	
				break;
			case 4:
	
				break;
	
			default:
				break;
		}

	}





}


