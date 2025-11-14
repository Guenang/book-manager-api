.PHONY: help build up down logs test clean

help:
	@echo "🐳 Docker Commands:"
	@echo "  make build   - Build containers"
	@echo "  make up      - Start containers"
	@echo "  make down    - Stop containers"
	@echo "  make logs    - View logs"
	@echo "  make test    - Run tests in container"
	@echo "  make clean   - Clean everything"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "✅ API: http://localhost:8000"
	@echo "✅ Docs: http://localhost:8000/docs"

down:
	docker-compose down

logs:
	docker-compose logs -f api

test:
	docker-compose exec api pytest tests/ -v

clean:
	docker-compose down -v
	docker system prune -f