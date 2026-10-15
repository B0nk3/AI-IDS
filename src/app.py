
from flask import Flask, request, render_template
from detection import detect as run_detection
import os
import csv
import json

app = Flask(__name__)

def read_history():
    history = []

    log_file = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "logs",
        "alerts.csv"
    )

    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            history = list(reader)

    return history


def read_evaluation():
    eval_file = os.path.join("logs", "evaluation.json")

    with open(eval_file, "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/")
def home():
    return render_template(
        "index.html",
        history=read_history(),
        results=read_evaluation()
    )


@app.route("/detect", methods=["POST"])
def detect():
    if "file" not in request.files:
        return "No file given"

    file = request.files["file"]

    if file.filename == "":
        return "No file selected"

    detection_result = run_detection(file)

    return render_template(
        "index.html",
        detection_result=detection_result,
        file_name=file.filename,
        history=read_history(),
        results=read_evaluation()
    )


if __name__ == "__main__":
    app.run()
