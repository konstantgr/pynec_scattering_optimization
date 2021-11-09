import sys
import os
from flask import Flask, render_template, abort, url_for, json, jsonify
import json
import html


sys.path.insert(0, '..')
app = Flask(__name__)

# read file
with open('../data/optimization_results/configs/test.json', 'r') as myfile:
    data = json.loads(myfile.read())

@app.route("/")
def index():
    return jsonify(**data) #return render_template('index.html', title="page", jsonfile=jsonify(data))

if __name__ == '__main__':
    app.run(debug=True)
