import os
from flask import Flask
from flask import render_template
from flask import request
from flask import session , redirect


import pickle
from utils import read_pkl_data, save_as_pkl

app = Flask(__name__,static_url_path='', 
            static_folder='static',
            template_folder='templates')


app.config['SECRET_KEY'] = 'secrsest'    

@app.route('/status/')
def status_check():
    print("*"*30)
    print("Status check reached")
    print("*"*30)
    return 'It\'s working!'

@app.route('/')
def home():
    return 'Please go to /tag/ endpoint'

@app.route('/api/save', methods = ["POST"])
def post_data():
    # labels = json.loads(request.form.get('data'))
    
    # headers = ['fear','anger','joy','sadness','surprise','disgust', 'neutral']

    # print("In updating caption")
    # for header, label in zip(headers, labels):
    #     print("updating")
    #     df.iloc[session['idx']][header] = label

    # data = json.load(request.form.get('data'))
    data = request.get_json()

    print(data)

    return {"status":"success"}


@app.route('/form/save', methods =["GET", "POST"])
def get_form():
    form_data = request.form.to_dict()

    print(form_data)

    data_path = os.path.join(data_dir, f"{session['id']}.pkl")
    data = read_pkl_data(data_path)

    annotations = {}

    for idx, (ent, hint) in data['entities'].items():
        val = form_data[str(idx)]
        annotations[idx] = [ent, val]

    data['annotations'] = annotations
    
    save_as_pkl(data_path, data)

    return redirect('/tag/')


@app.route('/tag/')
def tag():
    if 'id' not in session:
        session['id'] = 0

    if session['id'] < start_id:
        session['id'] = start_id

    if session['id'] > end_id:
        session['id'] = end_id 


    data_path = os.path.join(data_dir, f"{session['id']}.pkl")
    data = read_pkl_data(data_path)

    if not data['annotations']:
        data['annotations'] = data['entities']


    return render_template('tag.html', item=data)

@app.route('/api/update/', methods=["GET"])
def update():

    session['id'] += 1
    return redirect('/tag/')


@app.route('/back/', methods=["GET"])
def back():
    session['id'] -=1
    return redirect('/tag/')

@app.route('/forward/', methods=["GET"])
def forward():
    session['id'] += 1
    return redirect('/tag/')

if __name__ == '__main__':

    start_id = 0
    end_id = 10
    data_dir = './data/artifacts/val_v2/'
    # data = load_data(data_dir)    

    app.run(debug=True)