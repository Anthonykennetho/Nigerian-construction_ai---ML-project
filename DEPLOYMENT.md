# Nigerian Construction AI - Deployment Guide

## Overview

This application consists of three components:
1. **Model Training Service** - Trains ML models for delay and material predictions
2. **FastAPI Backend** - RESTful API for predictions
3. **Streamlit Frontend** - User-friendly web interface

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- At least 2GB of available RAM
- Ports 8000 and 8501 available

### One-Command Deployment

```bash
chmod +x setup.sh
./setup.sh
```

### Manual Deployment

1. **Train the models:**
```bash
docker-compose up train
```

2. **Start the services:**
```bash
docker-compose up -d api streamlit
```

3. **Access the application:**
- Streamlit UI: http://localhost:8501
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Architecture

```
┌─────────────────┐
│  Streamlit UI   │ :8501
│   (Frontend)    │
└────────┬────────┘
         │
         │ HTTP
         ▼
┌─────────────────┐
│   FastAPI       │ :8000
│   (Backend)     │
└────────┬────────┘
         │
         │ Loads
         ▼
┌─────────────────┐
│  ML Models      │
│  (.pkl files)   │
└─────────────────┘
```

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Predict Delay
```bash
curl -X POST http://localhost:8000/predict-delay \
  -H "Content-Type: application/json" \
  -d '{
    "built_up_area_m2": 200,
    "plot_size_m2": 400,
    "number_of_floors": 2,
    "planned_completion_days": 240,
    "initial_budget_naira": 20000000,
    "project_manager_experience_years": 5,
    "state": "Lagos",
    "area_type": "Middle Class",
    "building_type": "Duplex",
    "foundation_type": "Strip",
    "roof_type": "Concrete",
    "finishing_quality": "Standard",
    "start_season": "Rainy",
    "contractor_experience": "Mid"
  }'
```

### Predict Materials
```bash
curl -X POST http://localhost:8000/predict-materials \
  -H "Content-Type: application/json" \
  -d '{
    "built_up_area_m2": 200,
    "plot_size_m2": 400,
    "number_of_floors": 2,
    "building_type": "Duplex",
    "foundation_type": "Strip",
    "roof_type": "Concrete",
    "finishing_quality": "Standard"
  }'
```

## Managing the Application

### View Logs
```bash
docker-compose logs -f
docker-compose logs -f api
docker-compose logs -f streamlit
```

### Stop Services
```bash
docker-compose down
```

### Restart Services
```bash
docker-compose restart
```

### Rebuild After Code Changes
```bash
docker-compose down
docker-compose build
docker-compose up -d
```

## Retrain Models

To retrain models with updated data:

```bash
docker-compose up train
docker-compose restart api
```

## Production Considerations

1. **Environment Variables**: Create a `.env` file for sensitive configuration
2. **Reverse Proxy**: Use Nginx or Traefik for SSL and load balancing
3. **Monitoring**: Add logging and monitoring solutions
4. **Scaling**: Use Docker Swarm or Kubernetes for multi-instance deployment
5. **Database**: Consider adding PostgreSQL/Supabase for storing predictions
6. **Authentication**: Add user authentication for production use

## Troubleshooting

### Models Not Loading
```bash
docker-compose up train
docker-compose restart api
```

### Port Already in Use
Change ports in `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"  # API
  - "8502:8501"  # Streamlit
```

### Connection Refused
Ensure all services are running:
```bash
docker-compose ps
```

## File Structure

```
.
├── api/
│   ├── main.py              # FastAPI application
│   └── requirements.txt
├── streamlit_app/
│   ├── app.py              # Streamlit UI
│   └── requirements.txt
├── src/
│   ├── data_generator.py   # Synthetic data generation
│   └── train_models.py     # Model training
├── models/                 # Trained models (generated)
├── Dockerfile.train
├── Dockerfile.api
├── Dockerfile.streamlit
├── docker-compose.yml
└── setup.sh
```

## License

MIT License - See LICENSE file for details
