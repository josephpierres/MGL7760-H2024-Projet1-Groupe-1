.PHONY: setup test clean run start exec

clean: ## Remove build and cache files
 cd wsgi && $(MAKE) clean

flake8: 
 cd wsgi && $(MAKE) flake8

test-coverage: ## Cleanup and deactivate venv
 cd wsgi && $(MAKE) test-coverage

test: ## Run pytest
 cd wsgi && $(MAKE) test

docs: ## Build docker image
 cd wsgi && $(MAKE) docs

setup: ## sets up environment and installs requirements
: ## Build docker image
 cd wsgi && $(MAKE) setup

coverage-check:: ## Create docker image
 cd wsgi && $(MAKE) coverage-check:
 
run: ## build, start and run docker image
docker run -it --rm -dp 8080:80 -v "$(pwd)/configs:/etc/nginx/conf.d" --name biblio_nginx nginx
 

 