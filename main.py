from src import pipelines
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main():
    predictions = pipelines.predict_withpath('data/Digital_Payment_Fraud_Detection_Dataset.csv')
    print('done')


if __name__ == "__main__":
    main()
