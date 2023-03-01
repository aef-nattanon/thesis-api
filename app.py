

from flask import Flask, jsonify, render_template, request, send_file
from flask_cors import CORS
from firebase_app import *

import os
import multiprocessing as mp
from prediction import *
from helper import *

##### Init #####
app = Flask(__name__)
CORS(app)
VERSION = '0.0.2'
number_model, meter_model, lapsrn_model = initialize_models()
cred, default_app, db, result_images_ref, bucket = initialize_firestore()

##### Routes #####
@app.route('/')
def index():
    return render_template('index.html', title='Thesis API', description='My Thesis API', version=VERSION)


@app.route('/version')
def version():
    return jsonify({'version': VERSION})


@app.route('/detection', methods=['GET', 'POST'])
def detection():
    try:
        if request.method == 'POST':
            print("👆 POST")
            request_data = request.get_json()
            url = request_data['url']
        elif request.method == 'GET':
            print("👆 GET")
            args = request.args
            url = args.get('url')
        else:
            return jsonify({'error': 'error methods'})

        print("🔗 image url:", url)
        if url:
            json, data, ts, meter_path, number_path = my_detection(
                url, meter_model, number_model, lapsrn_model)

            meter_url = firebase_upload_image(meter_path, bucket)
            number_url = firebase_upload_image(number_path, bucket)

            remove_file_p = mp.Process(target=remove_file(ts))
            remove_file_p.start()

            return jsonify({
                    'results': json,
                    'number': data,
                    'result_image': {
                        'meter': meter_url,
                        'number': number_url
                    }
                })
        return jsonify({'error': 'url param is null'})
    except NameError:
        return jsonify({'error': NameError})


# @ app.route('/view/meter/<id>')
# def view_meter(id=None):
#     try:
#         dir = os.getcwd()+"/run_meter/"+id+"/result/"
#         images = os.listdir(dir)
#         return send_file(dir+images[0], mimetype='image/jpg')
#     except NameError:
#         return jsonify({'error': NameError})


# @ app.route('/view/number/<id>')
# def view_number(id=None):
#     try:
#         dir = os.getcwd()+"/run_number/"+id+"/result/"
#         images = os.listdir(dir)
#         return send_file(dir+images[0], mimetype='image/jpg')
#     except NameError:
#         return jsonify({'error': NameError})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
