from sklearn.feature_extraction.text import HashingVectorizer

_hv = HashingVectorizer(n_features=2**18, alternate_sign=False, norm="l2")

def text_to_tfhash(text: str) -> list[float]:
    return _hv.transform([text]).toarray()[0].astype("float32").tolist()
