import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Baixa o lexicon do VADER
nltk.download("vader_lexicon")

# analisador
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
