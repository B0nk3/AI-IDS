import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)
import glob
import time
import os
import json


model = joblib.load("models/random_forest.pkl")

if model:
    print("Model loaded")


def evaluare():

    dft = []
    gl = glob.glob("data/MachineLearningCVE/*.csv")
    for file in gl:
        f = pd.read_csv(file)
        dft.append(f)

    df = pd.concat(dft, ignore_index=True)
    df.columns = df.columns.str.strip()

    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    df.drop(
    df[df["Label"].isin([
        "Heartbleed",
        "Web Attack � Sql Injection",
        "Infiltration"
    ])].index,
    inplace=True
    )

    x = df.drop("Label", axis=1)
    y = df["Label"]
    x = x[model.feature_names_in_]

    print(x.shape)
    print(y.shape)

    y = y.map({
        "BENIGN":0, "DoS Hulk":1, "DDoS":2, "PortScan":3, "DoS GoldenEye":4,
        "FTP-Patator":5,"DoS slowloris":6, "DoS Slowhttptest":7, "SSH-Patator":8,
        "Bot":9, "Web Attack � Brute Force":10,"Web Attack � XSS":11
    })

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        random_state=16,
        stratify=y,
        test_size=0.2
    )

    begining = time.time()
    predictions = model.predict(x_test)
    ending = time.time()
    latency = ending - begining


    total_latency = latency * 1000
    average_latency = (latency / len(x_test)) * 1000



    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(
                        y_test,
                        predictions,
                        average="weighted",
                        zero_division=0
                        )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )
    clasification = classification_report(y_test, predictions)
    f1 = f1_score(
        y_test,
        predictions,
        average="weighted"
        )
    
    #false positive rate
    cm = confusion_matrix(y_test, predictions)
    tn = cm[0,0]
    fp = cm[0,1:].sum()
    fpr = fp / (fp + tn)

    results = {
            "accuracy": round(accuracy * 100, 2),
            "precision": round(precision * 100, 2),
            "f1": round(f1 * 100, 2),
            "recall": round(recall * 100, 2),
            "fpr": round(fpr * 100, 2),
            "total_latency": round(total_latency, 2),
            "average_latency": round(average_latency,2)
        }
    folder_eval = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    file_eval = os.path.join(folder_eval, "evaluation.json")

    with open(file_eval, "w", encoding="UTF-8") as f:
        json.dump(
            results,
            f
        )
    return results

if __name__ == "__main__":
    evaluare()