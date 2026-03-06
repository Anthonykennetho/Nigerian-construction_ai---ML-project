import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_nigerian_construction_data(n_projects=1000, seed=101):
    np.random.seed(seed)
    random.seed(seed)

    data = {
        'project_id': [f'PRJ_{i:04d}' for i in range(n_projects)],
        'project_name': [f'House_{random.choice(["Bungalow", "Duplex", "Terrace"])}_{i}' for i in range(n_projects)],

        'state': np.random.choice(['Lagos', 'Abuja', 'Rivers', 'Oyo', 'Kano'],
                                  n_projects, p=[0.4, 0.25, 0.15, 0.1, 0.1]),
        'area_type': np.random.choice(['Highbrow', 'Middle Class', 'Estate', 'Remote'],
                                      n_projects, p=[0.2, 0.5, 0.25, 0.05]),

        'built_up_area_m2': np.random.uniform(80, 600, n_projects).round(0),
        'plot_size_m2': np.random.uniform(150, 1200, n_projects).round(0),
        'number_of_floors': np.random.choice([1, 2, 3, 4], n_projects, p=[0.4, 0.45, 0.1, 0.05]),
        'building_type': np.random.choice(['Bungalow', 'Duplex', 'Semi-Detached', 'Terrace', 'Mansion'],
                                          n_projects, p=[0.4, 0.3, 0.15, 0.1, 0.05]),
        'foundation_type': np.random.choice(['Strip', 'Raft', 'Pile'], n_projects, p=[0.7, 0.25, 0.05]),
        'roof_type': np.random.choice(['Wooden', 'Concrete', 'Metal'], n_projects, p=[0.3, 0.6, 0.1]),
        'finishing_quality': np.random.choice(['Basic', 'Standard', 'Luxury'], n_projects, p=[0.3, 0.5, 0.2]),

        'planned_start_date': [datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1460))
                               for _ in range(n_projects)],
        'planned_completion_days': np.random.choice([180, 240, 300, 360, 540], n_projects, p=[0.2, 0.3, 0.25, 0.15, 0.1]),

        'contractor_experience': np.random.choice(['Junior', 'Mid', 'Senior'], n_projects, p=[0.3, 0.5, 0.2]),
        'initial_budget_naira': np.random.uniform(5_000_000, 150_000_000, n_projects).round(0),
        'project_manager_experience_years': np.random.uniform(2, 20, n_projects).round(0),
    }

    df = pd.DataFrame(data)

    df['start_season'] = df['planned_start_date'].apply(
        lambda x: 'Rainy' if x.month in [4, 5, 6, 7, 8, 9, 10] else 'Dry'
    )

    delay_base = np.random.uniform(0, 50, n_projects)
    delay_base += np.where(df['start_season'] == 'Rainy', 30, 0)
    delay_base += np.where(df['state'] == 'Lagos', 20, 0)
    delay_base += np.where(df['area_type'] == 'Remote', 40, 0)
    delay_base += np.where(df['contractor_experience'] == 'Junior', 25, 0)
    delay_base += np.where(df['finishing_quality'] == 'Luxury', 15, 0)

    df['actual_delay_days'] = delay_base.round(0)
    df['actual_completion_days'] = df['planned_completion_days'] + df['actual_delay_days']

    cement_per_m2 = np.random.uniform(2.5, 4.5, n_projects)
    df['cement_bags'] = (df['built_up_area_m2'] * cement_per_m2 * df['number_of_floors']).round(0)

    sand_per_m2 = np.random.uniform(0.25, 0.45, n_projects)
    df['sand_tons'] = (df['built_up_area_m2'] * sand_per_m2 * df['number_of_floors']).round(1)

    granite_per_m2 = np.random.uniform(0.3, 0.5, n_projects)
    df['granite_tons'] = (df['built_up_area_m2'] * granite_per_m2 * df['number_of_floors']).round(1)

    blocks_per_m2 = np.random.uniform(10, 15, n_projects)
    df['blocks_quantity'] = (df['built_up_area_m2'] * blocks_per_m2).round(0)

    steel_per_m2 = np.random.uniform(15, 30, n_projects)
    df['steel_kg'] = (df['built_up_area_m2'] * steel_per_m2 * df['number_of_floors']).round(0)

    return df
