from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_redis import FlaskRedis

from flask_wtf.csrf import CSRFProtect
from config import ProductionConfig

app = Flask(__name__)
app.config.from_object(ProductionConfig)
csrf = CSRFProtect(app)
# csrf.init_app(app)
# Configuration de la base de données
#db.init_app(app)
#app.config.from_object('config')
db = SQLAlchemy(app)
redis_client = FlaskRedis(app)

# check if the connection is successfully established or not
with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print('\n\n---****** Connexion a Mysql reussie ******')
    except Exception as e:
        print('\n\n----------- Connexion echoue ! ERROR : ', e)


from . import routes, models