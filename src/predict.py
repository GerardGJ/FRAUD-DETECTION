
import joblib
import pandas as pd
from src.utils import read_yaml
from typing import Any

class Predicter():

    def _getModel(self, path:str) -> Any:
        """
        Loads the model from the path

        Parameters
        ----------
        path : str
            path to the model to be loaded
        
        Retruns
        -------
        model : Any
            Loaded model form the path given to make the predictions
        """
        model = joblib.load(path)
        return model
    
    def predict(self, df:pd.DataFrame) -> pd.DataFrame:
        """
        Makes predictions given a dataframe

        Parameters
        ----------
        df : pd.DataFrame
            The pandas dataframe that will be used to make the predictions

        Retruns
        -------
        ids : pd.DataFrame
            DataFrame with the different predictions with the id of the user, id of the transaction and the prediction
        """
        config = read_yaml()

        ids = df[['transaction_id','user_id']]
        X = df.drop(columns=['transaction_id','user_id','fraud_label'])

        model = self._getModel(config['model'])
        predictions = model.predict(X)

        ids['predictions'] = predictions

        return ids