
import joblib
import pandas as pd
from utils import read_yaml

class Predicter():

    def _getModel(self, path:str):
        model = joblib.load(path)
        return model
    
    def predict(self, df:pd.DataFrame):
        config = read_yaml()

        ids = df[['transaction_id','user_id']]
        X = df.drop(columns=['transaction_id','user_id','fraud_label'])

        model = self._getModel(config['model'])
        predictions = model.predict(X)

        ids['predictions'] = predictions

        return ids