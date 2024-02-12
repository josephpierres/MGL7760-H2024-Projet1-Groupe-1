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
MYSQL_CMD = f"docker exec -i mysql mysql  --defaults-extra-file=/app/config.cnf  -h{MYSQL_HOST} -P{MYSQL_PORT} -u{MYSQL_USER} -p{MYSQL_PASSWORD} {MYSQL_DATABASE}"
#MYSQL_CMD = f"docker exec -i mysql mysql  --defaults-extra-file=config.cnf"
# Remove double quotes around values in the CSV file
#subprocess.run(["sed", "-i", 's/"//g', CSV_FILE])

print(f"Inserting data into Editeur, Categorie, and Auteur tables from {CSV_FILE}")

with open(CSV_FILE, "r", newline='', encoding='utf-8') as csvfile:
    #reader = csv.DictReader(csvfile)
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, skipinitialspace=True)
    next(reader)  # Skip header row

    for row in reader:
        print(f"******************************************************************")
        print('titre: ', row['titre'], '\nauteurs: ', row['auteurs'],  '\ncategories: ', row['categories'])
        print(f"******************************************************************")
        # Replace empty values with NULL
        titre, description, isbn, annee_apparition, image, editeur, categories, auteurs = (
            row['titre'].strip() or None,
            row['description'].strip() or None,
            row['isbn'].strip() or None,
            row['annee_apparition'].strip() or None,
            row['image'].strip() or None,
            row['editeur'].strip() or None,
            [categorie.strip() for categorie in row['categories'].split(',')],
            [auteur.strip() for auteur in row['auteurs'].split(',')],
        )

        print(f"Processing row auteur:: {len(auteurs)} et categorie:: {len(categories)}")

        # Insert or retrieve Editeur ID
        editeur_id = subprocess.check_output(
            f"{MYSQL_CMD} -N -e \"INSERT INTO editeur (nom) VALUES ('{editeur}') "
            f"ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id); "
            f"SELECT id FROM editeur WHERE nom='{editeur}'\"",
            shell=True,
            text=True,
        ).strip()

        # Insert or retrieve Auteur IDs
        
        auteur_ids = []
        for auteur in auteurs:
            auteur_id = subprocess.check_output(
                f"{MYSQL_CMD} -N -e \"INSERT INTO auteur (nom) VALUES ('{auteur}') "
                f"ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id); "
                f"SELECT id FROM auteur WHERE nom='{auteur}'\"",
                shell=True,
                text=True,
            ).strip()
            auteur_ids.append(auteur_id)

        
              
        # Insert or retrieve Categorie IDs       
        categorie_ids = []
        for categorie in categories:
            categorie_id = subprocess.check_output(
                f"{MYSQL_CMD} -N -e \"INSERT INTO categorie (nom) VALUES ('{categorie}') "
                f"ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id); "
                f"SELECT id FROM categorie WHERE nom='{categorie}'\"",
                shell=True,
                text=True,
            ).strip()
            categorie_ids.append(categorie_id)        

        # Insert Livre
        subprocess.run(
            f"{MYSQL_CMD} -e \"INSERT INTO livre (titre, description, isbn, annee_apparition, image, id_editeur) "
            f"VALUES ('{titre}', '{description}', '{isbn}', {annee_apparition}, '{image}', {editeur_id})\"",
            shell=True,
        )

        # Retrieve Livre ID
        livre_id = subprocess.check_output(
            f"{MYSQL_CMD} -N -e \"SELECT id FROM livre WHERE titre='{titre}' AND isbn='{isbn}'\"",
            shell=True,
            text=True,
        ).strip()

        # Insert LivreAuteur
        for i, auteur_id in  enumerate(auteur_ids):
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
