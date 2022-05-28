import base64
import json
from io import BytesIO

import numpy as np
import requests
from flask import Flask, request, jsonify

from learn.scikit.recipes import RecipesV1Analyzer

# from flask_cors import CORS

app = Flask(__name__)

# Uncomment this line if you are making a Cross domain request
# CORS(app)

# Testing URL
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello, World 1,2!'

@app.route('/recipes/v1/analyzer/predict', methods=['GET', 'POST'])
def recipes_v1_analyzer_predict():
    analyzer = RecipesV1Analyzer()
    analyzer.call(request.args.getlist('ingredients[]'))

    return 'Hello, World 1,2!'

@app.route('/recipes/v1/analyzer/update', methods=['GET', 'POST'])
def recipes_v1_analyzer_update():


    return 'Hello, World 1,2!'

app.add_url_rule('/machine', 'hello_world', hello_world)
app.add_url_rule('/machine', 'recipes_v1_analyzer_predict', recipes_v1_analyzer_predict)
app.add_url_rule('/machine', 'recipes_v1_analyzer_update', recipes_v1_analyzer_update)
