# appel du package app qui a le fichier __init__.py et views.py
from biblio import app
import os
if __name__ == "__main__":
    app.run(host='0.0.0.0')
   