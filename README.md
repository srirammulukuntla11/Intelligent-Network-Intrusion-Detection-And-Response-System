# 🛡️ Intelligent Network Intrusion Detection and Response System

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.28.0-red)

An intelligent network intrusion detection and response system designed to monitor, detect, and respond to potential threats in real-time. This project leverages advanced machine learning techniques and provides a user-friendly interface for network administrators to analyze and mitigate security threats effectively.

---

## 📋 Table of Contents

1. [Features](#-features)
2. [Quick Start](#-quick-start)
3. [Project Structure](#-project-structure)
4. [Technologies Used](#-technologies-used)
5. [Dataset](#-dataset)
6. [Contributing](#-contributing)
7. [License](#-license)

---

## ✨ Features

- 🔍 **Real-time Detection**: Instant classification of network connections.
- 🤖 **ML-Powered**: Utilizes Random Forest and XGBoost algorithms for accurate predictions.
- 📊 **Attack Types**: Detects various attack types, including DoS, Probe, R2L, and U2R.
- 📈 **Analytics Dashboard**: Provides visualizations and history tracking for better insights.
- 🎯 **Confidence Scores**: Offers probability-based predictions for better decision-making.
- 📁 **Batch Processing**: Allows uploading multiple connections for analysis.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/srirammulukuntla11/Intelligent-Network-Intrusion-Detection-And-Response-System.git
   cd Intelligent-Network-Intrusion-Detection-And-Response-System
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

---

## 📂 Project Structure

```
network-sentinel/
│
├── app.py                # Main application file
├── dashboard.py          # Dashboard logic
├── train_model.py        # Model training script
├── setup.sh              # Setup script
├── config/
│   └── config.yaml       # Configuration file
├── datasets/             # Dataset files and scripts
│   ├── KDDTrain+.txt
│   ├── KDDTest+.txt
│   └── download_data.py
├── models/               # Model-related files
│   ├── __init__.py
│   ├── feature_importance.csv
│   └── model_loader.py
├── static/               # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css
│   ├── images/
│   └── js/
├── templates/            # HTML templates
│   ├── about.html
│   ├── contact.html
│   ├── dashboard.html
│   ├── home.html
│   └── visualization.html
├── utils/                # Utility scripts
│   ├── __init__.py
│   ├── data_preprocessing.py
│   ├── feature_engineering.py
│   ├── model_utils.py
│   └── visualizations.py
└── README.md             # Project documentation
```

---

## 🛠️ Technologies Used

- **Python**: Core programming language.
- **Streamlit**: For building the interactive web application.
- **Machine Learning**: Random Forest and XGBoost for intrusion detection.
- **NSL-KDD Dataset**: Dataset used for training and testing the model.
- **HTML/CSS/JavaScript**: For creating the web interface.

---

## 📊 Dataset

The project uses the **NSL-KDD dataset**, a refined version of the KDD Cup 1999 dataset, which is widely used for evaluating intrusion detection systems. The dataset includes labeled network traffic data for training and testing the machine learning models.

- **KDDTrain+.txt**: Training dataset.
- **KDDTest+.txt**: Testing dataset.

For more details, visit the [NSL-KDD dataset page](https://www.unb.ca/cic/datasets/nsl.html).

---

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a Pull Request.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
