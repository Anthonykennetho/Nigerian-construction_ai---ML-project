.PHONY: help setup train start stop restart logs clean build

help:
	@echo "Nigerian Construction AI - Makefile Commands"
	@echo ""
	@echo "  make setup       - Quick setup (train + start services)"
	@echo "  make train       - Train ML models"
	@echo "  make start       - Start API and Streamlit services"
	@echo "  make stop        - Stop all services"
	@echo "  make restart     - Restart all services"
	@echo "  make logs        - View logs from all services"
	@echo "  make build       - Rebuild Docker images"
	@echo "  make clean       - Stop services and remove containers"
	@echo ""
	@echo "Access points after setup:"
	@echo "  - Streamlit UI: http://localhost:8501"
	@echo "  - API: http://localhost:8000"
	@echo "  - API Docs: http://localhost:8000/docs"

setup:
	@echo "Training ML models..."
	docker-compose up train
	@echo "Starting services..."
	docker-compose up -d api streamlit
	@echo "Setup complete!"
	@echo "Streamlit UI: http://localhost:8501"
	@echo "API: http://localhost:8000"

train:
	docker-compose up train

start:
	docker-compose up -d api streamlit

stop:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

build:
	docker-compose build

clean:
	docker-compose down -v
	rm -rf models/*.pkl
