Session	Hiver 2024
Sigle	MGL7760
Groupe	01
Crédits	3
Titre	Qualité et productivité des outils logiciels
Liens utiles	Site du cours. Fiche du cours. Plan de cours.
Projet 1 : creation d'une base de donnee de gestion de Bibliotheque 





.DEFAULT_GOAL = help
.PHONY: setup test clean run start exec
# VENV = .venv
# #ACTIVATE_VENV := source ./$(VENV)/bin/activate # . $(VENV)/bin/activate
# PYTHON := $(VENV)/bin/python3
# PIP = $(VENV)/bin/pip
# COVERAGE = $(VENV)/bin/coverage
# activate:
#     $(PYTHON) -m venv $(VENV)
#     $(PYTHON) -m pip install --upgrade pip
#     $(PYTHON) -m pip install -r requirements.txt
#     source ./$(VENV)/bin/activate
#     # $(PIP) install -r requirements.txt
#     # touch $(VENV)/bin/activate
setup:
    #@echo "Hello je suis dans le setup"
    # $(ACTIVATE_VENV) && $(PYTHON) -m pip install --editable .
clean:
    rm -rf *.egg-info
    rm -rf build
    rm -rf dist
    rm -rf .pytest_cache
    # Remove all pycache
    find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
    rm -rf .venv
    rm -rf flake8_report.xml
    rm -rf coverage_report.xml
    rm -rf docs
test: $(VENV)
    ${PYTHON} -m pytest . -p no:logging -p no:warnings
test-coverage: $(VENV)
    $(COVERAGE) run -m pytest . -p no:logging -p no:warnings
    $(COVERAGE) xml -o coverage_report.xml
flake8: $(VENV)
    flake8 . --format=xml --output-file=flake8_report.xml src
docs: $(VENV)
    pdoc --output-dir docs .
    touch docs/.nojekyll  # Pour éviter que GitHub Pages ne traite pas le dossier docs comme un site Jekyll
coverage-check: $(VENV)
    $(COVERAGE) report --fail-under=80
# fake target
.PHONY: run clean















# Makefile pour votre projet Python

# Variables
VENV = .venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
COVERAGE := $(VENV)/bin/coverage

# Cibles
.PHONY: setup lint test docs coverage-check

# Installez les dépendances et créez un environnement virtuel
setup: $(VENV)
	@echo "Initialisation de l'environnement virtuel..."
	$(PIP) install -r requirements.txt

# Exécutez l'analyse statique du code avec Flake8
lint: $(VENV)
	$(PYTHON) -m flake8 .

# Exécutez les tests unitaires avec pytest
test: $(VENV)
	$(PYTHON) -m pytest . -p no:logging -p no:warnings

# Générez la documentation avec pdoc
docs: $(VENV)
	$(PYTHON) -m pdoc --output-dir docs .

# Vérifiez la couverture du code avec coverage
coverage-check: $(VENV)
	$(COVERAGE) run -m pytest . -p no:logging -p no:warnings
	$(COVERAGE) xml -o coverage_report.xml

# Rapport de qualité au format XML pour Jenkins
quality-report: lint test coverage-check
	@echo "Génération du rapport de qualité XML pour Jenkins..."
	# Ajoutez ici les commandes pour générer d'autres rapports (par exemple, pylint, etc.)

# Créez l'environnement virtuel
$(VENV):
    ( \ 
	python3 -m venv $(VENV); \
    source .venv/bin/activate; \
	$(PIP) install --upgrade pip; \
	$(PIP) install coverage flake8 pytest pdoc; \
    python -m pip install coverage flake8 pytest pdoc; 
*******************************************************






.PHONY: setup activate test clean run start exec

VENV = .venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
ACTIVATE_VENV := 

setup: active ## sets up environment and installs requirements
	@echo "Hello je suis dans le setup"
active: ## sets up environment and installs requirements
	( \
       source .venv/bin/activate; \
       pip install -r requirements.txt; \
    )