import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime

URL = "https://lambersart.fr/actualites"

def fetch_articles():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    for item in soup.select("article.teaser"):
        title_tag = item.select_one(".teaser-title, h2, h3")
        title = title_tag.text.strip() if title_tag else "Sans titre"
        link_tag = item.find("a")
        link = link_tag["href"] if link_tag else "#"
        full_link = link if link.startswith("http") else "https://lambersart.fr" + link
        pub_date = datetime.now()

        articles.append({
            "title": title,
            "link": full_link,
            "pubDate": pub_date,
        })

    return articles

def generate_rss(articles):
    fg = FeedGenerator()
    fg.title("Actualités de Lambersart")
    fg.link(href=URL, rel='alternate')
    fg.description("Flux RSS des actualités du site officiel de Lambersart")

    for article in articles:
        fe = fg.add_entry()
        fe.title(article["title"])
        fe.link(href=article["link"])
        fe.pubDate(article["pubDate"])

    fg.rss_file("feed.xml")

if __name__ == "__main__":
    articles = fetch_articles()
    generate_rss(articles)
