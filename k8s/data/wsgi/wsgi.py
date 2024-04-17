from flask import Flask, render_template, jsonify, request
from flask_redis import FlaskRedis
from flask_caching import Cache
from flask_wtf.csrf import CSRFProtect
from config import ProductionConfig
from utilities import AuthorSearchForm, CategoryForm, TitleSearchForm
from models import db, Auteur, Categorie, Livre
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object(ProductionConfig)
csrf = CSRFProtect(app)
db.init_app(app)

# Initialiser Flask-Caching avec Redis
cache = Cache(app=app)
cache.init_app(app)
redis_client = FlaskRedis(app)

# Vérifier si la connexion est établie avec succès
with app.app_context():
    try:
        db.session.execute('SELECT 1')
        print('\n\n---****** Connexion à MySQL réussie ******')
    except Exception as e:
        print('\n\n----------- Connexion échouée ! ERREUR : ', e)


# Afficher la date du jour avec le libellé Biblio
@app.route('/')
def index():
    current_time = datetime.now().strftime("%d-%m-%Y")
    redis_client.set('flask_key', current_time)
    value = redis_client.get('flask_key').decode('utf-8')
    return render_template('index.html', date_du_jour=value)


# Obtenir l'heure actuelle
@app.route('/heure')
def get_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    return jsonify({'Heure': current_time})


# Fonction pour convertir un objet Livre en un dictionnaire JSON
def livre_to_dict(book):
    return {
        'id': book.id,
        'titre': book.titre,
        'description': book.description,
        'isbn': book.isbn,
        'annee_apparition': book.annee_apparition,
        'image': book.image,
        'editeur': {
            'id': book.editeur.id,
            'nom': book.editeur.nom
        },
        'categories': [categorie.nom for categorie in book.categories],
        'auteurs': [auteur.nom for auteur in book.auteurs]
    }


# Afficher la liste de tous les livres avec des informations sur le livre, ses catégories, le(s) auteur(s) et l'éditeur
@app.route('/getAllBooks', methods=['GET'])
def get_all_books():
    livres = Livre.query.all()
    livres_list = [livre_to_dict(livre) for livre in livres]
    return render_template('bootstrap_table.html', title='Liste des livres', data={'livres': livres_list})


# Route pour afficher le formulaire de sélection de catégorie
@app.route('/getBooksByCategory', methods=['GET', 'POST'])
def get_books_by_category():
    form = CategoryForm()

    # Récupérer toutes les catégories depuis la base de données
    categories = Categorie.query.all()
    # Mettre à jour les choix du menu déroulant dans le formulaire
    form.categories.choices = [(str(categorie.id), categorie.nom) for categorie in categories]

    if form.validate_on_submit():
        # Récupérer l'ID de la catégorie sélectionnée
        selected_category_id = int(form.categories.data)

        # Récupérer les livres de la catégorie sélectionnée
        books = Livre.query.join(Livre.categories).filter(Categorie.id == selected_category_id).all()

        books_list = [livre_to_dict(book) for book in books]
        return render_template('books_by_category.html', title='Livres par Catégorie', form=form, data={'livres': books_list})

    return render_template('category_form.html', title='Sélectionner une Catégorie', form=form)


# API pour afficher un livre en particulier avec tous les détails
@app.route('/getBookById/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):

    livre = Livre.query.get(book_id)
    if livre:
        livre_dict = livre_to_dict(livre)
        return render_template('book_by_id.html', title='Livre', data={'livre': livre_dict})
    else:
        return jsonify({'message': 'Livre non trouvé'}), 404


# Route pour rechercher des livres par titre
@app.route('/getBookByTitle', methods=['GET', 'POST'])
def get_books_by_title():
    form = TitleSearchForm()

    if form.validate_on_submit():
        search_title = form.title.data
        # Rechercher des livres dont le titre contient le mot-clé
        books = Livre.query.filter(Livre.titre.ilike(f'%{search_title}%')).all()
        books_list = [livre_to_dict(livre) for livre in books]
        return render_template('books_by_title.html', title='Livres par Titre', form=form, data={'livres': books_list})

    return render_template('title_search_form.html', title='Rechercher par Titre', form=form)


# Route pour rechercher des livres par auteur
@app.route('/getBookByAuthor', methods=['GET', 'POST'])
def get_books_by_author():
    form = AuthorSearchForm()

    if form.validate_on_submit():
        search_author = form.author.data
        # Rechercher des livres dont le nom de l'auteur contient le mot-clé
        books = Livre.query.join(Livre.auteurs).filter(Auteur.nom.ilike(f'%{search_author}%')).all()
        livres_list = [livre_to_dict(livre) for livre in books]
        return render_template('books_by_author.html', title="Livres par Auteur", form=form, data={'livres': livres_list})

    return render_template('author_search_form.html', title="Rechercher par Auteur", form=form)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT"), debug=True)
