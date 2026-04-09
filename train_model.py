#!/usr/bin/env python3
"""
Network Intrusion Detection System - Model Training Script
This script downloads NSL-KDD dataset and trains the ML model
"""

import os
import requests
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Import our modules
from utils.data_preprocessing import DataPreprocessor
from utils.model_utils import ModelManager

def download_dataset(url, filename):
    """Download dataset from URL"""
    print(f"Downloading {filename}...")
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {filename}")

def main():
    print("=" * 60)
    print("NETWORK INTRUSION DETECTION SYSTEM - MODEL TRAINING")
    print("=" * 60)
    
    # Create directories
    os.makedirs('models', exist_ok=True)
    os.makedirs('datasets', exist_ok=True)
    
    # Dataset URLs
    train_url = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain%2B.txt"
    test_url = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest%2B.txt"
    
    train_path = "datasets/KDDTrain+.txt"
    test_path = "datasets/KDDTest+.txt"
    
    # Download datasets if not exist
    if not os.path.exists(train_path):
        download_dataset(train_url, train_path)
    if not os.path.exists(test_path):
        download_dataset(test_url, test_path)
    
    print("\n📊 Loading and preprocessing data...")
    preprocessor = DataPreprocessor()
    
    # Load data
    train_df, test_df = preprocessor.load_and_preprocess_data(train_path, test_path)
    print(f"✓ Training samples: {len(train_df)}")
    print(f"✓ Test samples: {len(test_df)}")
    
    # Encode categorical features
    train_df, test_df = preprocessor.encode_categorical_features(train_df, test_df)
    print("✓ Categorical features encoded")
    
    # Encode attack labels
    train_df, test_df = preprocessor.encode_attack_labels(train_df, test_df)
    print("✓ Attack labels categorized")
    
    # Prepare features
    X_train, X_test, y_train, y_test = preprocessor.prepare_features(train_df, test_df)
    print("✓ Features prepared and scaled")
    
    # Save preprocessors
    preprocessor.save_preprocessors()
    print("✓ Preprocessors saved")
    
    print("\n🤖 Training Random Forest model...")
    model_manager = ModelManager()
    
    # Train model
    model_manager.train_random_forest(X_train, y_train)
    
    # Evaluate model
    print("\n📈 Evaluating model performance...")
    results = model_manager.evaluate_model(X_test, y_test)
    
    print(f"\n🎯 Model Accuracy: {results['accuracy']*100:.2f}%")
    print("\n📊 Classification Report:")
    print("-" * 40)
    
    # Print classification report
    for class_name, metrics in results['classification_report'].items():
        if class_name not in ['accuracy', 'macro avg', 'weighted avg']:
            if isinstance(metrics, dict):
                print(f"\n{class_name.upper()}:")
                print(f"  Precision: {metrics['precision']:.3f}")
                print(f"  Recall: {metrics['recall']:.3f}")
                print(f"  F1-Score: {metrics['f1-score']:.3f}")
    
    # Save model
    model_manager.save_model()
    print("\n✅ Model saved to 'models/nids_model.pkl'")
    
    # Save feature importance
    importance = model_manager.get_feature_importance()
    if importance is not None:
        feature_names = preprocessor.feature_names
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        feature_importance.to_csv('models/feature_importance.csv', index=False)
        print("✓ Feature importance saved")
    
    print("\n" + "=" * 60)
    print("✅ TRAINING COMPLETE! Ready to run the dashboard.")
    print("=" * 60)
    print("\nTo start the application, run:")
    print("  streamlit run app.py")

if __name__ == "__main__":
    main()