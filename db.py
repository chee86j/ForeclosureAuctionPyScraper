import sqlite3

def create_connection():
    conn = sqlite3.connect('auctions.db')
    return conn

def create_table(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS auctions
                 (title TEXT, price TEXT)''')
    conn.commit()

def insert_auction(conn, item):
    conn.execute('INSERT INTO auctions (title, price) VALUES (?, ?)', (item['title'], item['price']))
    conn.commit()

def main():
    conn = create_connection()
    create_table(conn)
    # Temporary insertion to be called after scraping and parsing
    insert_auction(conn, {'title': 'Example Title', 'price': '1000'})

if __name__ == '__main__':
    main()
