from . import db


# Modèle pour la table Editeur
class Editeur(db.Model):
    __tablename__="editeur"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(255), nullable=False)

# Modèle pour la table Categorie
class Categorie(db.Model):
    __tablename__="categorie"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(255), nullable=False)

# Modèle pour la table Auteur
class Auteur(db.Model):
    __tablename__="auteur"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(255), nullable=False)

# Modèle pour la table livre
class Livre(db.Model):
    __tablename__="livre"
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    isbn = db.Column(db.String(20), nullable=False)
    annee_apparition = db.Column(db.Integer)
    image = db.Column(db.String(255))
    id_editeur = db.Column(db.Integer, db.ForeignKey('editeur.id'))
    editeur = db.relationship('Editeur', backref=db.backref('livres')) # backref ou back_populate le nom de la colonne 
    categories = db.relationship('Categorie', secondary='livrecategorie')
    auteurs = db.relationship('Auteur', secondary='livreauteur')

# Modèle pour la table livreCategorie
class Livrecategorie(db.Model):
    __tablename__="livrecategorie"
    id_livre = db.Column(db.Integer, db.ForeignKey('livre.id'), primary_key=True)
    id_categorie = db.Column(db.Integer, db.ForeignKey('categorie.id'), primary_key=True)

# Modèle pour la table livreAuteur
class Livreauteur(db.Model):
    __tablename__="livreauteur"
    id_livre = db.Column(db.Integer, db.ForeignKey('livre.id'), primary_key=True)
    id_auteur = db.Column(db.Integer, db.ForeignKey('auteur.id'), primary_key=True)
