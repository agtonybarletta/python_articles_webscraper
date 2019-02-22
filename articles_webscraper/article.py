from newspaper import Article
from selenium import webdriver
import time
def get_article(url, lan='en'):
    article = Article(url)
    driver = webdriver.Firefox()
    try:

        driver.get(url)
        time.sleep(2)
        html = driver.page_source
        article.download(input_html=html)
        article.parse()
        driver.close()
        return (article.title, article.text)
    except Exception as e:
        driver.close()
        return None,None

def get_article_fast(url, lan='en'):
    article = Article(url,language=lan)
    try:
        article.download()
        article.parse()
        return (article.title, article.text)
    except Exception as e:
        return None,None