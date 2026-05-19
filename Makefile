.PHONY: help install dev build docker-up docker-down clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies
	cd backend && pip install -e .
	cd frontend && npm install

dev: ## Start development servers
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
	cd frontend && npm run dev

dev-backend: ## Start backend only
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Start frontend only
	cd frontend && npm run dev

build: ## Build for production
	cd frontend && npm run build

docker-up: ## Start with Docker Compose
	docker-compose up --build -d

docker-down: ## Stop Docker Compose
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

clean: ## Clean build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .next -exec rm -rf {} +
	find . -type d -name node_modules -exec rm -rf {} +
	rm -rf backend/data/*.db
