# Nigerian Construction AI - ML Project

## Project Description

A machine learning application that predicts construction project delays and material requirements specifically for Nigeria's real estate sector. The system accounts for local factors including:

- Rainy season impacts on construction timelines
- State-specific challenges (Lagos traffic, remote area logistics, etc.)
- Economic conditions and budget constraints
- Contractor and project manager experience levels
- Building specifications and quality requirements

## Features

### 1. Delay Prediction
Predicts expected delays in construction projects based on:
- Project specifications (area, floors, building type)
- Location factors (state, area type)
- Timeline factors (start season, planned duration)
- Budget and experience levels
- Construction details (foundation, roof, finishing)

### 2. Material Requirements
Estimates quantities needed for:
- Cement (bags)
- Sand (tons)
- Granite (tons)
- Blocks (units)
- Steel (kg)

## Technology Stack

- **Machine Learning**: scikit-learn (Random Forest, Gradient Boosting)
- **Backend API**: FastAPI with RESTful endpoints
- **Frontend UI**: Streamlit for interactive predictions
- **Containerization**: Docker and Docker Compose
- **Data Processing**: Pandas, NumPy

## Project Structure

```
Nigerian-construction_ai---ML-project/
├── api/                    # FastAPI backend
│   ├── main.py
│   └── requirements.txt
├── streamlit_app/          # Streamlit frontend
│   ├── app.py
│   └── requirements.txt
├── src/                    # Model training code
│   ├── data_generator.py
│   └── train_models.py
├── models/                 # Trained ML models (generated)
├── Dockerfile.train        # Docker image for training
├── Dockerfile.api          # Docker image for API
├── Dockerfile.streamlit    # Docker image for UI
├── docker-compose.yml      # Orchestration config
├── setup.sh               # Quick start script
├── DEPLOYMENT.md          # Deployment instructions
└── README.md              # Project readme
```

## Models

### Delay Prediction Model
- **Algorithm**: Gradient Boosting Regressor
- **Features**: 14 input features including location, specifications, and experience
- **Output**: Predicted delay in days
- **Training Data**: 2000 synthetic projects based on Nigerian construction patterns

### Material Prediction Models
- **Algorithm**: Random Forest Regressor (5 separate models)
- **Features**: 7 input features related to building specifications
- **Outputs**:
  - Cement bags
  - Sand tons
  - Granite tons
  - Blocks quantity
  - Steel kg

## Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd Nigerian-construction_ai---ML-project
```

2. **Run the application**
```bash
chmod +x setup.sh
./setup.sh
```

3. **Access the services**
- Streamlit UI: http://localhost:8501
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## API Endpoints

### GET /options
Returns all available options for dropdown selections

### POST /predict-delay
Predicts construction delay based on project parameters

### POST /predict-materials
Predicts material requirements for construction

### GET /health
Health check endpoint

## Use Cases

1. **Project Planning**: Help contractors estimate realistic timelines
2. **Budgeting**: Accurate material quantity estimation for costing
3. **Risk Assessment**: Identify high-risk projects early
4. **Resource Allocation**: Plan material procurement efficiently
5. **Stakeholder Communication**: Data-driven timeline expectations

## Nigerian Context Factors

The models specifically account for:
- **Rainy Season**: April-October typically adds 30+ days delay
- **Lagos Factor**: Traffic and logistics add ~20 days
- **Remote Areas**: Limited access adds ~40 days
- **Contractor Experience**: Junior contractors may add 25+ days
- **Luxury Finishes**: Premium quality adds ~15 days

## Future Enhancements

1. Integration with real construction data from Nigerian projects
2. Cost prediction models accounting for Naira inflation
3. Weather API integration for real-time season predictions
4. Historical project database with actual outcomes
5. Multi-language support (English, Yoruba, Hausa, Igbo)
6. Mobile application for on-site access
7. Integration with construction management tools

## Development

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Train models:
```bash
cd src
python train_models.py
```

3. Run API:
```bash
cd api
uvicorn main:app --reload
```

4. Run Streamlit:
```bash
cd streamlit_app
streamlit run app.py
```

### Docker Development

```bash
docker-compose up --build
```

## Contributing

Contributions are welcome! Areas for improvement:
- Integration with real Nigerian construction datasets
- Additional ML models for cost prediction
- UI/UX enhancements
- Performance optimizations
- Documentation improvements

## License

MIT License - See LICENSE file for details

## Contact

For questions or collaboration opportunities, please open an issue on GitHub.

## Acknowledgments

This project addresses real challenges in Nigeria's construction sector using machine learning to improve project planning and resource management.
