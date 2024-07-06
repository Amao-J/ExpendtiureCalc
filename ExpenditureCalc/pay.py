import sqlite3
import os
from datetime import datetime

class Pay:
    def __init__(self, db_name="items.db", start_new_session=False):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        
        if start_new_session:
            self._create_table()
            self._create_new_file()
        else:
            self._check_existing_session()
    
    def _create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS items (
                            id INTEGER PRIMARY KEY,
                            item TEXT,
                            category TEXT,
                            price REAL
                            )''')
        self.conn.commit()
    
    def _check_existing_session(self):
        # Check if there are any existing items in the database
        self.cur.execute("SELECT COUNT(*) FROM items")
        count = self.cur.fetchone()[0]
        if count == 0:
            self._create_table()
            self._create_new_file()
        else:
            print("Existing session found. Adding items to previous session.")
    
    def _create_new_file(self):
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = os.path.join(os.getcwd(), f"added_items_{current_datetime}.txt")
    
    def clearSession(self):
        # Clear all items from the current session
        self.cur.execute("DELETE FROM items")
        self.conn.commit()
        self._create_new_file()
        print("Session cleared. Starting new list.")
    
    def addItem(self, item, category):
        self.cur.execute("INSERT INTO items (item, category, price) VALUES (?, ?, NULL)", (item, category))
        self.conn.commit()
    
    def addPrice(self, item, price):
        self.cur.execute("UPDATE items SET price = ? WHERE item = ?", (price, item))
        self.conn.commit()
    
    def updateCategory(self, item, new_category):
        self.cur.execute("UPDATE items SET category = ? WHERE item = ?", (new_category, item))
        self.conn.commit()
    
    def deleteItem(self, item):
        self.cur.execute("DELETE FROM items WHERE item = ?", (item,))
        self.conn.commit()
    
    def getItemsByCategory(self, category):
        self.cur.execute("SELECT item, price FROM items WHERE category = ?", (category,))
        return self.cur.fetchall()
    
    def expenditures(self):
        self.cur.execute("SELECT item, category, price FROM items")
        rows = self.cur.fetchall()
        items = {}
        for row in rows:
            items[row[0]] = {'category': row[1], 'price': row[2]}
        return items
    
    def calculateTotal(self):
        self.cur.execute("SELECT SUM(price) FROM items WHERE price IS NOT NULL")
        total = self.cur.fetchone()[0]
        return total if total else 0.0
    
    def printAddedItemsToFile(self):
        with open(self.filename, 'w') as f:
            f.write(f"Added Items - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            items = self.expenditures()
            for item, details in items.items():
                f.write(f"Item: {item}, Category: {details['category']}, Price: {details['price']}\n")
            total = self.calculateTotal()
            f.write(f"\nTotal Expenditure: {total}\n")
            
        print(f"Added items and total expenditure have been saved to {self.filename}")
    
    def close(self):
        self.conn.close()
