.PHONY: help install test lint format clean docker-build docker-up docker-down

help: ## Show this help
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

test: ## Run tests
	python manage.py test --verbosity=2

test-coverage: ## Run tests with coverage
	coverage run --source='.' manage.py test
	coverage report
	coverage html

lint: ## Check code (isort, flake8, mypy)
	@echo "Checking imports..."
	isort . --check-only --diff
	@echo "Checking code style..."
	flake8 .
	@echo "Type checking..."
	mypy . --ignore-missing-imports

format: ## Format code
	@echo "Sorting imports..."
	isort .
	@echo "Code formatted!"

clean: ## Clean cache and temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf .coverage

docker-build: ## Build Docker image
	docker-compose build

docker-up: ## Start Docker containers
	docker-compose up -d

docker-down: ## Stop Docker containers
	docker-compose down

docker-logs: ## Show Docker container logs
	docker-compose logs -f

docker-shell: ## Enter container shell
	docker-compose exec web python manage.py shell

docker-migrate: ## Run migrations in container
	docker-compose exec web python manage.py migrate

docker-test: ## Run tests in container
	docker-compose exec web python manage.py test

docker-lint: ## Run code checks in container
	docker-compose exec web make lint

dev-setup: ## Setup development environment
	python -m venv venv
	@echo "Virtual environment created. Activate it:"
	@echo "source venv/bin/activate  # Linux/Mac"
	@echo "venv\\Scripts\\activate     # Windows"
	@echo "Then run: make install"

ci: ## Run all CI checks locally
	make lint
	make test
	python manage.py check --deploy

# Database commands
db-migrate: ## Apply migrations
	python manage.py migrate

db-makemigrations: ## Create new migrations
	python manage.py makemigrations

db-reset: ## Reset database (DANGEROUS!)
	@echo "This will delete all data! Confirm by typing 'yes':"
	@read -p "Confirmation: " confirm && [ "$$confirm" = "yes" ]
	python manage.py flush --no-input

createsuperuser: ## Create superuser
	python manage.py createsuperuser

runserver: ## Run development server
	python manage.py runserver

# Celery commands
celery-worker: ## Start Celery worker
	celery -A config worker --loglevel=info

celery-beat: ## Start Celery beat
	celery -A config beat --loglevel=info

celery-flower: ## Start Celery Flower (monitoring)
	celery -A config flower 