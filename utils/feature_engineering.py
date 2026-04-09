import pandas as pd
import numpy as np

class FeatureEngineer:
    @staticmethod
    def extract_features_from_input(input_data):
        """Extract features from user input for prediction"""
        features = []
        
        # Convert input data to correct format
        # This handles the 41 features in the correct order
        feature_order = [
            'duration', 'protocol_type', 'service', 'flag', 'src_bytes',
            'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
            'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
            'su_attempted', 'num_root', 'num_file_creations', 'num_shells',
            'num_access_files', 'num_outbound_cmds', 'is_host_login',
            'is_guest_login', 'count', 'srv_count', 'serror_rate',
            'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
            'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count',
            'dst_host_srv_count', 'dst_host_same_srv_rate',
            'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
            'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
            'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
            'dst_host_srv_rerror_rate'
        ]
        
        for feature in feature_order:
            if feature in input_data:
                features.append(input_data[feature])
            else:
                features.append(0)  # Default value if missing
                
        return np.array(features).reshape(1, -1)
    
    @staticmethod
    def calculate_risk_score(prediction, confidence):
        """Calculate risk score based on prediction and confidence"""
        risk_levels = {
            'normal': 0,
            'probe': 3,
            'dos': 4,
            'u2r': 5,
            'r2l': 5,
            'unknown': 2
        }
        
        base_risk = risk_levels.get(prediction, 2)
        adjusted_risk = base_risk * confidence
        
        return min(adjusted_risk, 5)  # Scale 0-5