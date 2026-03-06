import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import os
from data_generator import generate_nigerian_construction_data

def prepare_features(df):
    df_encoded = df.copy()

    label_encoders = {}
    categorical_cols = ['state', 'area_type', 'building_type', 'foundation_type',
                       'roof_type', 'finishing_quality', 'start_season', 'contractor_experience']

    for col in categorical_cols:
        le = LabelEncoder()
        df_encoded[col + '_encoded'] = le.fit_transform(df_encoded[col])
        label_encoders[col] = le

    return df_encoded, label_encoders

def train_delay_model(df):
    df_encoded, label_encoders = prepare_features(df)

    feature_cols = ['built_up_area_m2', 'plot_size_m2', 'number_of_floors',
                   'planned_completion_days', 'initial_budget_naira',
                   'project_manager_experience_years',
                   'state_encoded', 'area_type_encoded', 'building_type_encoded',
                   'foundation_type_encoded', 'roof_type_encoded',
                   'finishing_quality_encoded', 'start_season_encoded',
                   'contractor_experience_encoded']

    X = df_encoded[feature_cols]
    y = df_encoded['actual_delay_days']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GradientBoostingRegressor(n_estimators=150, learning_rate=0.1,
                                      max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Delay Model - MAE: {mae:.2f} days, R2: {r2:.3f}")

    return model, label_encoders, feature_cols

def train_material_models(df):
    df_encoded, label_encoders = prepare_features(df)

    feature_cols = ['built_up_area_m2', 'plot_size_m2', 'number_of_floors',
                   'building_type_encoded', 'foundation_type_encoded',
                   'roof_type_encoded', 'finishing_quality_encoded']

    X = df_encoded[feature_cols]

    material_targets = ['cement_bags', 'sand_tons', 'granite_tons', 'blocks_quantity', 'steel_kg']
    material_models = {}

    for target in material_targets:
        y = df_encoded[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"{target} Model - MAE: {mae:.2f}, R2: {r2:.3f}")

        material_models[target] = model

    return material_models, label_encoders, feature_cols

def save_models():
    os.makedirs('models', exist_ok=True)

    print("Generating training data...")
    df = generate_nigerian_construction_data(n_projects=2000, seed=101)

    print("\nTraining Delay Prediction Model...")
    delay_model, delay_encoders, delay_features = train_delay_model(df)

    with open('models/delay_model.pkl', 'wb') as f:
        pickle.dump({
            'model': delay_model,
            'encoders': delay_encoders,
            'features': delay_features
        }, f)

    print("\nTraining Material Prediction Models...")
    material_models, material_encoders, material_features = train_material_models(df)

    with open('models/material_models.pkl', 'wb') as f:
        pickle.dump({
            'models': material_models,
            'encoders': material_encoders,
            'features': material_features
        }, f)

    print("\nModels saved successfully!")

if __name__ == "__main__":
    save_models()
