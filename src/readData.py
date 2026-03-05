# The main objective of this code is to the data and read it
# TODO: Implement testing (The dataframe is correctly read)
# TODO: Also impement another data read for when data given through streamlit or API

import pandas as pd

class DataReader():
    """
    This class reads all the data
    """

    def read_data(self, path:str) -> tuple[pd.DataFrame, str] :
        """
        The main objective of this data set is to read the provided data set
        and return a pandas dataframe

        Parameters
        ----------
        path : str
            This is the path to the csv file:

        Returns
        -------
        dataframe : pd.DataFrame
            This is the dataframe read from the path provided
        error : str
            In case of an error this string has the error, otherwise
            it is an empty string
        """
        dataframe: pd.DataFrame = pd.DataFrame()
        error: str = ""

        try:
            dataframe = pd.read_csv(path)
        except Exception as e:
            error = f'Function failed, error {e}'
        finally:
            return dataframe,error
