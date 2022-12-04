

from flask import Flask, jsonify, render_template, request, send_file
import json
import os
import glob
from prediction import *

##### Init #####
app = Flask(__name__)
VERSION = '0.0.1'
number_model, meter_model, lapsrn_model = initialize_models()

##### Routes #####


@app.route('/')
def index():
    return render_template('index.html', title='Thesis API', description='My Thesis API', version=VERSION)


@app.route('/version')
def version():
    return jsonify({'version': VERSION})


@app.route('/detection', methods=['GET'])
def detection():
    args = request.args
    url = args.get('url')
    if url:
        json, data, ts = my_detection(
            url, meter_model, number_model, lapsrn_model)
        return jsonify({'results': json, 'number': data, 'result_image': {'meter': request.url_root + "/view/meter/"+ts, 'number': request.url_root+"/view/number/"+ts}})
    return jsonify({'error': 'url param is null'})


@app.route('/view/meter/<id>')
def view_meter(id=None):
    try:
        dir = "./run_meter/"+id+"/result/"
        images = os.listdir(dir)
        return send_file(dir+images[0], mimetype='image/jpg')
    except:
        return jsonify({'error': 'not found image'})


@app.route('/view/number/<id>')
def view_number(id=None):
    try:
        dir = "./run_number/"+id+"/result/"
        images = os.listdir(dir)
        return send_file(dir+images[0], mimetype='image/jpg')
    except:
        return jsonify({'error': 'not found image'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
