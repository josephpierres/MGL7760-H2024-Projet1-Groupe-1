# import logging
from biblio.utilities import AuthorSearchForm, CategoryForm, TitleSearchForm
from . import app, redis_client, logger, tracer, meter
from flask import render_template, request, jsonify, session
from biblio.models import Auteur, Categorie, Livre
from datetime import datetime
# from opentelemetry import trace
# from prometheus_client import start_http_server, Counter, Gauge




# # Prometheus metrics for request counting and latency
# start_http_server(8000)  # Prometheus server on port 8000

# request_counter = Counter("request_count", "Number of requests", ["method", "endpoint"])
# latency_gauge = Gauge("request_latency_seconds", "Request latency", ["endpoint"])

# OpenTelemetry metrics 
request_counter = meter.create_counter(
    name="requests",
    description="number of requests",
    unit="1",    
)

# request_gauge = meter.create_gauge(name, unit='', description='')

#
# Phase 1: Affichage de la date du jour avec le libelle Biblio
#
@app.route('/')
def index():
    logger.warning(" In index page")
    try:
        with tracer.start_as_current_span("index"):
            current_time = datetime.now().strftime("%d-%m-%Y")
            redis_client.set('flask_key', current_time)
            value = redis_client.get('flask_key').decode('utf-8')
            request_counter.add(1)
            logger.info(f"Page d'accueil chargée avec la date {current_time}")
            return render_template('index.html', date_du_jour=value)
    except Exception as e:
        logger.error(f"Erreur lors de l'accès à la page d'accueil : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500


# flask health check
@app.route('/heure')
def get_time():
    try:
        current_time = datetime.now().strftime("%H:%M:%S")
        logger.info(f"Heure actuelle {current_time} affichée avec succès")
        return { 'Heure': current_time }
    except Exception as e:
        logger.error(f"Erreur lors de l'accès à l'heure actuelle : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500


#
#Phase 2: Affichage des livres
#
def livre_to_dict(book):
    """Convertir un objet Livre en dictionnaire pour JSON"""
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

@app.route('/getAllBooks', methods=['GET'])
def get_all_books():
    with tracer.start_as_current_span("get_all_books"):
        try:
            livres = Livre.query.all()
            livres_list = [livre_to_dict(livre) for livre in livres]
            request_counter.add(1)
            logger.info(f"{len(livres_list)} livres récupérés et affichés avec succès")
            return render_template('bootstrap_table.html', title='Liste des livres', data={'livres': livres_list})
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de tous les livres : {str(e)}")
            return jsonify({"error": "Erreur interne du serveur"}), 500


@app.route('/getBooksByCategory', methods=['GET', 'POST'])
def get_books_by_category():
    form = CategoryForm()
    try:
        categories = Categorie.query.all()
        form.categories.choices = [(str(categorie.id), categorie.nom) for categorie in categories]
        logger.info(f"{len(categories)} catégories récupérées pour la sélection")
        
        if form.validate_on_submit():
            selected_category_id = int(form.categories.data)
            books = Livre.query.join(Livre.categories).filter(Categorie.id == selected_category_id).all()
            books_list = [livre_to_dict(book) for book in books]
            logger.info(f"{len(books_list)} livres récupérés pour la catégorie ID {selected_category_id}")
            return render_template('books_by_category.html', title='Livres par Catégorie', form=form, data={'livres': books_list})

        return render_template('category_form.html', title='Sélectionner une Catégorie', form=form)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des livres par catégorie : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500


@app.route('/getBookById/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    try:
        livre = Livre.query.get(book_id)
        if livre:
            livre_dict = livre_to_dict(livre)
            logger.info(f"Livre ID {book_id} récupéré avec succès")
            return render_template('book_by_id.html', title='Livre', data={'livre': livre_dict})
        else:
            logger.warning(f"Livre ID {book_id} non trouvé")
            return jsonify({'message': 'Livre non trouvé'}), 404
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du livre ID {book_id} : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500


@app.route('/getBookByTitle', methods=['GET', 'POST'])
def get_books_by_title():
    form = TitleSearchForm()
    try:
        if form.validate_on_submit():
            search_title = form.title.data
            books = Livre.query.filter(Livre.titre.ilike(f'%{search_title}%')).all()
            books_list = [livre_to_dict(livre) for livre in books]
            logger.info(f"{len(books_list)} livres trouvés pour la recherche de titre '{search_title}'")
            return render_template('books_by_title.html', title='Livres par Titre', form=form, data={'livres': books_list})

        return render_template('title_search_form.html', title='Rechercher par Titre', form=form)
    except Exception as e:
        logger.error(f"Erreur lors de la recherche de livres par titre : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500


@app.route('/getBookByAuthor', methods=['GET', 'POST'])
def get_books_by_author():
    form = AuthorSearchForm()
    try:
        if form.validate_on_submit():
            search_author = form.author.data
            books = Livre.query.join(Livre.auteurs).filter(Auteur.nom.ilike(f'%{search_author}%')).all()
            livres_list = [livre_to_dict(livre) for livre in books]
            logger.info(f"{len(livres_list)} livres trouvés pour l'auteur '{search_author}'")
            return render_template('books_by_author.html', title="Livres par Auteur", form=form, data={'livres': livres_list})

        return render_template('author_search_form.html', title="Rechercher par Auteur", form=form)
    except Exception as e:
        logger.error(f"Erreur lors de la recherche de livres par auteur : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500
