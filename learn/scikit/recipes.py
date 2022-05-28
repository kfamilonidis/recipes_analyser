import os
import re
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
    def __init__(self, encoder, refresh = False):
        if not os.path.exists(DS_MODELS_DIR):
            os.makedirs(DS_MODELS_DIR)
        vect_path = os.path.join(DS_MODELS_DIR, 'vectorizer.pkl')
        lenc_path = os.path.join(DS_MODELS_DIR, 'encoder.pkl')
        clf_path  = os.path.join(DS_MODELS_DIR, 'random_forest.pkl')

        if refresh or any(not os.path.exists(i) for i in [vect_path, lenc_path, clf_path]):
            vect, lenc, clf  = encoder.call()

            pickle.dump(vect, open(f.vect, 'wb'))
            pickle.dump(lenc, open(f.lenc, 'wb'))
            pickle.dump(clf, open(f.clf, 'wb'))
        else:
            vect = self.load(vect_path)
            lenc = self.load(lenc_path)
            clf  = self.load(clf_path)

        self.vect = vect
        self.lenc = lenc
        self.clf =  clf
        self.features_in  = len(list(filter(re.compile('^ingredients').match, vect.feature_names_)))
        self.features_out = len(list(filter(re.compile('^recipe').match, vect.feature_names_)))
        pass

    def __enter__(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def load(self, path):
          if os.path.exists(path):
              return pickle.load(open(path, 'rb'))
          else:
              return None

class Encoder(object):
    """docstring for Encoder"""
    def __init__(self):
        super(Encoder, self).__init__()

    def call(self):
        xraw = Fetcher().call()

        xraw = [{'ingredients': [ j['name'] for j in i['ingredients'] ], 'recipe': i['name'] } for i in xraw]
        xraw.sort(key=lambda x: x['recipe'])

        len_out = len(xraw)

        vect = DictVectorizer()
        data = vect.fit_transform(xraw).toarray()
        xdata = data[:,:-len_out]

        len_feature = xdata.shape[1]
        yraw = np.unique([ i['recipe'] for i in xraw ])

        lenc = LabelEncoder()
        ydata = lenc.fit_transform(yraw)

        clf = RandomForestClassifier()
        clf.fit(xdata, ydata)

        return [vect, lenc, clf]


class RecipesV1Analyzer(object):
    """docstring for RecipesV1Analyzer"""
    def __init__(self):
        super(RecipesV1Analyzer, self).__init__()

    def __repr__(self):
        return 'RecipesV1Analyzer'

    def __str__(self):
        return 'RecipesV1Analyzer'

    def call(self, params):
        with ModelFileManager(Encoder, False) as encoder:
            check = encoder.vect.transform({ 'ingredients': ['Μπάμιες', 'Πατάτες','Καρότα', 'Μαϊντανός'] }).toarray()
            check = check[:,:encoder.features_in]

            print(encoder.clf.predict(check))
