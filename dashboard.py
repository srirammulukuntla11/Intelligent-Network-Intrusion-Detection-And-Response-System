from flask import Flask, render_template, request, jsonify
from utils.data_preprocessing import DataPreprocessor
from utils.model_utils import ModelManager
from utils.visualizations import Visualizer

app = Flask(__name__)

# Initialize the DataPreprocessor
preprocessor = DataPreprocessor()

# Initialize the ModelManager
model_manager = ModelManager()

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for the dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for the contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for data preprocessing
@app.route('/preprocess', methods=['POST'])
def preprocess():
    data = request.json
    train_path = data.get('train_path')
    test_path = data.get('test_path')
    train_df, test_df = preprocessor.load_and_preprocess_data(train_path, test_path)
    return jsonify({"message": "Data preprocessed successfully"})

# Route for model training
@app.route('/train', methods=['POST'])
def train():
    data = request.json
    X_train = data.get('X_train')
    y_train = data.get('y_train')
    model = model_manager.train_random_forest(X_train, y_train)
    return jsonify({"message": "Model trained successfully"})

# Route for generating visualizations
@app.route('/visualize', methods=['GET'])
def visualize():
    # Example data for visualization
    data = {"normal": 50, "attack": 50}
    visualization = Visualizer.create_attack_distribution_chart(data)
    return render_template('visualization.html', visualization=visualization.to_html(full_html=False))

if __name__ == '__main__':
    app.run(debug=True)