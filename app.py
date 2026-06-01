from flask import Flask, render_template, request, jsonify
from werkzeug.security import generate_password_hash
from db import get_db


app = Flask(__name__)

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
      "content": post["content"]
    })
  
  return jsonify(result)

@app.route("/posts", methods=["POST"])
def create_post():
  
  data = request.get_json()

  content = data.get("content")

  if not content:
    return jsonify({"message": "content is required"}), 400

  conn = get_db()
  cur = conn.cursor()

  cur.execute(
    "INSERT INTO posts (content) VALUES (?)",
    (content,)
  )
  
  conn.commit()
  conn.close()

  return jsonify({"message": "post created"})

@app.route("/posts/<int:post_id>", methods=["PATCH"])
def update_post(post_id):
  data = request.get_json()
  content = data.get("content")

  if not content:
    return jsonify({"message": "content is required"}), 400

  conn = get_db()
  cur = conn.cursor()

  cur.execute(
    "SELECT id FROM posts WHERE id = ?",
    (post_id,)
  )

  post = cur.fetchone()

  if post is None:
    conn.close()
    return jsonify({"message": "post not found"}), 404

  cur.execute(
    "UPDATE posts SET content = ? WHERE id = ?",
    (content, post_id)
  )

  conn.commit()
  conn.close()

  return jsonify({"message": "post updated"})

@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
  conn = get_db()
  cur = conn.cursor()

  cur.execute(
    "SELECT id FROM posts WHERE id = ?",
    (post_id,)
  )

  post = cur.fetchone()

  if post is None:
    conn.close()
    return jsonify({"message": "post not found"}), 404

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
  except:
    return jsonify({"message": "username already exists"}), 400
  finally:
    conn.close()

  return jsonify({"message": "signup success"}), 201



if __name__ == "__main__":
  app.run(debug=True)