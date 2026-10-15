import joblib
import pandas as pd
import numpy as np
from datetime import datetime
import os
import csv

model = joblib.load("models/random_forest.pkl")

def detect(path):

    x = pd.read_csv(path)
    x.columns = x.columns.str.strip()

    x.replace([np.inf, -np.inf], np.nan, inplace=True)
    x.dropna(inplace=True)
    if "Label" in x.columns:
        x.drop("Label", axis=1, inplace=True)

    x = x[model.feature_names_in_]
    predictions = model.predict(x).tolist()


    benign_traffic = predictions.count(0)
    malicious_traffic = len(predictions) - benign_traffic

    if malicious_traffic > 0:
        print("Malicious traffic detected")
    else:
        print("No malicious traffic detected")

    attacks = {
    "benign": predictions.count(0),
    "dos_hulk": predictions.count(1),
    "ddos": predictions.count(2),
    "portscan": predictions.count(3),
    "dos_goldeneye": predictions.count(4),
    "ftp_patator": predictions.count(5),
    "dos_slowloris": predictions.count(6),
    "dos_slowhttptest": predictions.count(7),
    "ssh_patator": predictions.count(8),
    "bot": predictions.count(9),
    "web_brute_force": predictions.count(10),
    "web_xss": predictions.count(11)
}
    
    severities = {
    "dos_hulk": "HIGH",
    "ddos": "HIGH",
    "portscan": "MEDIUM",
    "dos_goldeneye": "HIGH",
    "ftp_patator": "HIGH",
    "dos_slowloris": "MEDIUM",
    "dos_slowhttptest": "MEDIUM",
    "ssh_patator": "HIGH",
    "bot": "HIGH",
    "web_brute_force": "HIGH",
    "web_xss": "HIGH"
}

    alerts = []
    for type, nr in attacks.items():

        if type == "benign":
            continue
        if nr > 0:
            alerts.append({
                "type": type,
                "severity": severities[type],
                "number":nr
            })

    folder_logs = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")

    fisier_log = os.path.join(folder_logs, "alerts.csv")


    with open(fisier_log, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if fisier_log and os.stat(fisier_log).st_size == 0:
            writer.writerow([
                "date_time",
                "type",
                "severity",
                "detections"
            ])

            for alert in alerts:
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    alert["type"],
                    alert["severity"],
                    alert["number"]
                ])
        if fisier_log and os.stat(fisier_log).st_size != 0:
            for alert in alerts:
                    writer.writerow([
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        alert["type"],
                        alert["severity"],
                        alert["number"]
                    ])

    return {
        "total_traffic": len(predictions),
        "benign_traffic": predictions.count(0),
        "malicious_traffic": malicious_traffic,
        "attacks": attacks,
        "alerts": alerts
    }


