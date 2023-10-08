import joblib


def is_hate_speech(text):
    cv = joblib.load("algorithm/cv.joblib")
    clf = joblib.load("algorithm/clf.joblib")

    df = cv.transform([text]).toarray()
    msg = clf.predict(df)[0]

    POSSIBLE_TEXT = [
        "Hate Speech Detected",
        "Offensive Language Detected",
        "Neither Hate Speech nor Offensive Language Detected",
    ]

    if msg == POSSIBLE_TEXT[0] or msg == POSSIBLE_TEXT[1]:
        return True

    return False
