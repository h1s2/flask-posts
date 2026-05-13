import sqlite3

def get_db():
  conn = sqlite3.connect("app.db")
  conn.row_factory = sqlite3.Row
  return conn

def init_db():
  conn = get_db()
  cur = conn.cursor()
  cur.execute("""
    CREATE TABLE IF NOT EXISTS posts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      post TEXT
    )
  """)
  conn.commit()
  conn.close()

if __name__ == "__main__":
  init_db()