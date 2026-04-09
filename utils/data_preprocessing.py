import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import os

class DataPreprocessor:
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_names = None
        
    def load_and_preprocess_data(self, train_path, test_path):
        """Load and preprocess NSL-KDD dataset"""
        # Column names from NSL-KDD dataset
        columns = [
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
            'dst_host_srv_rerror_rate', 'attack', 'difficulty'
        ]
        
        # Load datasets
        train_df = pd.read_csv(train_path, names=columns)
        test_df = pd.read_csv(test_path, names=columns)
        
        # Remove difficulty column
        train_df = train_df.drop('difficulty', axis=1)
        test_df = test_df.drop('difficulty', axis=1)
        
        return train_df, test_df
    
    def encode_categorical_features(self, train_df, test_df):
        """Encode categorical features"""
        categorical_cols = ['protocol_type', 'service', 'flag']
        
        for col in categorical_cols:
            self.label_encoders[col] = LabelEncoder()
            # Combine train and test for consistent encoding
            combined = pd.concat([train_df[col], test_df[col]], axis=0)
            self.label_encoders[col].fit(combined)
            
            train_df[col] = self.label_encoders[col].transform(train_df[col])
            test_df[col] = self.label_encoders[col].transform(test_df[col])
            
        return train_df, test_df
    
    def encode_attack_labels(self, train_df, test_df):
        """Convert attack names to categories"""
        attack_categories = {
            'normal': 'normal',
            'back': 'dos', 'land': 'dos', 'neptune': 'dos', 'pod': 'dos',
            'smurf': 'dos', 'teardrop': 'dos', 'apache2': 'dos',
            'udpstorm': 'dos', 'processtable': 'dos', 'worm': 'dos',
            'satan': 'probe', 'ipsweep': 'probe', 'nmap': 'probe',
            'portsweep': 'probe', 'mscan': 'probe', 'saint': 'probe',
            'guess_passwd': 'r2l', 'ftp_write': 'r2l', 'imap': 'r2l',
            'phf': 'r2l', 'multihop': 'r2l', 'warezmaster': 'r2l',
            'warezclient': 'r2l', 'spy': 'r2l', 'xlock': 'r2l',
            'xsnoop': 'r2l', 'snmpguess': 'r2l', 'snmpgetattack': 'r2l',
            'httptunnel': 'r2l', 'sendmail': 'r2l', 'named': 'r2l',
            'buffer_overflow': 'u2r', 'loadmodule': 'u2r', 'rootkit': 'u2r',
            'perl': 'u2r', 'sqlattack': 'u2r', 'xterm': 'u2r', 'ps': 'u2r'
        }
        
        train_df['attack_category'] = train_df['attack'].map(attack_categories)
        test_df['attack_category'] = test_df['attack'].map(attack_categories)
        
        # Fill any missing with 'unknown'
        train_df['attack_category'].fillna('unknown', inplace=True)
        test_df['attack_category'].fillna('unknown', inplace=True)
        
        return train_df, test_df
    
    def prepare_features(self, train_df, test_df):
        """Prepare features for model training"""
        # Separate features and labels
        feature_cols = [col for col in train_df.columns if col not in ['attack', 'attack_category']]
        
        X_train = train_df[feature_cols]
        y_train = train_df['attack_category']
        
        X_test = test_df[feature_cols]
        y_test = test_df['attack_category']
        
        # Scale numerical features
        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)
        
        self.feature_names = feature_cols
        
        return X_train, X_test, y_train, y_test
    
    def save_preprocessors(self, path='models/'):
        """Save label encoders and scaler"""
        os.makedirs(path, exist_ok=True)
        joblib.dump(self.label_encoders, f'{path}/label_encoders.pkl')
        joblib.dump(self.scaler, f'{path}/scaler.pkl')
        
    def load_preprocessors(self, path='models/'):
        """Load label encoders and scaler"""
        self.label_encoders = joblib.load(f'{path}/label_encoders.pkl')
        self.scaler = joblib.load(f'{path}/scaler.pkl')