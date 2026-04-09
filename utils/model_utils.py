import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import xgboost as xgb
import numpy as np

class ModelManager:
    def __init__(self):
        self.model = None
        self.model_path = 'models/nids_model.pkl'
        
    def train_random_forest(self, X_train, y_train):
        """Train Random Forest classifier"""
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        return self.model
    
    def train_xgboost(self, X_train, y_train):
        """Train XGBoost classifier"""
        self.model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            use_label_encoder=False,
            eval_metric='mlogloss'
        )
        self.model.fit(X_train, y_train)
        return self.model
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate model performance"""
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Get class names
        class_names = self.model.classes_
        
        # Generate classification report
        report = classification_report(y_test, y_pred, output_dict=True)
        
        # Generate confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        return {
            'accuracy': accuracy,
            'classification_report': report,
            'confusion_matrix': cm,
            'class_names': class_names
        }
    
    def predict_with_confidence(self, features):
        """Make prediction with confidence scores"""
        if self.model is None:
            self.load_model()
            
        # Get prediction probabilities
        probabilities = self.model.predict_proba(features)[0]
        prediction = self.model.predict(features)[0]
        
        # Get confidence for the predicted class
        class_index = list(self.model.classes_).index(prediction)
        confidence = probabilities[class_index]
        
        # Get top 3 predictions
        top_3_indices = np.argsort(probabilities)[-3:][::-1]
        top_3_predictions = [
            {
                'class': self.model.classes_[i],
                'confidence': probabilities[i]
            }
            for i in top_3_indices
        ]
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'top_3': top_3_predictions,
            'all_probabilities': dict(zip(self.model.classes_, probabilities))
        }
    
    def save_model(self, path=None):
        """Save trained model"""
        if path is None:
            path = self.model_path
            
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.model, path)
        
    def load_model(self, path=None):
        """Load trained model"""
        if path is None:
            path = self.model_path
            
        if os.path.exists(path):
            self.model = joblib.load(path)
            return True
        return False
    
    def get_feature_importance(self):
        """Get feature importance if available"""
        if hasattr(self.model, 'feature_importances_'):
            return self.model.feature_importances_
        return None