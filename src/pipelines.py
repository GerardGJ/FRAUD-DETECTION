# This code will have all the different pipelines

from readData import DataReader
from preprocessing import Preprocesser
from predict import Predicter

def predict_withpath(path:str):
    
    # First we istanciate all the differnt classes
    reader = DataReader()
    preprocesser = Preprocesser()
    predicter = Predicter()

    df,error = reader.read_data(path)

    if not error:
        df_preprocessed = preprocesser.transform(df)
    
    output = predicter.predict(df_preprocessed)

    print(output)

    


predict_withpath("data/Digital_Payment_Fraud_Detection_Dataset.csv")
