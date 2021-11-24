import streamlit as st
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join, abspath
from PIL import Image
import json


def get_files(directory):
    return [abspath(directory + '/' + f) for f in listdir(directory) if isfile(join(directory, f))]


def get_data(path):
    configs = [file for file in get_files(path + 'configs/')]
    images = [file for file in get_files(path + 'images/')]

    return images, configs


def get_layout(n, images, configs):
    st.set_page_config(layout='wide')
    cols = st.columns([12 for i in range(n)])

    for i, image_path in enumerate(images):
        try:
            json_file = [cf for cf in configs
                         if image_path.split('/')[-1][:-4] in cf][0]
        except Exception as e:
            json_file = None

        if json_file:
            with open(json_file, 'r') as f:
                config = json.loads(f.read())
                best_result = config['best_result']
                optimizator = config['kind']
                cols[i % n].subheader(f'Optimizator: {optimizator}')
                cols[i % n].subheader(f'best result: {round(best_result, 3)}')
                cols[i % n].download_button(
                    label='download config',
                    data=open(json_file, 'r'),
                    file_name=json_file.split('/')[-1],
                    mime='json'
                )
                with cols[i % n].expander('see config') as a:
                    st.json(config)

        im = Image.open(image_path)
        cols[i % n].image(im, use_column_width=True)


if __name__ == '__main__':
    data_path = 'data/optimization_results/'
    images, configs = get_data(data_path)
    get_layout(4, images, configs)
