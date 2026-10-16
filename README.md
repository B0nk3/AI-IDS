# AI-Powered Intrusion Detection System (AI-IDS)

A machine learning-based Intrusion Detection System (IDS) that analyzes network traffic and identifies potentially malicious activity using a Random Forest classifier trained on the CICIDS2017 dataset.

## Overview

AI-IDS is a Python application designed to detect and classify network traffic into benign traffic and several attack categories. It provides a web interface built with Flask, allowing users to upload network traffic CSV files and review detection results, generated alerts, and model evaluation metrics.

## Features

- **Machine Learning Detection:** Uses a trained Random Forest classifier to analyze network traffic.
- **Multi-Class Classification:** Identifies benign traffic and multiple types of network attacks.
- **CSV Upload:** Allows users to upload network traffic datasets through a web interface.
- **Attack Classification:** Supports categories such as DDoS, DoS Hulk, PortScan, FTP-Patator, SSH-Patator, Bot, and web attacks.
- **Alert Generation:** Generates alerts for detected attack categories and assigns severity levels.
- **Alert Logging:** Stores detection alerts in a CSV file.
- **Model Evaluation:** Reports accuracy, precision, recall, F1-score, false positive rate, and prediction latency.
- **Web Dashboard:** Displays detection results, alert history, and evaluation metrics.

## Technologies

- Python
- Flask
- Pandas
- NumPy
- Scikit-learn
- Joblib
- HTML, CSS, JavaScript
- Chart.js
- CICIDS2017 dataset

## Project Structure

```text
AI-IDS/
├── data/
│   └── MachineLearningCVE/
├── logs/
│   ├── alerts.csv
│   └── evaluation.json
├── models/
│   └── random_forest.pkl
├── src/
│   ├── app.py
│   ├── detection.py
│   ├── evaluation.py
│   └── templates/
│       └── index.html
├── .gitignore
└── README.md
```

The dataset and trained model are excluded from Git because of their large file sizes.

## Requirements

- Python 3.10 or newer recommended
- pip
- A trained Random Forest model saved as `models/random_forest.pkl`
- CICIDS2017 CSV files for model evaluation and training data access

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/B0nk3/AI-IDS.git
cd AI-IDS
```

### 2. Create a virtual environment

On Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install flask pandas numpy scikit-learn joblib
```

If additional libraries are imported by the project, install them as needed.

### 4. Add the required files

The dataset and trained model are not included in this repository.

Place the CICIDS2017 CSV files in:

```text
data/MachineLearningCVE/
```

Place the trained model in:

```text
models/random_forest.pkl
```

The model must be compatible with the feature columns expected by `detection.py`.

## Running the Application

From the project root, run:

```bash
python src/app.py
```

Open the local address displayed by Flask in your browser, usually:

```text
http://127.0.0.1:5000/
```

Upload a compatible network traffic CSV file to run detection and view the results.

## Model Evaluation

The evaluation module calculates several classification metrics:

| Metric | Description |
|---|---|
| Accuracy | Percentage of correct predictions |
| Precision | Proportion of predicted positive classes that are correct, according to the selected averaging method |
| Recall | Proportion of actual classes correctly identified |
| F1-score | Harmonic mean of precision and recall |
| False Positive Rate | Proportion of benign samples incorrectly classified as attacks, according to the implemented calculation |
| Total Latency | Time required to predict the evaluation dataset |
| Average Latency | Average prediction time per sample |

Evaluation results are saved to `logs/evaluation.json`.

Run the evaluation module from the project root:

```bash
python src/evaluation.py
```

## Alert Logging

Detected attack categories generate alerts with a severity level and detection count. Alerts are stored in:

```text
logs/alerts.csv
```

The dashboard can display previously recorded alerts alongside new detection results.

## Supported Attack Categories

The classifier is configured for the following classes:

- Benign
- DoS Hulk
- DDoS
- PortScan
- DoS GoldenEye
- FTP-Patator
- DoS slowloris
- DoS Slowhttptest
- SSH-Patator
- Bot
- Web Attack – Brute Force
- Web Attack – XSS

Detection results depend on the trained model, input data quality, and the compatibility of the CSV feature columns.

## Limitations

- The application analyzes CSV exports of network traffic rather than directly capturing live network packets.
- Detection quality depends on the training dataset and the trained model.
- The model and dataset must be obtained separately.
- Predictions are intended for research and educational purposes and should not be treated as a replacement for a production-grade security monitoring system.

## Future Improvements

- Real-time network traffic integration
- Threat intelligence feed integration
- Improved alert prioritization
- Periodic model retraining
- Expanded testing on unseen network traffic
- More detailed detection and performance reports

## License

No license has been specified yet. Add a license if you intend to permit others to reuse, modify, or distribute this project.
