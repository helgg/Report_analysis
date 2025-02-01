from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from scraping import get_g1_headlines, get_us_headlines, get_uk_headlines, get_germany_headlines, get_france_headlines, get_japan_headlines

from sentiment import analyze_sentiment
from database import SessionLocal, init_db, save_news, get_stored_news, News

# Inicializa o banco de dados (cria a tabela se não existir)
init_db()

app = FastAPI(title="API de Análise de Sentimento de Notícias")

class SentimentRequest(BaseModel):
    text: str

# Dependência para gerenciar a sessão com o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/news", summary="Coleta notícias dos portais, analisa o sentimento e salva no banco")
def get_news(db: Session = Depends(get_db)):
    # todos os portais de notícias
    news_sources = [
        get_g1_headlines,
        get_us_headlines,
        get_uk_headlines,
        get_germany_headlines,
        get_france_headlines,
        get_japan_headlines
    ]
    all_news = []
    for source_func in news_sources:
        headlines = source_func()
        for item in headlines:
            sentiment_result = analyze_sentiment(item["title"])
            item["sentiment"] = sentiment_result["sentiment"]
            save_news(db, item["title"], item["url"], item["source"], item["sentiment"])
        all_news.extend(headlines)
    return all_news

@app.get("/stored-news", summary="Retorna notícias armazenadas com filtros opcionais")
def fetch_stored_news(
    db: Session = Depends(get_db),
    source: Optional[str] = Query(None, description="Filtra notícias por portal (ex.: G1, UOL, CNN Brasil, Oeste)"),
    sentiment: Optional[str] = Query(None, description="Filtra notícias por sentimento (ex.: positivo, negativo, neutro)")
):
    query = db.query(News)
    if source:
        query = query.filter(News.source.ilike(f"%{source}%"))
    if sentiment:
        query = query.filter(News.sentiment.ilike(f"%{sentiment}%"))
    return query.all()

@app.post("/analyze", summary="Analisa o sentimento de um texto personalizado")
def analyze_text(data: SentimentRequest):
    return analyze_sentiment(data.text)
