# This code will have all the different pipelines

import pandas as pd

from readData import DataReader
from preprocessing import Preprocesser
from predict import Predicter

def predict_withpath(path:str) -> pd.DataFrame:
    
    # First we istanciate all the differnt classes
    reader:DataReader = DataReader()
    preprocesser:Preprocesser = Preprocesser()
    predicter:Predicter = Predicter()

    df,error = reader.read_data(path)

    if not error:
        df_preprocessed = preprocesser.transform(df)
    
    output = predicter.predict(df_preprocessed)

    return output
