import tkinter as tk
from tkinter import ttk
import webbrowser




class App(tk.Tk):
    def __init__(self, canScrape, curCat, rtnScrapCat, rtnSearch):
        super().__init__()
        self.title("Scrapping Project")
        self.geometry("1200x600")
        self.rtnScrapCat = rtnScrapCat
        self.rtnSearch = rtnSearch

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(sticky="nsew")

        self.idToLink = {}

        #Scrape Frame
        self.frame1 = tk.Frame(self.notebook)
        self.frame1.columnconfigure((0,1),weight=1)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=3)

        self.catSelector = Combo(self.frame1, canScrape)
        self.haveDisplay = Display(self.frame1, curCat)
        self.scrapeButton = Button(self.frame1, self.selected) 
        self.notebook.add(self.frame1, text="Scrape")

        #Search Frame
        self.frame2 = tk.Frame(self.notebook)
        self.frame2.columnconfigure(0,weight=1)
        self.frame2.columnconfigure(1,weight=3)

        self.seachFrame = SearchFilters(self.frame2, curCat, self.search)
        self.table = searchRes(self.frame2, self.openLink)

        self.notebook.add(self.frame2, text="Search")

        self.mainloop()

    def openLink(self, event):
        id = self.table.focus()
        if id:
            webbrowser.open(self.idToLink[id])
    
    def search(self):

        cat = self.seachFrame.curCat.get()
        price = self.seachFrame.curPrice.get()
        if price != "":

            if price != "$70 and Above":
                price = float(price[1:])
            else:  
                price = price.split()
                price = price[len(price)-1]

        rat = self.seachFrame.curRat.get()
        if rat != "":
            rat = int(rat.split()[0])
        
        searchCrit = (cat, price, rat)

        self.updateTable(self.rtnSearch(searchCrit))

    def selected(self):
        
        selected = self.catSelector.selected.get()
        if selected != "":
            self.haveDisplay.listbox.insert(tk.END, selected)
            
            items = list(self.catSelector['values'])
            items.remove(selected)
            self.catSelector['values'] = items
            self.catSelector.set('')
            
            self.seachFrame.combo['values'] = self.haveDisplay.listbox.get(0,tk.END)

            self.rtnScrapCat(selected)

    def updateTable(self,res):
        
        self.idToLink.clear()

        for item in self.table.get_children():
            self.table.delete(item)


        for item in res:
            id = self.table.insert("", "end", values=item[:4])
            self.idToLink[id] = item[4]


class Display(tk.Frame):
    def __init__(self,parent, curCat):
        super().__init__(parent)

        have_label = ttk.Label(self, text="Already Scrapped", font = "Calibri 18 bold")
        have_label.pack()


        self.listbox = tk.Listbox(self, width=40, height=15, selectmode=tk.NONE)
        self.listbox.pack(side="left", expand=True)
        
        for item in curCat:
            self.listbox.insert(tk.END, item)

        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)


        self.grid(row=1,column=1)

class Button(tk.Button):
    def __init__(self, parent, command):
        super().__init__(parent,text= "Scrape", height=5, width=20, font = "Calibri 18 bold", command=command)
        self.grid(row=1,column=0)

class Combo(ttk.Combobox):
    def __init__(self, parent, canScrape):
        self.selected = tk.StringVar()
        super().__init__(parent, state="readonly", textvariable = self.selected)
        self["values"] = canScrape
        self.grid(row=0, column=0, columnspan=2)

class searchRes(ttk.Treeview):
    def __init__(self, parent, command):
        super().__init__(parent, columns= ('Title', 'Price', 'Category', 'Rating'), show="headings")
        self.heading('Title', text="Title")
        self.heading('Price', text="Price")
        self.heading('Category', text="Category")
        self.heading('Rating', text="Rating")
        self.bind("<Double-1>", command)
        self.grid(row=0,column=1, sticky="nsew")
        
class SearchFilters(tk.Frame):
    def __init__(self,parent, curCat, command):
        super().__init__(parent)
        
        label1 = ttk.Label(self, text="Category:" )
        label1.grid(row=0,column=0, pady=10)

        self.curCat = tk.StringVar()
        self. combo = ttk.Combobox(self, state="readonly", textvariable= self.curCat)
        categories = list(curCat)
        categories.append("All")
        self.combo['values'] = categories
        self.combo.set(list(self.combo['values'])[0])
        self.combo.grid(row=0, column=1, pady=10)

        label2 = ttk.Label(self, text="Rating:")
        label2.grid(row=1,column=0, pady=10)

        self.curRat = tk.StringVar()
        combo2 = ttk.Combobox(self, state="readonly", textvariable=self.curRat)
        combo2['values'] = ["1 Star and Up", "2 Stars and Up", "3 Stars and Up", "4 Stars and Up", "5 Stars" ]
        combo2.grid(row=1, column=1, pady=10)

        label3 = ttk.Label(self, text="Price up to:")
        label3.grid(row=2,column=0, pady=10)


        self.curPrice = tk.StringVar()
        combo3 = ttk.Combobox(self, state="readonly", textvariable= self.curPrice)
        combo3['values'] = ["$10", "$20", "$30", "$40", "$50", "$60", "$70", "$70 and Above" ]
        combo3.grid(row=2, column=1, pady=10)        

        searchButton = tk.Button(self ,text= "Search", height=5, width=20, font = "Calibri 18 bold", command=command)
        searchButton.grid(row=3, columnspan=2, pady=10)

        self.grid(row=0, column=0)
