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

  conn = get_db()
  cur = conn.cursor()

  cur.execute(
    "INSERT INTO posts (content) VALUES (?)",
    (content,)
  )
  
  conn.commit()
  conn.close()

  return jsonify({"message": "post created"})

if __name__ == "__main__":
  app.run(debug=True)