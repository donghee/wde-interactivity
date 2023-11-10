from flask import Flask, render_template, send_file, request
import os
import pandas as pd
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from GET_interaction_score import compare_value, combined_torques_graph
app = Flask(__name__)

@app.route('/')
def index():
    device = 'upper' if request.args.get('device') == None else request.args.get('device')
    body = 'body1' if request.args.get('body') == None else request.args.get('body')
    joint = 'joint1' if request.args.get('joint') == None else request.args.get('joint')
    code = 'code1' if request.args.get('code') == None else request.args.get('code')
    url = f'/?device={device}&body={body}&joint={joint}&code={code}'
    return render_template('index.html', url=url, device=device, body=body, code=code)

@app.route('/score/interactivity', methods=['GET'])
def interactivity():
    file_path = os.path.dirname(os.path.realpath(__file__)) + '/../' + '(0724)(on_move) result_human.csv'
    evaluate_file_path = os.path.dirname(os.path.realpath(__file__)) + '/../' + 'Evaluation_Table2.csv' 
    df = pd.read_csv(file_path)
    df_evaluate = pd.read_csv(evaluate_file_path)
    
    #N번 사람 비교
    df_number = df[df['Number'] ==10]
    df_number = compare_value(df_number)
    
    column_values = df_number['Filtered_Score']
    total_score = column_values.mean()  
    return f"""
    <div id="usability-result" hx-swap-oob="true" hx-swap="outerHTML">
    <h4>상호작용성 점수: {total_score}</h4>'
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

@app.route('/fig/graph', methods=['GET'])
def get_graph():
    file_path = os.path.dirname(os.path.realpath(__file__)) + '/../' + '(0724)(on_move) result_human.csv'
    evaluate_file_path = os.path.dirname(os.path.realpath(__file__)) + '/../' + 'Evaluation_Table2.csv' 
    df = pd.read_csv(file_path)
    df_evaluate = pd.read_csv(evaluate_file_path)
    
    #N번 사람 비교
    df_number = df[df['Number'] ==10]
    df_number = compare_value(df_number)
    
    column_values = df_number['Filtered_Score']
    total_score = column_values.mean()  
    
    print('Interactivitiy Score is '+ str(total_score))
 
    img = combined_torques_graph(df_number, df_evaluate)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5051, debug=True)
