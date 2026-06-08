from db import get_db


def init_db():
  conn = get_db()
  cur = conn.cursor()

  cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL
    )
  """)

  cur.execute("""
    CREATE TABLE IF NOT EXISTS posts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      content TEXT NOT NULL,
      user_id INTEGER NOT NULL,
      FOREIGN KEY (user_id)
        REFERENCES users(id)
    )
  """)
  
  conn.commit()
  conn.close()

if __name__ == "__main__":
  init_db()