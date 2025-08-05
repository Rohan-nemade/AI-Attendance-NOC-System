import spacy

nlp = spacy.load("en_core_web_sm")

def clean_text(text: str) -> str:
    doc = nlp(text)
    tokens =[
        token.lemma_.lower()
        for token in doc
        if not token.is_stop and token.is_alpha
    ]
    return " ".join(tokens)