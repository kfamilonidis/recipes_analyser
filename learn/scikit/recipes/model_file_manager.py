import os
import re
import numpy as np
import pickle

DS_MODELS_DIR = '../../../saved_models'

class ModelFileManager():
    """docstring for ModelFileManager"""
    def __init__(self, encoder, refresh = False):
        if not os.path.exists(DS_MODELS_DIR):
            os.makedirs(DS_MODELS_DIR)

        vect_path = os.path.join(DS_MODELS_DIR, 'vectorizer.pkl')
        lenc_path = os.path.join(DS_MODELS_DIR, 'encoder.pkl')
        clf_path  = os.path.join(DS_MODELS_DIR, 'random_forest.pkl')

        if refresh or any(not os.path.exists(i) for i in [vect_path, lenc_path, clf_path]):
            vect, lenc, clf = encoder.call(self)

            pickle.dump(vect, open(vect_path, 'wb'))
            pickle.dump(lenc, open(lenc_path, 'wb'))
            pickle.dump(clf, open(clf_path, 'wb'))
        else:
            vect = self.load(vect_path)
            lenc = self.load(lenc_path)
            clf  = self.load(clf_path)

        self.vect = vect
        self.lenc = lenc
        self.clf =  clf
        self.features_in  = len(list(filter(re.compile('^ingredients').match, vect.feature_names_)))
        self.features_out = len(np.unique(list(filter(re.compile('^recipe').match, vect.feature_names_))))
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
