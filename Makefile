# Variables
APP_NAME = biblio
SOURCE_DIR = wsgi/app
TEMPLATE_DIR = $(SOURCE_DIR)/templates
BUILD_DIR = build
FLAKE8 = flake8
BIBLIO_DIR = ./wsgi/app
PYTEST = pytest
TEST_FILE = test_init.py
XML_OUTPUT_FILE = test_results.xml
WSGI_CONTAINER = wsgi1
PROJECT_DIR = /app/app
DOCS_DIR = ./docs
DOC_XML_OUTPUT_FILE = docs.xml

# Règles
.PHONY: all analysis build clean cleanall

all: analysis build

analysis:
	@echo "Running static code analysis..."
#	@docker exec wsgi1 $(FLAKE8) /app/app/__init__.py --ignore=E501,E302,W293,W292 --format=xml --output-file=flake8_report.xml
#	@docker cp wsgi1:app/flake8_report.xml ./flake8_report.xml
	-$(FLAKE8) $(BIBLIO_DIR)/__init__.py --ignore=E501,E302,W293,W292 > rapport_flake8.txt

#build:
#	@echo "Building the project..."
#	# Mettez ici les commandes de construction spécifiques à votre projet Python
#	mkdir -p $(BUILD_DIR)
#	cp -r $(SOURCE_DIR)/__init__.py $(BUILD_DIR)
#	cp -r $(TEMPLATE_DIR) $(BUILD_DIR)
#	# Ajoutez ici d'autres étapes de construction si nécessaire

setup:

test:
	@docker exec wsgi1 $(PYTEST) /app/app/$(TEST_FILE) --junitxml=/app/$(XML_OUTPUT_FILE)
	@docker cp wsgi1:/app/$(XML_OUTPUT_FILE) ./$(XML_OUTPUT_FILE)

docs:
	@docker exec wsgi1 pdoc -o $(DOCS_DIR) $(PROJECT_DIR)
	@docker cp wsgi1:$(DOCS_DIR) ./docs

coverage:
	@docker exec wsgi1 coverage run -m pytest /app/app/$(TEST_FILE)
	@docker exec wsgi1 coverage xml -o /app/coverage.xml
	@docker cp wsgi1:/app/coverage.xml ./coverage.xml


clean:
	@echo "Cleaning up..."
	# Mettez ici les commandes de nettoyage si nécessaire
	rm -rf $(BUILD_DIR)

cleanall: clean
	@echo "Cleaning up all files..."
	# Mettez ici les commandes de nettoyage complet si nécessaire