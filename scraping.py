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

def get_us_headlines():
    url = "https://www.cnn.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []    
    for item in soup.select("h3.cd__headline a"):
        title = item.get_text(strip=True)
        link = item.get("href")
        if link and not link.startswith("http"):
            link = "https://www.cnn.com" + link
        headlines.append({"title": title, "url": link, "source": "CNN US"})
    return headlines

def get_uk_headlines():
    url = "https://www.theguardian.com/uk"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []
    for item in soup.select(".fc-item__title a"):
        title = item.get_text(strip=True)
        link = item.get("href")
        headlines.append({"title": title, "url": link, "source": "The Guardian"})
    return headlines

def get_germany_headlines():
    url = "https://www.spiegel.de/international/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []
    for item in soup.select("article h2 a"):
        title = item.get_text(strip=True)
        link = item.get("href")
        if link and not link.startswith("http"):
            link = "https://www.spiegel.de" + link
        headlines.append({"title": title, "url": link, "source": "Der Spiegel"})
    return headlines

def get_france_headlines():
    url = "https://www.lemonde.fr/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []
    for item in soup.select("h3.teaser__title a"):
        title = item.get_text(strip=True)
        link = item.get("href")
        headlines.append({"title": title, "url": link, "source": "Le Monde"})
    return headlines

def get_japan_headlines():
    url = "https://www.japantimes.co.jp/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []
    for item in soup.select("h2.entry-title a"):
        title = item.get_text(strip=True)
        link = item.get("href")
        headlines.append({"title": title, "url": link, "source": "Japan Times"})
    return headlines
