import joblib
from fastapi import FastAPI, HTTPException
from typing import Annotated
from pydantic import Field

app = FastAPI()
model = joblib.load("model.joblib")


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/predict")
def predict(features: Annotated[list[float], Field(min_length=4, max_length=4)]):
    if len(features) != 4:
        raise HTTPException(status_code=422, detail="features must contain exactly 4 floats")
    prediction = model.predict([features])
    return {"prediction": int(prediction[0])}
