from .model_file_manager import ModelFileManager
from .encoder import Encoder

class RecipesV1Analyzer(object):
    """docstring for RecipesV1Analyzer"""
    def __init__(self):
        super(RecipesV1Analyzer, self).__init__()

    def __repr__(self):
        return 'RecipesV1Analyzer'

    def __str__(self):
        return 'RecipesV1Analyzer'

    def call(self, params, refresh = False):
        print(params)

        with ModelFileManager(Encoder, refresh) as encoder:
            check = encoder.vect.transform({ 'ingredients': params['ingredients'] }).toarray()
            check = check[:,:encoder.features_in]

            pred = encoder.clf.predict(check)
            pred_a = encoder.clf.predict_proba(check)

            pred_decoded = encoder.lenc.inverse_transform(pred)
            check_decoded = encoder.vect.inverse_transform(check)

            probs = [{ 'prob': pred_a[0][i], 'recipe': j } for i, j in enumerate(encoder.lenc.classes_)]
            probs.sort(key=lambda x: x['prob'], reverse=True)
            probs = list(filter(lambda x: x['prob'] != 0.0 , probs))

            return {
              "predict": pred_decoded.tolist(),
              "input": check_decoded,
              "probs": probs
            }
