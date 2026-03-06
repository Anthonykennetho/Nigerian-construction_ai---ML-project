from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pickle
import numpy as np
from typing import Dict, Optional
import os

app = FastAPI(
    title="Nigerian Construction AI API",
    description="ML models for predicting construction delays and material requirements",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

delay_model_data = None
material_model_data = None

@app.on_event("startup")
def load_models():
    global delay_model_data, material_model_data

    try:
        with open('/app/models/delay_model.pkl', 'rb') as f:
            delay_model_data = pickle.load(f)

        with open('/app/models/material_models.pkl', 'rb') as f:
            material_model_data = pickle.load(f)

        print("Models loaded successfully!")
    except Exception as e:
        print(f"Error loading models: {e}")

class DelayPredictionInput(BaseModel):
    built_up_area_m2: float = Field(..., gt=0, description="Built-up area in square meters")
    plot_size_m2: float = Field(..., gt=0, description="Plot size in square meters")
    number_of_floors: int = Field(..., ge=1, le=10, description="Number of floors")
    planned_completion_days: int = Field(..., gt=0, description="Planned completion days")
    initial_budget_naira: float = Field(..., gt=0, description="Initial budget in Naira")
    project_manager_experience_years: float = Field(..., ge=0, description="PM experience in years")
    state: str = Field(..., description="State (Lagos, Abuja, Rivers, Oyo, Kano)")
    area_type: str = Field(..., description="Area type (Highbrow, Middle Class, Estate, Remote)")
    building_type: str = Field(..., description="Building type")
    foundation_type: str = Field(..., description="Foundation type")
    roof_type: str = Field(..., description="Roof type")
    finishing_quality: str = Field(..., description="Finishing quality")
    start_season: str = Field(..., description="Start season (Rainy or Dry)")
    contractor_experience: str = Field(..., description="Contractor experience")

class MaterialPredictionInput(BaseModel):
    built_up_area_m2: float = Field(..., gt=0, description="Built-up area in square meters")
    plot_size_m2: float = Field(..., gt=0, description="Plot size in square meters")
    number_of_floors: int = Field(..., ge=1, le=10, description="Number of floors")
    building_type: str = Field(..., description="Building type")
    foundation_type: str = Field(..., description="Foundation type")
    roof_type: str = Field(..., description="Roof type")
    finishing_quality: str = Field(..., description="Finishing quality")

@app.get("/")
def read_root():
    return {
        "message": "Nigerian Construction AI API",
        "endpoints": ["/predict-delay", "/predict-materials", "/health"]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "models_loaded": delay_model_data is not None and material_model_data is not None
    }

@app.post("/predict-delay")
def predict_delay(input_data: DelayPredictionInput):
    if delay_model_data is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        model = delay_model_data['model']
        encoders = delay_model_data['encoders']
        features = delay_model_data['features']

        feature_values = []
        for feat in features:
            if feat.endswith('_encoded'):
                col_name = feat.replace('_encoded', '')
                original_value = getattr(input_data, col_name)
                encoded_value = encoders[col_name].transform([original_value])[0]
                feature_values.append(encoded_value)
            else:
                feature_values.append(getattr(input_data, feat))

        X = np.array([feature_values])
        prediction = model.predict(X)[0]

        return {
            "predicted_delay_days": round(float(prediction), 2),
            "expected_completion_days": round(input_data.planned_completion_days + float(prediction), 2)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.post("/predict-materials")
def predict_materials(input_data: MaterialPredictionInput):
    if material_model_data is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        models = material_model_data['models']
        encoders = material_model_data['encoders']
        features = material_model_data['features']

        feature_values = []
        for feat in features:
            if feat.endswith('_encoded'):
                col_name = feat.replace('_encoded', '')
                original_value = getattr(input_data, col_name)
                encoded_value = encoders[col_name].transform([original_value])[0]
                feature_values.append(encoded_value)
            else:
                feature_values.append(getattr(input_data, feat))

        X = np.array([feature_values])

        predictions = {}
        for material_name, model in models.items():
            pred = model.predict(X)[0]
            predictions[material_name] = round(float(pred), 2)

        return {
            "material_predictions": predictions
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.get("/options")
def get_options():
    return {
        "states": ["Lagos", "Abuja", "Rivers", "Oyo", "Kano"],
        "area_types": ["Highbrow", "Middle Class", "Estate", "Remote"],
        "building_types": ["Bungalow", "Duplex", "Semi-Detached", "Terrace", "Mansion"],
        "foundation_types": ["Strip", "Raft", "Pile"],
        "roof_types": ["Wooden", "Concrete", "Metal"],
        "finishing_qualities": ["Basic", "Standard", "Luxury"],
        "seasons": ["Rainy", "Dry"],
        "contractor_experiences": ["Junior", "Mid", "Senior"]
    }
