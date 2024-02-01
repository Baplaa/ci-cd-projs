import sqlite3

conn = sqlite3.connect('carlot.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE IF NOT EXISTS cars
          (id INTEGER PRIMARY KEY ASC,
           timestamp DATETIME NOT NULL,
           make VARCHAR(250) NOT NULL,
           model VARCHAR(250) NOT NULL,           
           year INTEGER NOT NULL,
           price REAL NOT NULL
          )
          ''')

conn.commit()
conn.close()
