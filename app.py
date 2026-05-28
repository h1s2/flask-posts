from flask import Flask, render_template, request, jsonify
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

  cur.execute("DELETE FROM posts WHERE id = ?", (post_id,))
  conn.commit()
  conn.close()

  return jsonify({"message": "post delete"})

if __name__ == "__main__":
  app.run(debug=True)