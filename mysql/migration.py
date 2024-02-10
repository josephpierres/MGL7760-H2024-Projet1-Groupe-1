#!/usr/bin/env python3
# csv-reader.py: Example of CSV parsing and MySQL insertion in Python

import csv
import subprocess

# MySQL configuration
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "gestion_bibliotheque"
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"

# Path to the CSV file
CSV_FILE = "biblio.csv"

# Command for inserting data into MySQL
MYSQL_CMD = f"docker exec -i mysql mysql -h{MYSQL_HOST} -P{MYSQL_PORT} -u{MYSQL_USER} -p{MYSQL_PASSWORD} {MYSQL_DATABASE}"

# Remove double quotes around values in the CSV file
subprocess.run(["sed", "-i", 's/"//g', CSV_FILE])

print(f"Inserting data into Editeur, Categorie, and Auteur tables from {CSV_FILE}")

with open(CSV_FILE, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    next(reader)  # Skip header row

    for row in reader:
        print( 'titre: ', row['titre'], 'description: ', row['description'], 'isbn: ', row['isbn'], 'annee_apparition: ', row['annee_apparition'], 'image: ', row['image'], 'auteurs: ', row['auteurs'], 'editeur: ', row['editeur'], 'categories: ', row['categories'])
       
        # Replace empty values with NULL
        titre, description, isbn, annee_apparition, image, editeur, categories, auteurs = (
            row['titre'].strip() or "NULL",
            row['description'].strip() or "NULL",
            row['isbn'].strip() or "NULL",
            row['annee_apparition'].strip() or "NULL",
            row['image'].strip() or "NULL",
            row['editeur'].strip() or "NULL",
            row['categories'].strip() or "NULL",
            row['auteurs'].strip() or "NULL",
        )
       # titre = row['titre'], 'description: ', row['description'], 'isbn: ', row['isbn'], 'annee_apparition: ', row['annee_apparition'], 'image: ', row['image'], 'auteurs: ', row['auteurs'], 'editeur: ', row['editeur'], 'categories: ', row['categories'])
        
        print(f"Processing row: {titre} {description} {isbn} {annee_apparition} {image} {auteurs} {editeur} {categories}")

        # Insert or retrieve Editeur ID
        editeur_id = subprocess.check_output(
            f"{MYSQL_CMD} -N -e \"INSERT INTO editeur (nom) VALUES ('{editeur}') ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id); SELECT id FROM editeur WHERE nom='{editeur}'\"",
            shell=True,
            text=True,
        ).strip()

        # Insert or retrieve Auteur ID
        auteurs_list = [auteur.strip() for auteur in row['auteurs'].split(',')]
        auteur_ids = []
        for auteur in auteurs_list:
            auteur_id = subprocess.check_output(
                f"{MYSQL_CMD} -N -e \"INSERT INTO auteur (nom) VALUES ('{auteur}') ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id); SELECT id FROM auteur WHERE nom='{auteur}'\"",
                shell=True,
                text=True,
            ).strip()
            auteur_ids.append(auteur_id)

        # Insert or retrieve Categorie ID
        categories_list = [categorie.strip() for categorie in row['categories'].split(',')]
        categorie_ids = []
        for categorie in categories_list:
            categorie_id = subprocess.check_output(
                f"{MYSQL_CMD} -N -e \"INSERT INTO categorie (nom) VALUES ('{categorie}') ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id); SELECT id FROM categorie WHERE nom='{categorie}'\"",
                shell=True,
                text=True,
            ).strip()
            categorie_ids.append(categorie_id)

        # Insert Livre
        subprocess.run(
            f"{MYSQL_CMD} -e \"INSERT INTO livre (titre, description, isbn, annee_apparition, image, id_editeur) VALUES ('{titre}', '{description}', '{isbn}', {annee_apparition}, '{image}', {editeur_id})\"",
            shell=True,
        )

        # Retrieve Livre ID
        livre_id = subprocess.check_output(
            f"{MYSQL_CMD} -N -e \"SELECT id FROM livre WHERE titre='{titre}' AND isbn='{isbn}'\"",
            shell=True,
            text=True,
        ).strip()

        # Insert LivreAuteur
        for auteur_id in auteur_ids:
            subprocess.run(
                f"{MYSQL_CMD} -e \"INSERT INTO livreauteur (id_livre, id_auteur) VALUES ({livre_id}, {auteur_id})\"",
                shell=True,
            )

        # Insert LivreCategorie
        for categorie_id in categorie_ids:
            subprocess.run(
                f"{MYSQL_CMD} -e \"INSERT INTO livrecategorie (id_livre, id_categorie) VALUES ({livre_id}, {categorie_id})\"",
                shell=True,
            )

print("Data insertion complete.")