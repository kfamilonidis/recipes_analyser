import base64
import json
from io import BytesIO

import numpy as np
import requests
from flask import Flask, request, jsonify

# from flask_cors import CORS

app = Flask(__name__)

# Uncomment this line if you are making a Cross domain request
# CORS(app)

# Testing URL
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello, World 1!'

app.add_url_rule('/machine', 'hello_world', hello_world)
