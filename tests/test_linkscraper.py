from .context import articles_webscraper
from articles_webscraper.LinkScraper import LinkScraper

linkScraper = LinkScraper("xqc article", "01/01/2018","31/01/2018", n_articles = 5)

for l in linkScraper:
    print(l)
