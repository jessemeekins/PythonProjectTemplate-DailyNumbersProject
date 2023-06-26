#%%
from flask import Flask, send_file
from pathlib import Path


app = Flask(__name__)

current_directory = Path.cwd()

@app.route('/onduty')
def on_duty():
    return send_file(f"{current_directory}/onDutyRecords.json", mimetype="application/json")

@app.route('/offduty')
def off_duty():
    return send_file(f"{current_directory}/offDutyRecords.json", mimetype="application/json")

@app.route("/fullroster")
def full_roster():
    return send_file("/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/json/full_roster.json", mimetype="application/json")

@app.route("/assignments")
def assignment():
    return send_file("/Users/jessemeekins/Documents/VS_CODE/PythonProjectTemplate/app/data/json/full_assignment.json", mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True, port=5050)

