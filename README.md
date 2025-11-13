# 📚 Book Manager API

[![CI/CD Pipeline](https://github.com/Guenang/book-manager-api/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Guenang/book-manager-api/actions/workflows/ci-cd.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)

API REST moderne pour gérer une bibliothèque de livres avec architecture hexagonale.

## 🚀 Fonctionnalités

- ✅ CRUD complet (Create, Read, Update, Delete)
- ✅ Recherche de livres
- ✅ Système de notation (1-5 étoiles)
- ✅ Statistiques de bibliothèque
- ✅ Architecture hexagonale (Ports & Adapters)
- ✅ Tests automatisés (80%+ couverture)
- ✅ Documentation interactive (Swagger UI)
- ✅ Déploiement automatique (CI/CD)

## 🏗️ Architecture

```
Domain (Cœur métier)
    ↓
Ports (Interfaces)
    ↓
Adapters (SQLAlchemy, In-Memory)
    ↓
API (FastAPI)
```

## 🛠️ Technologies

- **Backend**: Python 3.12, FastAPI, SQLAlchemy
- **Base de données**: PostgreSQL (prod), SQLite (dev)
- **Tests**: Pytest, pytest-cov
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Déploiement**: Render.com
- **CI/CD**: GitHub Actions

## 📦 Installation locale

```bash
# Cloner le repo
git clone https://github.com/Guenang/book-manager-api.git
cd book-manager-api

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'API
uvicorn main:app --reload

# Lancer les tests
pytest tests/ -v
```

## 🌐 API Endpoints

- `GET /` - Infos de l'API
- `GET /docs` - Documentation Swagger
- `POST /books/` - Créer un livre
- `GET /books/` - Lister tous les livres
- `GET /books/{id}` - Récupérer un livre
- `PUT /books/{id}` - Modifier un livre
- `DELETE /books/{id}` - Supprimer un livre
- `GET /books/search?q=...` - Rechercher
- `GET /books/stats` - Statistiques

## 🧪 Tests

```bash
# Tous les tests
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=. --cov-report=html

# Tests spécifiques
pytest tests/test_domain.py -v
```

## 📝 Licence

MIT

## 👤 Auteur

Guenang

## 📝 Étape 3 : Créer `.gitignore` (si pas déjà fait)

```

# Python

**pycache**/
_.py[cod]
_$py.class
_.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
_.egg-info/
.installed.cfg
\*.egg

# Virtual environments

venv/
ENV/
env/

# IDEs

.vscode/
.idea/
_.swp
_.swo
\*~

# Testing

.pytest_cache/
.coverage
htmlcov/
.tox/
coverage.xml

# Databases

_.db
_.sqlite
\*.sqlite3

# Environment variables

.env
.env.local

# OS

.DS_Store
Thumbs.db

# Logs

\*.log
```
