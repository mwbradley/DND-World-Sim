import sqlite3

conn = sqlite3.connect("matesia.db", check_same_thread=False)
conn.row_factory = sqlite3.Row  # lets you access columns by name like a dict
cursor = conn.cursor()

cursor.execute("SELECT * FROM economy")
economies = [dict(row) for row in cursor.fetchall()]

for c in economies:
    print(c)
