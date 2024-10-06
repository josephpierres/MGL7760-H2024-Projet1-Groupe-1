import logging
import os
import time
from biblio.utilities import AuthorSearchForm, CategoryForm, TitleSearchForm
from biblio.instrument_tracing import TracesInstrumentor
from . import app, redis_client, logger
from flask import render_template, request, jsonify, session
from biblio.models import Auteur, Categorie, Livre
from datetime import datetime
from prometheus_client import make_wsgi_app, Counter, Histogram


service_name = "biblio-app"
otlp_endpoint = os.environ.get("OTLP_GRPC_ENDPOINT", "localhost:4317")

TracesInstrumentor(app=app, service_name=service_name, otlp_endpoint=otlp_endpoint, excluded_urls="/metrics")
# OpenTelemetry metrics
request_counter = Counter(
    'app_request_count',
    'Application Request Count',
    ['method', 'endpoint', 'http_status']
)

request_histogram = Histogram(
    'app_request_latency_seconds',
    'Application Request Latency',
    ['method', 'endpoint']
)

# Route 1: Affichage de la date du jour avec le libellé Biblio
@app.route('/')
def index():
    logger.warning(" In index page")
    start_time = datetime.now()   
    try:
        # Start the timer
        current_time = datetime.now().strftime("%d-%m-%Y")
        redis_client.set('flask_key', current_time)
        value = redis_client.get('flask_key').decode('utf-8')
        
        # Increment the counter for requests
        request_counter.labels('GET', '/', 200).inc()
        
        # Logging the event
        logger.info(f"Page d'accueil chargée avec la date {current_time}")
        
        # Calculate request duration and record it
        duration = (datetime.now() - start_time).total_seconds()        
        request_histogram.labels('GET', '/').observe(duration)
        return render_template('index.html', date_du_jour=value)
    except Exception as e:
        logger.error(f"Erreur lors de l'accès à la page d'accueil : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500


# Route 2: Health check - Heure actuelle
@app.route('/heure')
def get_time():
    start_time = datetime.now()
   
    try:
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Increment the counter for this request
        request_counter.labels('GET', '/heure', 200).inc()
        
        # Calculate request duration and record it
        duration = (datetime.now() - start_time).total_seconds()
        
        request_histogram.labels('GET', '/heure').observe(duration)
        logger.info("Heure actuelle récupérée avec succès")
        return jsonify({"heure": current_time})
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'heure : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500


# Route 3: Récupérer un livre par ID
@app.route('/getBookById/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    start_time = datetime.now()
   
    try:
        livre = Livre.query.get(book_id)
        if livre:
            request_counter.labels('GET', '/getBook', 200).inc()
            duration = (datetime.now() - start_time).total_seconds()
            
            logger.info(f"Livre ID {book_id} récupéré avec succès") 
                
        
            livre_dict = livre_to_dict(livre)
            logger.info(f"Livre ID {book_id} récupéré avec succès")
            request_histogram.labels('GET', '/').observe(duration)
            return render_template('book_by_id.html', title='Livre', data={'livre': livre_dict})
        else:
            logger.warning(f"Livre ID {book_id} non trouvé")
            return jsonify({"message": "Livre non trouvé"}), 404
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du livre ID {book_id} : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500


# Route 4: Rechercher des livres par titre
@app.route('/getBookByTitle', methods=['GET', 'POST'])
def get_books_by_title():
    form = TitleSearchForm()
    
    try:
        if form.validate_on_submit():
            search_title = form.title.data
            books = Livre.query.filter(Livre.titre.ilike(f'%{search_title}%')).all()
            books_list = [livre.to_dict() for livre in books]
            
            # Log number of books found
            logger.info(f"{len(books_list)} livres trouvés pour la recherche de titre '{search_title}'")
            
            request_counter.labels('POST', '/getBookByTitle', 200).inc()
            return render_template('books_by_title.html', title='Livres par Titre', form=form, data={'livres': books_list})
        
        return render_template('title_search_form.html', title='Rechercher par Titre', form=form)
    except Exception as e:
        logger.error(f"Erreur lors de la recherche de livres par titre : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500


# Route 5: Rechercher des livres par auteur
@app.route('/getBookByAuthor', methods=['GET', 'POST'])
def get_books_by_author():
    form = AuthorSearchForm()
   
    try:
        if form.validate_on_submit():
            search_author = form.author.data
            books = Livre.query.join(Livre.auteurs).filter(Auteur.nom.ilike(f'%{search_author}%')).all()
            livres_list = [livre_to_dict(livre) for livre in books]
            
            logger.info(f"{len(livres_list)} livres trouvés pour l'auteur '{search_author}'")
            
            request_counter.labels('GET', '/', 200).inc()
            return render_template('books_by_author.html', title="Livres par Auteur", form=form, data={'livres': livres_list})
        
        return render_template('author_search_form.html', title="Rechercher par Auteur", form=form)
    except Exception as e:
        logger.error(f"Erreur lors de la recherche de livres par auteur : {str(e)}")
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

# Route 6: Rechercher tous les livres 
@app.route('/getAllBooks', methods=['GET'])
def get_all_books():
   
    try:
        livres = Livre.query.all()
        livres_list = [livre_to_dict(livre) for livre in livres]
        request_counter.labels('GET', '/getAllBooks', 200).inc()
        logger.info(f"{len(livres_list)} livres récupérés et affichés avec succès")
        return render_template('bootstrap_table.html', title='Liste des livres', data={'livres': livres_list})
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de tous les livres : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

# Route 7: Rechercher des livres par categorie
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


# @app.route('/getBookById/<int:book_id>', methods=['GET'])
# def get_book_by_id(book_id):
#     try:
#         livre = Livre.query.get(book_id)
#         if livre:
#             livre_dict = livre_to_dict(livre)
#             logger.info(f"Livre ID {book_id} récupéré avec succès")
#             return render_template('book_by_id.html', title='Livre', data={'livre': livre_dict})
#         else:
#             logger.warning(f"Livre ID {book_id} non trouvé")
#             return jsonify({'message': 'Livre non trouvé'}), 404
#     except Exception as e:
#         logger.error(f"Erreur lors de la récupération du livre ID {book_id} : {str(e)}")
#         return jsonify({"error": "Erreur interne du serveur"}), 500


# @app.route('/getBookByTitle', methods=['GET', 'POST'])
# def get_books_by_title():
#     form = TitleSearchForm()
#     try:
#         if form.validate_on_submit():
#             search_title = form.title.data
#             books = Livre.query.filter(Livre.titre.ilike(f'%{search_title}%')).all()
#             books_list = [livre_to_dict(livre) for livre in books]
#             logger.info(f"{len(books_list)} livres trouvés pour la recherche de titre '{search_title}'")
#             return render_template('books_by_title.html', title='Livres par Titre', form=form, data={'livres': books_list})

#         return render_template('title_search_form.html', title='Rechercher par Titre', form=form)
#     except Exception as e:
#         logger.error(f"Erreur lors de la recherche de livres par titre : {str(e)}")
#         return jsonify({"error": "Erreur interne du serveur"}), 500


# @app.route('/getBookByAuthor', methods=['GET', 'POST'])
# def get_books_by_author():
#     form = AuthorSearchForm()
#     try:
#         if form.validate_on_submit():
#             search_author = form.author.data
#             books = Livre.query.join(Livre.auteurs).filter(Auteur.nom.ilike(f'%{search_author}%')).all()
#             livres_list = [livre_to_dict(livre) for livre in books]
#             logger.info(f"{len(livres_list)} livres trouvés pour l'auteur '{search_author}'")
#             return render_template('books_by_author.html', title="Livres par Auteur", form=form, data={'livres': livres_list})

#         return render_template('author_search_form.html', title="Rechercher par Auteur", form=form)
#     except Exception as e:
#         logger.error(f"Erreur lors de la recherche de livres par auteur : {str(e)}")
#         return jsonify({"error": "Erreur interne du serveur"}), 500