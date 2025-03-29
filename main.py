from gui import App
from db import getCategories, dbInsert, dbSearch
from scrape import getAllCategories, scrapeCategory

def search(searchCrit):
    return dbSearch(searchCrit)   

def scrape_button_press(category):
    
    #1-scrape the current selected category
    #2-insert in data into the DB
    dbInsert(scrapeCategory(category))

def main():
    
    #inital data needed for gui
    curCat = getCategories()
    allCat = getAllCategories()
    canScrape = allCat-curCat
    canScrape = list(canScrape)
    canScrape.sort()
    
    App(tuple(canScrape), curCat, scrape_button_press, search)

if __name__ == "__main__":
    main()