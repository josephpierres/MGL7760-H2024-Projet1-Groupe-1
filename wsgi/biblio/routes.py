from biblio.utilities import AuthorSearchForm, CategoryForm, TitleSearchForm
from . import app, redis_client, cache
from flask import render_template, request, jsonify, session
from flask_wtf import csrf, Form
from biblio.models import Auteur, Categorie, Livre
from datetime import datetime
import json

#
# Phase 1: Affichage de la date du jour avec le libelle Biblio
#


@app.route('/')
def index():    
    current_time = datetime.now().strftime("%d-%m-%Y")
    redis_client.set('flask_key', current_time)
    value = redis_client.get('flask_key').decode('utf-8')
    return render_template('index.html', date_du_jour = value)

# flask health check
@app.route('/heure')
def get_time():
    current_time = datetime.now().strftime("%H:%M:%S")    
    return { 'Heure': current_time }

#
#Phase 2: 
#

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


# Fonction pour générer une clé de cache unique basée sur l'URL de la requête
def make_cache_key(*args, **kwargs):
    return request.url


# Afficher la liste de tous les livres avec des informations sur le livre, ses catégories, le(s) auteur(s) et l'éditeur
@app.route('/getAllBooks', methods=['GET'])
#@cache.cached(timeout=300, key_prefix=make_cache_key)
def get_all_books():
    livres = Livre.query.all()
    livres_list = [livre_to_dict(livre) for livre in livres]    
    return render_template('bootstrap_table.html', title='Liste des livres', data={'livres': livres_list})

#
# Phase 3



# Route pour afficher le formulaire de sélection de catégorie
@app.route('/getBooksByCategory', methods=['GET', 'POST'])
#@cache.cached(timeout=300, key_prefix=make_cache_key)
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
#@cache.cached(timeout=300, key_prefix=make_cache_key)
def get_book_by_id(book_id):
   
    livre = Livre.query.get(book_id)
    if livre:
        livre_dict = livre_to_dict(livre)
        return render_template('book_by_id.html', title='Livre', data={'livre': livre_dict})
    else:
        return jsonify({'message': 'Livre non trouvé'}), 404

# Route pour rechercher des livres par titre
@app.route('/getBookByTitle', methods=['GET', 'POST'])
#@cache.cached(timeout=300, key_prefix=make_cache_key)
def get_books_by_title():
    form = TitleSearchForm()
   
    if form.validate_on_submit():
        search_title = form.title.data
        # Rechercher des livres dont le titre contient le mot-clé
        books = Livre.query.filter(Livre.titre.ilike(f'%{search_title}%')).all()
        #books_list = []
        #title = request.args.get('title')
        #livres = Livre.query.filter(Livre.titre.ilike(f'%{title}%')).all()
        books_list = [livre_to_dict(livre) for livre in books]
        return render_template('books_by_title.html', title='Livres par Titre', form=form, data={'livres': books_list})

    return render_template('title_search_form.html', title='Rechercher par Titre', form=form)

# Route pour rechercher des livres par auteur
@app.route('/getBookByAuthor', methods=['GET', 'POST'])
#@cache.cached(timeout=300, key_prefix=make_cache_key)
def get_books_by_author():
    form = AuthorSearchForm()
    
    if form.validate_on_submit():
        search_author = form.author.data
        # Rechercher des livres dont le nom de l'auteur contient le mot-clé
        books = Livre.query.join(Livre.auteurs).filter(Auteur.nom.ilike(f'%{search_author}%')).all()
        #books_list = []
        #author = request.args.get('author')
        #livres = Livre.query.filter(Livre.auteurs.any(nom=author)).all()
        livres_list = [livre_to_dict(livre) for livre in books]
        return render_template('books_by_author.html', title="Livres par Auteur", form=form, data={'livres': livres_list})

    return render_template('author_search_form.html', title="Rechercher par Auteur", form=form)


