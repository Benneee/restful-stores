import sqlite3


class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return { 'name': self.name, 'price': self.price }

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('app.db')
        cursor = connection.cursor()

        get_query = "SELECT * FROM items WHERE name=?"
        results = cursor.execute(get_query, (name,))
        row = results.fetchone()

        connection.close()

        if row:
            return cls(*row)
    
    def insert_item(self):
        connection = sqlite3.connect('app.db')
        cursor = connection.cursor()

        create_query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(create_query, (self.name, self.price))

        connection.commit()
        connection.close()

    def update_item(self):
        connection = sqlite3.connect('app.db')
        cursor = connection.cursor()

        update_query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(update_query, (self.name, self.price)) # The items in the tuple have to be in the order of their appearance in the query above

        connection.commit()
        connection.close()