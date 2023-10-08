import joblib
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    text: str


@app.post("/predict")
def read_item(item: Item):
    text = item.text

    hate_speech = False

    cv = joblib.load("cv.joblib")
    clf = joblib.load("clf.joblib")

    df = cv.transform([text]).toarray()

    msg = clf.predict(df)[0]

    POSSIBLE_TEXT = [
        "Hate Speech Detected",
        "Offensive Language Detected",
        "Neither Hate Speech nor Offensive Language Detected",
    ]

    if msg == POSSIBLE_TEXT[0] or msg == POSSIBLE_TEXT[1]:
        hate_speech = True

    return {"hate_speech": hate_speech, "message": msg}
