from biblio import app
from flask import render_template
from datetime import datetime

#
# Phase 1: Affichage de la date du jour avec le libelle Biblio
#


@app.route('/')
def index():
    current_time = datetime.now().strftime("%d-%m-%Y")
    return render_template('index.html', date_du_jour = current_time)

# flask health check
@app.route('/heure')
def get_time():
    current_time = datetime.now().strftime("%H:%M:%S")    
    return { 'Heure': current_time }

