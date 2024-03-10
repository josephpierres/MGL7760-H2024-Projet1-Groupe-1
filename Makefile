.PHONY: setup test clean run start exec
# Defines the default target that `make` will to try to make, or in the case of a phony target, execute the specified commands
# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help
SUBDIRS = wsgi

help:
	@echo "---------------HELP-----------------"
	@echo "To setup the project type make setup"
	@echo "To test the project type make test"
	@echo "To run the project type make run"
	@echo "------------------------------------"
clean: clean-build clean-pyc destroy
	

flake8:
	@docker exec wsgi1 flake8 --extend-ignore E203,W234,E225,E501 ./biblio/models.py --format=html --htmldir=flake-report

test-coverage: ## Cleanup and deactivate venv
	cd wsgi && $(MAKE) test

test: ## Run pytest
	@docker exec wsgi1 pytest . --junitxml=/app/pytest.xml
	@docker cp wsgi1:/app/pytest.xml ./pytest.xml

docs: ## Build docker image
	@docker exec wsgi1 pdoc --output-dir app/docs /app/biblio
	@docker cp wsgi1:app/docs ./docs

setup:  ## sets up environment and installs requirements
	@docker compose up -d

coverage-check: ## Create docker image
	@docker exec wsgi1 coverage run -m pytest .
	@docker exec wsgi1 coverage xml -o /app/coverage.xml
	@docker cp wsgi1:/app/coverage.xml ./coverage.xml
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: # type: ignore
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
 
destroy: ## build, start and run docker image
	docker compose down
	docker network rm -f front_network back_network
	docker stop $(docker ps -q)
	docker rmi -f nginx:1.25.3
	docker rmi -f wsgi0:1.0  wsgi1:1.0 wsgi2:1.0
	docker rmi -f redis:7.2.4
	docker rmi -f mysql:8.0.22
	docker volume rm -f mysql_volume
	docker system prune -f