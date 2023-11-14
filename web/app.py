from flask import Flask, render_template, send_file, request
import os
import pandas as pd
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from GET_interaction_score_exhibition import compare_value, combined_torques_graph, map_motion_percent

app = Flask(__name__)


@app.route("/")
def index():
    device = "upper" if request.args.get(
        "device") == None else request.args.get("device")
    body = "body1" if request.args.get("body") == None else request.args.get(
        "body")
    joint = "joint1" if request.args.get(
        "joint") == None else request.args.get("joint")
    code = "code1" if request.args.get("code") == None else request.args.get(
        "code")
    url = f"/?device={device}&body={body}&joint={joint}&code={code}"
    subject = "interactivity"
    return render_template("index.html",
                           url=url,
                           subject=subject,
                           device=device,
                           body=body,
                           code=code)

@app.route('/score')
def score():
    file_path = os.path.dirname(os.path.realpath(__file__)) + "/../" + 'interaction_control_node_1.csv'
    df = pd.read_csv(file_path)
    df = map_motion_percent(df)
    df = df.sort_values('Motion')

    evaluate_file_path = os.path.dirname(os.path.realpath(__file__)) + "/../" + 'Evaluation_Table2.csv' 
    df_evaluate = pd.read_csv(evaluate_file_path)
    total_score = compare_value(df)
    
    return f"{round(total_score,1)}"

@app.route("/score/interactivity", methods=["GET"])
def interactivity():
    file_path = os.path.dirname(os.path.realpath(__file__)) + "/../" + 'interaction_control_node_1.csv'
    df = pd.read_csv(file_path)
    df = map_motion_percent(df)
    df = df.sort_values('Motion')

    evaluate_file_path = os.path.dirname(os.path.realpath(__file__)) + "/../" + 'Evaluation_Table2.csv' 
    df_evaluate = pd.read_csv(evaluate_file_path)
    total_score = compare_value(df)
    
    return f"""
    <div id="usability-result" hx-swap-oob="true" hx-swap="outerHTML">
    <h4>상호작용성 점수: {total_score}</h4>
    <div class="flex justify-center py-12">
    <img id="update-spinner" class="htmx-indicator" src="https://htmx.org/img/bars.svg"/ width=200>
    <img id="usability-result-fig" src="fig/graph"/>
    </div>
    <div>
    <p>
    그래프 수치에 대한 설명
    </p>
    </div>
    </div>
    """


@app.route("/fig/graph", methods=["GET"])
def get_graph():
    file_path = os.path.dirname(os.path.realpath(__file__)) + "/../" + 'interaction_control_node_1.csv'
    df = pd.read_csv(file_path)
    df = map_motion_percent(df)
    df = df.sort_values('Motion')

    evaluate_file_path = os.path.dirname(os.path.realpath(__file__)) + "/../" + 'Evaluation_Table2.csv' 
    df_evaluate = pd.read_csv(evaluate_file_path)

    img = combined_torques_graph(df, df_evaluate)
    return send_file(img, mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051, debug=True)
