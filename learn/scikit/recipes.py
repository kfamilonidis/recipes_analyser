import os
import requests
import json
import numpy as np
import pickle
import multiprocessing

from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

DS_MODELS_DIR = '../../saved_models'

class Fetcher(object):
    """docstring for Fetcher."""
    def __init__(self, url = "https://familonidis.io/food/api/recipes.json"):
        super(Fetcher, self).__init__()
        self.url = url
        self.data = []

    def call(self):
        data = requests.get(self.url)
        self.data = json.loads(data.text)

        return self.data

class ModelFileManager():
  """docstring for ModelFileManager"""
  def __init__(self):
    pass

  def __enter__(self):
    print('__enter__')
    return self

  def __exit__(self, exc_type, exc_value, exc_traceback):
    print('__exit__')
    pass

class Encoder(object):
    """docstring for Encoder"""
    def __init__(self):
        super(Encoder, self).__init__()
        if not os.path.exists(DS_MODELS_DIR):
            os.makedirs(DS_MODELS_DIR)


    def call(self):
        with ModelFileManager() as f:
            xraw = Fetcher().call()

            xraw = [{'ingredients': [ j['name'] for j in i['ingredients'] ], 'recipe': i['name'] } for i in xraw]
            xraw.sort(key=lambda x: x['recipe'])

            len_out = len(xraw)

            vect = DictVectorizer()
            data = vect.fit_transform(xraw).toarray()
            xdata = data[:,:-len_out]

            len_feature = xdata.shape[1]
            yraw = np.unique([ i['recipe'] for i in xraw ])

            le = LabelEncoder()
            ydata = le.fit_transform(yraw)

            clf = RandomForestClassifier()
            clf.fit(xdata, ydata)

            pickle.dump(clf, open(os.path.join(DS_MODELS_DIR, 'random_forest.pkl'), 'wb'))
            pickle.dump(vect, open(os.path.join(DS_MODELS_DIR, 'vectorizer.pkl'), 'wb'))
            pickle.dump(le, open(os.path.join(DS_MODELS_DIR, 'encoder.pkl'), 'wb'))

        pass


class RecipesV1Analyzer(object):
    """docstring for RecipesV1Analyzer"""
    def __init__(self):
        super(RecipesV1Analyzer, self).__init__()

    def __repr__(self):
        return 'RecipesV1Analyzer'

    def __str__(self):
        return 'RecipesV1Analyzer'

    def call(self, params):
        print(params)
        # thread = multiprocessing.Process(target=Encoder().call, args=())
        # thread.start()

        pass
