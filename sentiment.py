import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Baixa o lexicon do VADER (se ainda não estiver baixado)
nltk.download("vader_lexicon")

# Inicializa o analisador
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str):
    scores = sia.polarity_scores(text)
    if scores["compound"] >= 0.05:
        sentiment = "positivo"
    elif scores["compound"] <= -0.05:
        sentiment = "negativo"
    else:
        sentiment = "neutro"
    return {"text": text, "sentiment": sentiment, "scores": scores}
