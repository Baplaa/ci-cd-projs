import sqlite3

conn = sqlite3.connect('points.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE point
          (id INTEGER PRIMARY KEY ASC, 
           x INTEGER NOT NULL,
           y INTEGER NOT NULL)
          ''')

conn.commit()
conn.close()
