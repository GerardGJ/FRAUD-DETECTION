def test_read_data():
    import pandas as pd
    from src.readData import DataReader
    
    dr = DataReader()
    df = dr.read_data('data/Digital_Payment_Fraud_Detection_Dataset.csv')[0]
    assert isinstance(df,pd.DataFrame)