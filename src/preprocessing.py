# This script is in charge of preprocessing the data
import polars as pl
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
CATEGORICAL_VARIABLES = ["transaction_type", "payment_mode", "device_type", "device_location"]



class Preprocesser():

    def _previousActionsGenerator(self, 
                                 df: pl.DataFrame
        ) -> pl.DataFrame: 
        """
        Generation of feature engineering variables based on past actions.
        The features fenerated are:
            - previous_fraud : Boolean variable that tell if user previously commited faud
            - previous_fraud_num : Numeric variable that tells how many times was comited fraud previously
                                    by the user
            - previous_transactions : Boolean variable that shows if a user previouly made a transaction
            - previous_transactions_num : Numeric variable that shows how many transaction the user 
                                            made before
        
        Parameters
        ----------
            df:pd.DataFrame 
        
        Returns
        -------
            df:pd.DataFrame
        """

        df = (
            df
            .with_columns(pl.col("transaction_id").str.replace("T","").alias("transaction_id_number"))
            .cast({"transaction_id_number": pl.Int16})
            .sort("transaction_id_number")

        )

        df2 = df.select(["transaction_id_number","user_id","fraud_label"])

        df_join = (
            df
            .join(df2, 
                on='user_id',
                how="inner",
                suffix='_r')
            .filter(
                pl.col('transaction_id_number') > pl.col("transaction_id_number_r")
            )
        )

        df_agg =df_join.group_by("user_id","transaction_id_number").agg(
            fraud_any=pl.col('fraud_label').any().cast(pl.Int8),
            fraud_number=pl.col("fraud_label").sum(),
            transaction_any=1,
            transaction_number=pl.col("fraud_label").count(),
        )

        df = (
            df
            .join(
                df_agg,
                on=['user_id','transaction_id_number'],
                how='left'
            )
            .fill_null(0)
            .drop('transaction_id_number')
        )

        return df

    def _getFeaturnEncodingModles(self, 
                                 categorical_columns: list[str]
        ) -> dict[str,LabelEncoder]:

        dict_le = dict()
        for col in categorical_columns:
            path = f"utils_models/{col}_LE.joblib"
            le = joblib.load(path)

            dict_le[col] = le

        return dict_le
         
    def _featrueEncoding(self, 
                        dict_le: dict[str,LabelEncoder], 
                        df: pd.DataFrame, 
                        categorical_columns: list[str]
    ) -> pd.DataFrame:
        
        for col in categorical_columns:
            print(f"Encoding column: {col}")
            encoded_col = dict_le[col].transform(df[col])

            df[col] = encoded_col

        return df

    def transform(self, 
                  df:pd.DataFrame
        ) -> pd.DataFrame:
        """
        This method is in charge of preprocessing the data
        """

        df_polars = pl.from_pandas(df)
        
        # The first step in the preprocessing step is the 
        # Feature Engineering
        df_fe_polars = self._previousActionsGenerator(df_polars)
        df_fe = df_fe_polars.to_pandas()

        # After this we will encode the different features
        # First we get the label encoders
        dict_le = self._getFeaturnEncodingModles(CATEGORICAL_VARIABLES)
        df_le = self._featrueEncoding(dict_le,df_fe,CATEGORICAL_VARIABLES)

        return df_le


