import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://helgg:1234@172.28.240.1:5432/newsdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de dados: Tabela "news"
class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    source = Column(String, nullable=False)
    sentiment = Column(String, nullable=False)

# cria a tabela no banco
def init_db():
    Base.metadata.create_all(bind=engine)

# salva uma notícia
def save_news(db, title, url, source, sentiment):
    news_entry = News(title=title, url=url, source=source, sentiment=sentiment)
    db.add(news_entry)
    db.commit()
    db.refresh(news_entry)
    return news_entry

# retornar todas as notícias armazenadas
def get_stored_news(db):
    return db.query(News).all()
