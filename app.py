

from flask import Flask, jsonify
import json
import os

app = Flask(__name__)


##### Routes #####
@app.route('/')
def index():
    return jsonify({'title': 'thesis API',
                    'description': 'my thesis API'})


@app.route('/version')
def version():
    return jsonify({'version': '0.0.1'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
