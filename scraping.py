import requests
from bs4 import BeautifulSoup

def get_g1_headlines():
    url = "https://g1.globo.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []
    for item in soup.select(".feed-post-body-title a"):
        title = item.get_text(strip=True)
        link = item.get("href")
        headlines.append({"title": title, "url": link, "source": "G1"})
    return headlines

def get_uol_headlines():
    url = "https://noticias.uol.com.br/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []
    for item in soup.select("h3 a"):
        title = item.get_text(strip=True)
        link = item.get("href")
        headlines.append({"title": title, "url": link, "source": "UOL"})
    return headlines

def get_cnn_headlines():
    url = "https://www.cnnbrasil.com.br/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []
    for item in soup.select("h2 a"):
        title = item.get_text(strip=True)
        link = item.get("href")
        headlines.append({"title": title, "url": link, "source": "CNN Brasil"})
    return headlines

def get_oeste_headlines():
    url = "https://revistaoeste.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []
    for item in soup.select(".jeg_post_title a"):
        title = item.get_text(strip=True)
        link = item.get("href")
        headlines.append({"title": title, "url": link, "source": "Oeste"})
    return headlines
