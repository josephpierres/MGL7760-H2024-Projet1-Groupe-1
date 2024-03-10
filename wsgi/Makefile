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
	$(PYTHON) -m flake8 --extend-ignore E203,W234,E225,E501 ./biblio/models.py

# Exécutez les tests unitaires avec pytest
test: $(VENV)
	$(PYTHON) -m pytest . -p no:logging -p no:warnings

# Générez la documentation avec pdoc
docs: $(VENV)
	$(PYTHON) -m pdoc --output-dir docs ./biblio

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
		source ./$</bin/activate ; set -u ;\
        $(PIP) install --upgrade pip; \
        $(PIP) install coverage flake8 pytest pdoc; \
        python3 -m pip install coverage flake8 pytest pdoc; \
    )
