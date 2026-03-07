from src import pipelines
import uvicorn

from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Summary, generate_latest, CONTENT_TYPE_LATEST, REGISTRY

app = FastAPI()

def get_or_create_counter(name, documentation, labelnames):
    if name in REGISTRY._names_to_collectors:
        return REGISTRY._names_to_collectors[name]
    return Counter(name, documentation, labelnames)

def get_or_create_summary(name, documentation, labelnames):
    if name in REGISTRY._names_to_collectors:
        return REGISTRY._names_to_collectors[name]
    return Summary(name, documentation, labelnames)

EXCEPTIONS = get_or_create_counter(
    "app_exceptions_total", 
    "Total number of unhandeled exceptions.",
    ["endpoint", "exception_type"]
)

REQUEST_COUNT = get_or_create_counter(
    "app_requests_total", 
    "Total number of requests.",
    ["method", "endpoint"]
)

EXECUTION_TIME = get_or_create_summary(
    "app_execution_time_summary",
    'Summarized information about execution time', 
    ["endpoint"]
)


@app.exception_handler(Exception)
async def catch_all(request:Request, e:Exception):
    EXCEPTIONS.labels(
        endpoint=request.url.path,  
        exception_type=type(e).__name__
    ).inc()

    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred.", "type": type(e).__name__},
    )


@app.middleware("http")
async def count_requests(request:Request, call_next):
    REQUEST_COUNT.labels(
        method=request.method, 
        endpoint=request.url.path
    ).inc()

    response = await call_next(request)
    return response


@EXECUTION_TIME.labels(endpoint="heavy_task").time()
@app.get("/predict")
def predict():
    predictions = pipelines.predict_withpath('data/Digital_Payment_Fraud_Detection_Dataset.csv')

    csv_data = predictions.to_csv(index=False)

    return Response(content=csv_data, media_type="text/csv")

@app.get('/metrics')
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)