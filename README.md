# Nigerian Construction AI - ML Project

Machine learning models that predict construction project delays and material requirements specifically for Nigeria's real estate sector, accounting for local factors like rainy seasons, location challenges, and economic conditions.

## Features

- **Delay Prediction**: Predict project delays based on Nigerian construction factors
- **Material Estimation**: Estimate cement, sand, granite, blocks, and steel requirements
- **FastAPI Backend**: RESTful API for predictions
- **Streamlit UI**: User-friendly web interface
- **Dockerized**: Complete containerized deployment

## Quick Start

```bash
chmod +x setup.sh
./setup.sh
```

Then access:
- **Web UI**: http://localhost:8501
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Architecture

- **Training Service**: Trains ML models using synthetic Nigerian construction data
- **FastAPI Backend**: Serves predictions via REST API
- **Streamlit Frontend**: Interactive web interface for users

## Technology Stack

- Python 3.11
- scikit-learn (ML models)
- FastAPI (API backend)
- Streamlit (UI frontend)
- Docker & Docker Compose

## Documentation

- [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - Detailed project information
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment and API documentation

## Models

### Delay Prediction
Predicts construction delays considering:
- Location (state, area type)
- Rainy season impact
- Building specifications
- Contractor experience
- Budget constraints

### Material Requirements
Estimates quantities for:
- Cement (bags)
- Sand (tons)
- Granite (tons)
- Blocks (units)
- Steel (kg)

## Development

### Manual Setup

1. Train models:
```bash
docker-compose up train
```

2. Start services:
```bash
docker-compose up -d api streamlit
```

3. View logs:
```bash
docker-compose logs -f
```

4. Stop services:
```bash
docker-compose down
```

## API Example

```bash
curl -X POST http://localhost:8000/predict-delay \
  -H "Content-Type: application/json" \
  -d '{
    "built_up_area_m2": 200,
    "state": "Lagos",
    "building_type": "Duplex",
    "start_season": "Rainy"
  }'
```

## License

MIT License - See [LICENSE](LICENSE) file for details

## Contributing

Contributions welcome! This project aims to improve construction planning in Nigeria using machine learning.
