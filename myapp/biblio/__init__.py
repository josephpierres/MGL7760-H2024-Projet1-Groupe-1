import datetime
import logging
import os
from urllib import response
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_redis import FlaskRedis
from flask_wtf.csrf import CSRFProtect
from config import ProductionConfig
# from colorama import Fore, Back, Style


service_name = "biblio-app"

app = Flask(__name__)
#
# Attach OTLP handler to root logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app.config.from_object(ProductionConfig)
FASTAPI_URL="http://biblio_api:8082"

# Initialize CSRF protection, database, and Redis
# csrf = CSRFProtect(app)
redis_client = FlaskRedis(app)

with app.app_context():
    # Instrument Flask, SQLAlchemy, and Redis with OpenTelemetry
    from opentelemetry.instrumentation.flask import FlaskInstrumentor
    from opentelemetry.instrumentation.redis import RedisInstrumentor
    # from opentelemetry.instrumentation.requests import RequestsInstrumentor

    # FlaskInstrumentor().instrument( enable_commenter=True, commenter_options={})
    FlaskInstrumentor().instrument_app(app)   
    RedisInstrumentor().instrument()
    
    # Check if the connection is successfully established or not

    

import time
from biblio.utilities import AuthorSearchForm, CategoryForm, TitleSearchForm


from flask import render_template, request, jsonify, session
import requests
from datetime import datetime


# Routes and Models import
# from . import routes, models
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
        
              
        # Logging the event
        logger.info(f"Page d'accueil chargée avec la date {current_time}")
        
        # Calculate request duration and record it
        duration = (datetime.now() - start_time).total_seconds()        
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
        
        
        # Calculate request duration and record it
        duration = (datetime.now() - start_time).total_seconds()
        
        
        logger.info("Heure actuelle récupérée avec succès")
        return {"Heure": current_time}
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'heure : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500


# Route 3: Récupérer un livre par ID
@app.route('/getBookById/<book_id>', methods=['GET'])
def get_book_by_id(book_id):
    try:
        response = requests.get(f"{FASTAPI_URL}/getBookById/{book_id}")  # Ajout d'ID dans l'URL
        if response.status_code == 200:
            livre = response.json()  # Obtenir les données JSON de la réponse
            return render_template('book_by_id.html', title='Livre', livre=livre)
        else:
            logger.error(f"Erreur lors de la récupération du livre ID {book_id}: {response.status_code}")
            return jsonify({"error": f"Livre non trouvé avec l'ID {book_id}"}), 404
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du livre ID {book_id}: {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500
       

# Route 4: Rechercher des livres par titre
@app.route('/getBookByTitle', methods=['GET', 'POST'])
def get_books_by_title():
    form = TitleSearchForm()
    
    try:
        if form.validate_on_submit():
            search_title = form.title.data
            response = requests.get(f"{FASTAPI_URL}/getBookByTitle", params={"search_title": search_title})
            if response.status_code == 200:
                livres = response.json()  # Récupérer les livres en JSON
                logger.info(f"{len(livres)} livres trouvés pour la recherche de titre '{search_title}'")
                return render_template('books_by_title.html', title='Livres par Titre', form=form, data={'livres': livres})
            else:
                logger.warning(f"Aucun livre trouvé pour le titre '{search_title}'")
                return jsonify({"error": "Aucun livre trouvé"}), 404
        
        return render_template('title_search_form.html', title='Rechercher par Titre', form=form)
    except Exception as e:
        logger.error(f"Erreur lors de la recherche de livres par titre : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

    
# Route 6: Rechercher tous les livres 
@app.route('/getAllBooks', methods=['GET'])
def get_all_books():   
    try:
        response = requests.get(f"{FASTAPI_URL}/getAllBooks")
        if response.status_code == 200:
            livres = response.json()  # Obtenir les livres en JSON
            logger.info(f"{len(livres)} livres récupérés et affichés avec succès")
            return render_template('bootstrap_table.html', title='Liste des livres', data={'livres': livres})
        else:
            logger.warning("Aucun livre trouvé")
            return jsonify({"error": "Aucun livre trouvé"}), 404
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de tous les livres - front-end : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500
        
    

    
@app.route('/getBookByAuthor', methods=['GET', 'POST'])
def get_books_by_author():
    form = AuthorSearchForm()
    try:
        if form.validate_on_submit():
            search_author = form.author.data
            response = requests.get(f"{FASTAPI_URL}/getBookByTitle", params={"search_author": search_author})
            if response.status_code == 200:
                livres = response.json()  # Récupérer les livres en JSON
                logger.info(f"{len(livres)} livres trouvés pour la recherche de l'auteur '{search_author}'")
                return render_template('books_by_author.html', title='Livres par Auteur', form=form, data={'livres': livres})
            else:
                logger.warning(f"Aucun livre trouvé pour l'auteur '{search_author}'")
                return jsonify({"error": "Aucun livre trouvé"}), 404
        
        return render_template('author_search_form.html', title='Rechercher par Titre', form=form)
    except Exception as e:
        logger.error(f"Erreur lors de la recherche de livres par titre : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500


@app.route('/getBooksByCategory', methods=['GET', 'POST'])
def get_books_by_category():
    logging.info("Hello World4")
    return {"message": "Hello World6"}





