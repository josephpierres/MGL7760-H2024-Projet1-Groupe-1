from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text
import os
import logging
from time import sleep

from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from instrument_logging import LogsInstrumentor
from instrument_tracing import TracesInstrumentor
from instrument_metrics import MetricsInstrumentor
from prometheus_client import Counter, Histogram, Gauge
import uvicorn
from sqlalchemy.orm import Session
from models import Base
from crud import ( get_all_books as all_books, 
                  get_book_by_id as book_by_id, 
                  get_books_by_author as books_by_author, 
                  get_books_by_category as books_by_category,
                  get_books_by_title as books_by_title)
from database import SessionLocal, engine

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Flask Front-end origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency pour la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

service_name = "biblio-app"
otlp_endpoint = os.environ.get("OTLP_GRPC_ENDPOINT", "http://localhost:4317")

# Instrument tracing
tracer = TracesInstrumentor(app=app, service_name=service_name, otlp_endpoint=otlp_endpoint, excluded_urls="/metrics")

# Instrument logging
handler = LogsInstrumentor(service_name=service_name)
logging.getLogger().addHandler(handler)

# Send test message to log
logging.info(f"{service_name} started, listening on port 8082")

# Instrument metrics
MetricsInstrumentor(app=app, service_name=service_name)

g = Gauge('my_inprogress_requests', 'Description of gauge')
g.set_to_current_time()

h = Histogram('request_latency_seconds', 'Description of histogram')
h.observe(4.7)

c = Counter('my_failures', 'Description of counter')

# Instrument database
SQLAlchemyInstrumentor().instrument(
    engine=engine,
    tracer_provider=tracer,
    enable_commenter=True,
    commenter_options={},
)

# Route 1: Affichage de la date du jour avec le libellé Biblio
@app.get("/")
def root_endpoint():
    logging.info("Hello World")
    return {"message": "Hello World"}

# Route 2: Health check - Heure actuelle
@app.get('/heure')
def get_time():
    start_time = datetime.now()
    try:
        current_time = datetime.now().strftime("%H:%M:%S")
        duration = (datetime.now() - start_time).total_seconds()
        logging.info("Heure actuelle récupérée avec succès")
        return {"Heure": current_time}
    except Exception as e:
        logging.error(f"Erreur lors de la récupération de l'heure : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

# Route 3: Récupérer un livre par ID
@app.get('/getBookById/{book_id}')
def get_book_by_id(book_id, db: Session = Depends(get_db)):
    start_time = datetime.now()
    try:
        livre = book_by_id(book_id, db)  # Appel de la fonction CRUD sans conflit
        if livre:
            duration = (datetime.now() - start_time).total_seconds()
            logging.info(f"Livre ID {book_id} récupéré avec succès")
            return livre
        else:
            logging.warning(f"Livre ID {book_id} non trouvé")
            raise HTTPException(status_code=404, detail="Livre non trouvé")
    except Exception as e:
        logging.error(f"Erreur lors de la récupération du livre ID {book_id} : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

# Route 4: Rechercher des livres par titre
@app.get('/getBooksByTitle/{search_title}')
def get_books_by_title(search_title, db: Session = Depends(get_db)):
    try:
        books = books_by_title(search_title, db)
        logging.info(f"{len(books)} livres trouvés pour la recherche de titre '{search_title}'")
        return books
    except Exception as e:
        logging.error(f"Erreur lors de la recherche de livres par titre : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

# Route 5: Rechercher des livres par auteur
@app.get('/getBooksByAuthor/{search_author}')
def get_books_by_author(search_author, db: Session = Depends(get_db)):
    try:
        books = books_by_author(search_author, db)
        logging.info(f"{len(books)} livres trouvés pour l'auteur '{search_author}'")
        return books
    except Exception as e:
        logging.error(f"Erreur lors de la recherche de livres par auteur : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

# Route 6: Rechercher tous les livres
@app.get("/getAllBooks")
def get_all_books(db: Session = Depends(get_db)):
    try:
        livres = all_books(db)
        if livres:
            logging.info(f"{len(livres)} livres récupérés et affichés avec succès")
            return livres
        else:
            logging.warning("Aucun livre trouvé.")
            raise HTTPException(status_code=404, detail="Aucun livre trouvé")
    except Exception as e:
        logging.error(f"Erreur lors de la récupération de tous les livres-back-end : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

# Route 7: Rechercher des livres par categorie
@app.get('/getBooksByCategory/{selected_category_id}')
def get_books_by_category(selected_category_id, db: Session = Depends(get_db)):
    try:
        books = books_by_category(selected_category_id, db)
        logging.info(f"{len(books)} livres récupérés pour la catégorie ID {selected_category_id}")
        return books
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des livres par catégorie : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

# Vérification de la connexion à MySQL
try:
    db = SessionLocal()
    db.execute(text('SELECT 1'))
    logging.info('---****** Connexion à MySQL réussie ******')
    print('\n\n---****** Connexion a Mysql reussie ******')
except Exception as e:
    logging.error(f'----------- Connexion échouée ! ERROR : {e}')
    print('\n\n----------- Connexion echoue ! ERROR : ', e)
finally:
    db.close()

if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = (
        "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
        "[trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    )
    uvicorn.run(app, host="0.0.0.0", port=8082, log_config=log_config)
