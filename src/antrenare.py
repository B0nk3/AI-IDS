import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import glob
import joblib


#in variabila dataframes vom incarca toate datele din fisiere
dataframes = []
#lista cu fisiere csv
files = glob.glob("data/MachineLearningCVE/*.csv")

#se ia continutul fiecarui fisier si este adaugat in dataframes
for file in files:
    df_temporar = pd.read_csv(file)
    df_temporar.columns = df_temporar.columns.str.strip()
    dataframes.append(df_temporar)

#variabila cu care vom lucra
df = pd.concat(dataframes, ignore_index=True)

print(df["Label"].value_counts())

#sterge duplicate
df = df.drop_duplicates()
#sterge valori +/- inf
df.replace([np.inf, -np.inf], np.nan, inplace=True)
#sterge valori nule
df.dropna(inplace=True)

df.drop(
    df[df["Label"].isin([
        "Heartbleed",
        "Web Attack � Sql Injection",
        "Infiltration"
    ])].index,
    inplace=True
)

print(df["Label"].value_counts())

x = df.drop("Label", axis=1)
y = df["Label"]



y = y.map({"BENIGN":0, "DoS Hulk":1, "DDoS":2, "PortScan":3, "DoS GoldenEye":4,
           "FTP-Patator":5,"DoS slowloris":6, "DoS Slowhttptest":7, "SSH-Patator":8,
           "Bot":9, "Web Attack � Brute Force":10,"Web Attack � XSS":11})


print(x.shape)
print(y.shape)



x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=14,
    n_jobs=-1
)

model.fit(x_train, y_train)

joblib.dump(model, "models/random_forest.pkl")
print("Model antrenat")

y_pred = model.predict(x_test)

print("accuracy", accuracy_score(y_test, y_pred))
print("classification", classification_report(y_test, y_pred))
print("confusion matrix", confusion_matrix(y_test, y_pred))