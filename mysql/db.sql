-- Création de la base de données
CREATE DATABASE IF NOT EXISTS gestion_bibliotheque CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Utilisation de la base de données
USE gestion_bibliotheque;

-- Création de la table editeur
CREATE TABLE IF NOT EXISTS editeur (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255) NOT NULL UNIQUE   
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Création de la table categorie
CREATE TABLE IF NOT EXISTS categorie (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255) NOT NULL UNIQUE   
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Création de la table auteur
CREATE TABLE IF NOT EXISTS auteur (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255) NOT NULL UNIQUE     
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Création de la table livre
CREATE TABLE IF NOT EXISTS livre (
    id INT PRIMARY KEY AUTO_INCREMENT,
    titre VARCHAR(255) NOT NULL,
    description TEXT,
    isbn VARCHAR(20) NOT NULL,
    annee_apparition INT,
    image VARCHAR(255),
    id_editeur INT,
    FOREIGN KEY (id_editeur) REFERENCES editeur(id),
    INDEX (id_editeur),
    CONSTRAINT fk_livre_editeur FOREIGN KEY (id_editeur) REFERENCES editeur(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Création de la table livrecategorie
CREATE TABLE IF NOT EXISTS livrecategorie (
    id_livre INT,
    id_categorie INT,
    PRIMARY KEY (id_livre, id_categorie),
    FOREIGN KEY (id_livre) REFERENCES livre(id),
    FOREIGN KEY (id_categorie) REFERENCES categorie(id),
    INDEX (id_categorie, id_livre ),
    CONSTRAINT fk_livrecategorie_livre FOREIGN KEY (id_livre) REFERENCES livre(id) ON DELETE CASCADE,
    CONSTRAINT fk_livrecategorie_categorie FOREIGN KEY (id_categorie) REFERENCES categorie(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Création de la table livreauteur
CREATE TABLE IF NOT EXISTS livreauteur (
    id_livre INT,
    id_auteur INT,
    PRIMARY KEY (id_livre, id_auteur),
    FOREIGN KEY (id_livre) REFERENCES livre(id),
    FOREIGN KEY (id_auteur) REFERENCES auteur(id),
    INDEX (id_auteur, id_livre ),
    CONSTRAINT fk_livreauteur_livre FOREIGN KEY (id_livre) REFERENCES livre(id) ON DELETE CASCADE,
    CONSTRAINT fk_livreauteur_auteur FOREIGN KEY (id_auteur) REFERENCES auteur(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;