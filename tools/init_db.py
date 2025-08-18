import sqlite3, pathlib

db_file = "bnb.sqlite3"
schema = pathlib.Path("data/schema.sql").read_text(encoding="utf-8")

conn = sqlite3.connect(db_file)
conn.executescript(schema)
conn.commit()
conn.close()
print("Database initialized:", db_file)
