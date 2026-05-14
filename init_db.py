from db import get_db


def init_db():
  conn = get_db()
  cur = conn.cursor()

  cur.execute("""
    CREATE TABLE IF NOT EXISTS posts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      content TEXT
    )
  """)
  
  conn.commit()
  conn.close()

if __name__ == "__main__":
  init_db()