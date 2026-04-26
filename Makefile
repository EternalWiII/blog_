# =============================================================================
# Makefile - Django Blog
# Requires: Python 3.12, PostgreSQL, GNU Make
# =============================================================================

PYTHON = py -3.12

.PHONY: help install setup migrate run test lint freeze clean superuser

help:
	@echo "Django Blog - available commands:"
	@echo "  make setup      Full setup from scratch"
	@echo "  make install    Install dependencies"
	@echo "  make run        Start server at 127.0.0.1:8000"
	@echo "  make migrate    Run makemigrations + migrate"
	@echo "  make test       Run all tests"
	@echo "  make lint       Check code style with flake8"
	@echo "  make superuser  Create admin superuser"
	@echo "  make freeze     Update requirements.txt"
	@echo "  make clean      Remove __pycache__ and .pyc files"

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

setup: install
	$(PYTHON) -c "import shutil, os; shutil.copy('.env.example', '.env') if not os.path.exists('.env') else print('.env already exists')"
	@echo "Setup complete. Fill in .env, then run: make migrate"

migrate:
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate

run:
	$(PYTHON) manage.py runserver

superuser:
	$(PYTHON) manage.py createsuperuser

test:
	$(PYTHON) manage.py test --verbosity=2

lint:
	$(PYTHON) -m pip install flake8 --quiet
	$(PYTHON) -m flake8 accounts/ blog/ config/ --max-line-length=120 --exclude=migrations

freeze:
	$(PYTHON) -m pip freeze > requirements.txt

clean:
	$(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc')]"
	@echo "Done."
