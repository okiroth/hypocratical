import csv
import json

from flask import Flask, jsonify, render_template, request

from hip_agent import HIPAgent

app = Flask(__name__)
app.json.sort_keys = False  # type: ignore


@app.route("/", methods=["GET"])
def home():
    with open("testbench.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        data = list(reader)

        aux = []
        for row in data:
            aux.append(
                {
                    "id": row[0],
                    "question": row[1],
                    "options": row[2:],
                    "json": json.dumps({"question": row[1], "options": row[2:]}),
                }
            )

    return render_template("home.html", data=aux)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    options = data.get("options")

    if question is None or options is None:
        return jsonify({"error": "question and options are required"}), 400

    agent = HIPAgent()
    response = agent.get_response(question, options, explain=False)

    return jsonify(response)


@app.route("/ask-why", methods=["POST"])
def ask_why():
    data = request.get_json()
    question = data.get("question")
    options = data.get("options") or []

    if question is None or options is None:
        return jsonify({"error": "question and options are required"}), 400

    agent = HIPAgent()
    response = agent.get_response(question, options, explain=True)

    return jsonify(response)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
