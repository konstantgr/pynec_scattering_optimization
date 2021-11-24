import sys
import os
from flask import Flask, render_template, send_from_directory #,  abort, url_for, json, jsonify
from os import listdir
from os.path import isfile, join, abspath

import json
import html


# sys.path.insert(0, '..')
app = Flask(__name__)

# read file
# with open('../data/optimization_results/configs/test.json', 'r') as myfile:
#     data = json.loads(myfile.read())


def get_files(directory):
    return [f for f in listdir(directory) if isfile(join(directory, f))]

@app.route("/")
def index():
    # return jsonify(**data)
    return render_template('index.html', title="page")


MEDIA_FOLDER_IMAGES = '../data/optimization_results/images/'
MEDIA_FOLDER_CONFIGS = '../data/optimization_results/configs/'


@app.route('/uploads/<path:filename>')
def download_image(filename):
    return send_from_directory(MEDIA_FOLDER_IMAGES, filename, as_attachment=True)


@app.route('/uploads/<path:filename>')
def download_config(filename):
    return send_from_directory(MEDIA_FOLDER_CONFIGS, filename, as_attachment=False)


@app.route("/images")
def images():
    path = '../data/optimization_results/images/'
    filenames = get_files('../data/optimization_results/images')
    # files = ['http://127.0.0.1:5000' + abspath(path + filename) for filename in filenames]
    files = [filename for filename in filenames]
    configs = [f[:-4] + '.json' for f in files]
    # return jsonify(**data)
    # files = [1,2,3]
    print(files)

    return render_template('images_page.html', title="page", files=files, configs=configs)


if __name__ == '__main__':
    app.run(debug=True)
