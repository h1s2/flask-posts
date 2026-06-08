from flask import Flask, render_template, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/posts", methods=["GET"])
def get_posts():
  conn = get_db()
  cur = conn.cursor()

  cur.execute("SELECT * FROM posts")

  posts = cur.fetchall()
  conn.close()

  result = []

  for post in posts:
    result.append({
      "id": post["id"],
      "content": post["content"],
      "user_id": post["user_id"]
    })
  
  return jsonify(result)

@app.route("/posts", methods=["POST"])
def create_post():
  if not session.get("user_id"):
    return jsonify({"message": "login required"}), 401

  data = request.get_json()

  content = data.get("content")
  user_id = session.get("user_id")

  if not content:
    return jsonify({"message": "content is required"}), 400

  conn = get_db()
  cur = conn.cursor()

  cur.execute(
    "INSERT INTO posts (content, user_id) VALUES (?, ?)",
    (content, user_id)
  )
  
  conn.commit()
  conn.close()

  return jsonify({"message": "post created"}), 201

@app.route("/posts/<int:post_id>", methods=["PATCH"])
def update_post(post_id):
  if not session.get("user_id"):
    return jsonify({"message": "login required"}), 401

  data = request.get_json()

  content = data.get("content")

  if not content:
    return jsonify({"message": "content is required"}), 400

  conn = get_db()
  cur = conn.cursor()

  cur.execute(
    "SELECT * FROM posts WHERE id = ?",
    (post_id,)
  )

  post = cur.fetchone()

  if post is None:
    conn.close()
    return jsonify({"message": "post not found"}), 404

  if post["user_id"] != session.get("user_id"):
    conn.close()
    return jsonify({"message": "forbidden"}), 403

  cur.execute(
    "UPDATE posts SET content = ? WHERE id = ?",
    (content, post_id)
  )

  conn.commit()
  conn.close()

  return jsonify({"message": "post updated"})

@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
  if not session.get("user_id"):
    return jsonify({"message": "login required"}), 401

  conn = get_db()
  cur = conn.cursor()

  cur.execute(
    "SELECT * FROM posts WHERE id = ?",
    (post_id,)
  )

  post = cur.fetchone()

  if post is None:
    conn.close()
    return jsonify({"message": "post not found"}), 404

  if post["user_id"] != session.get("user_id"):
    conn.close()
    return jsonify({"message": "forbidden"}), 403

  cur.execute(
    "DELETE FROM posts WHERE id = ?",
    (post_id,)
  )

  conn.commit()
  conn.close()

  return jsonify({"message": "post deleted"})


@app.route("/signup", methods=["POST"])
def signup():
  data = request.get_json()

  username = data.get("username")
  password = data.get("password")

  if not username or not password:
    return jsonify({"message": "username and password required"}), 400

  password_hash = generate_password_hash(password)

  conn = get_db()
  cur = conn.cursor()

  try:
    cur.execute(
    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
    (username, password_hash)
    )
    conn.commit()
  except sqlite3.IntegrityError:
    return jsonify({"message": "username already exists"}), 400
  finally:
    conn.close()

  return jsonify({"message": "signup success"}), 201

@app.route("/login", methods=["POST"])
def login():
  if "user_id" in session:
    return jsonify({"message": "already logged in"}), 400

  data = request.get_json()

  username = data.get("username")
  password = data.get("password")

  if not username or not password:
    return jsonify({"message": "username and password required"}), 400
  
  conn = get_db()
  cur = conn.cursor()

  cur.execute(
    "SELECT * FROM users WHERE username = ?",
    (username,)
  )

  user = cur.fetchone()
  conn.close()

  if user is None:
    return jsonify({"message": "invalid username or password"}), 401

  if not check_password_hash(user["password_hash"], password):
    return jsonify({"message": "invalid username or password"}), 401

  session["user_id"] = user["id"]

  return jsonify({"message": "login success"})

@app.route("/logout", methods=["POST"])
def logout():
  if "user_id" not in session:
    return jsonify({"message": "login required"}), 401

  session.pop("user_id", None)

  return jsonify({"message": "logout success"})

@app.route("/me", methods=["GET"])
def me():
  if "user_id" in session:
    return jsonify({"loggedIn": True})
  
  return jsonify({"loggedIn": False})


if __name__ == "__main__":
  app.run(debug=True)