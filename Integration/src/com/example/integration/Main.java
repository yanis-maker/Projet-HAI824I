package com.example.integration;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import org.apache.jena.graph.Triple;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Property;
import org.apache.jena.rdf.model.RDFNode;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.riot.RDFDataMgr;

public class Main {

	public static void main(String[] args) throws IOException {

		Model modelFile1 = ModelFactory.createDefaultModel();
		RDFDataMgr.read(modelFile1, "file1.ttl");
		List<Property> propertiesFile1 = new ArrayList<>();
		List<RDFNode> objectFile1=new ArrayList<>();
		List<Resource> subjectFile1=new ArrayList<>();
		modelFile1.listStatements().forEachRemaining(stmt -> {
			Triple triplets =stmt.asTriple();
			System.out.println(triplets.toString());
			Property prop = stmt.getPredicate();
			if (!propertiesFile1.contains(prop)) {
				propertiesFile1.add(prop);
			}
		});

		Model modelFile2 = ModelFactory.createDefaultModel();
		RDFDataMgr.read(modelFile2, "file2.ttl");
		List<Property> propertiesFile2 = new ArrayList<>();
		modelFile2.listStatements().forEachRemaining(stmt -> {
			Property prop = stmt.getPredicate();
			if (!propertiesFile2.contains(prop)) {
				propertiesFile2.add(prop);
			}
		});

		FileWriter source = new FileWriter("prop_1.txt");
		FileWriter cible = new FileWriter("prop_2.txt");
		FileWriter sameProp= new FileWriter("prop.txt");
		
		for (Property prop : propertiesFile1) {
			source.write(prop.getLocalName()+"\n");

		}
		
		for (Property prop : propertiesFile2) {
			cible.write(prop.getLocalName()+"\n");
		}
		
		for(Property prop : propertiesFile1) {
			for(Property prop2 : propertiesFile2) {
				if(prop.getLocalName().equals(prop2.getLocalName())) {
					sameProp.write(prop.getLocalName()+"\n");
				}
			}
		}
		
		

		/*Scanner lire = new Scanner(System.in);
		int choix = 0;
		int choixMesureSimilarite = 0;
		System.out.println("Choisir le numéro correspondant à l'action que vous voulez effectuer");
		System.out.println("1- Choix de propriétés à comparer\n"
				+ "2- choix de mesure(s) de similarité entre les valeurs de ces propriétés\n"
				+ "3- combinaison de plusieurs mesures de similarité (afin de prendre, par exemple, leur moyenne pondérée comme mesure finale)\n"
				+ "4-choix du seuil de similarité");
		choix = lire.nextInt();

		switch (choix) {
		case 1:
			break;

		case 2:
			System.out.println("Choisissez la mesure de  similarité");
			choixMesureSimilarite = lire.nextInt();
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
		}*/
		
		source.close();
		cible.close();
		sameProp.close();

	}

}
