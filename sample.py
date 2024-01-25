import sqlite3

conn = sqlite3.connect('instance/books.db')
cursor = conn.cursor()

# conn.execute("INSERT INTO book VALUES (1, 'NCERT', 'Govt', 12233, 150, 2)")

# Fetch all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

conn.close()
