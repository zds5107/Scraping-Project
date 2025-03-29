from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re

word_to_num = {
    "One" : 1,
    "Two" : 2,
    "Three" : 3,
    "Four" : 4,
    "Five" : 5
}

categoryToLink = {}
base_url = "https://books.toscrape.com/catalogue/"

def getAllCategories():
    #categoryToLink = {}
    
    url = f"https://books.toscrape.com/catalogue/page-{1}.html"
    res = requests.get(url)
    doc = BeautifulSoup(res.text, "html.parser")
    catElems = doc.find(class_="nav nav-list").li.ul.find_all("li")
    
    for item in catElems:
        link = item.a.get("href")
        categoryToLink[item.a.string.strip()] = link[:len(link)-10]
    
    return {item.a.string.strip() for item in catElems}

def scrapeCategory(category):
    if category != "":
        
        scrappedInfo=[]
        #print(categoryToLink[category])
        url = urljoin(base_url, categoryToLink[category])

        res = requests.get(url)
        doc = BeautifulSoup(res.text, "html.parser")


        pages = 1
        if doc.find(class_="current"): 
            pages = int(doc.find(class_= "current").string.strip().split()[3])

        for i in range(1, pages+1):
            if i != 1:
                res = requests.get(f"{url}page-{i}.html")
                doc = BeautifulSoup(res.text, "html.parser")

            pageArticles = doc.find_all(class_= "product_pod")

            for article in pageArticles:
                productLink = article.a.get("href")
                fullProductLink = urljoin(url, productLink)
                res = requests.get(fullProductLink)
                doc = BeautifulSoup(res.text, "html.parser")

                productPrice = float(doc.find(class_="price_color").string[2:])
                productName = doc.find(class_="col-sm-6 product_main").h1.text
                productCat = doc.find(class_="breadcrumb").find_all('li')[2].a.string

                productRating = word_to_num[doc.find(class_=re.compile('^star-rating')).get('class')[1]]
                productURL = fullProductLink
        
                scrappedInfo.append((productName,productPrice,productCat, productRating, productURL))
        
        return scrappedInfo