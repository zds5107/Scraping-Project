import sqlite3

def getCategories():
    
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS books
            (title TEXT PRIMARY KEY, price FLOAT, category TEXT, rating INT, url TEXT)''')


    cur.execute('SELECT DISTINCT category FROM books')
    curCategories = {item[0] for item in cur.fetchall()} 
    
    cur.close()
    conn.close()

    return curCategories

def dbInsert(data):

    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS books
                (title TEXT PRIMARY KEY, price FLOAT, category , rating INT, url TEXT)''')

    cur.executemany("INSERT OR IGNORE INTO books (title, price, category, rating, url) VALUES (?,?,?,?,?)", data)
    conn.commit()
        
    cur.close()
    conn.close()

def dbSearch(searchCrit):

    conn = sqlite3.connect("books.db")
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS books
                (title TEXT PRIMARY KEY, price FLOAT, category , rating INT, url TEXT)''')

    if searchCrit[0] == "All":
        cur.execute('SELECT * FROM books')
        res = [item for item in cur.fetchall()]
        
    else:
        cur.execute('SELECT * FROM books WHERE category = ?', (searchCrit[0],))
        res = [item for item in cur.fetchall()]

    if searchCrit[1] != "":
        if searchCrit[1] != "Above":
            res = [item for item in res if item[1] <= searchCrit[1]]

    if searchCrit[2] != "":
        res = [item for item in res if item[3] >= searchCrit[2]]

    return res