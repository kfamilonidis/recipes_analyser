import numpy as np

from learn.fetcher import Fetcher

from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

class Encoder(object):
    """docstring for Encoder"""
    def __init__(self):
        super(Encoder, self).__init__()

    def call(self):
        xraw = Fetcher("https://familonidis.io/food/api/recipes.json").call()

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
