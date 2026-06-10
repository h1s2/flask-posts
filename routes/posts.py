from flask import Blueprint, request, jsonify, session
from db import get_db

posts_bp = Blueprint("posts", __name__)

def is_blank(value):
  return not value or not value.strip()

@posts_bp.route("/posts", methods=["GET"])
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

@posts_bp.route("/posts", methods=["POST"])
def create_post():
  if not session.get("user_id"):
    return jsonify({"message": "login required"}), 401

  data = request.get_json()

  content = data.get("content")
  user_id = session.get("user_id")

  if is_blank(content):
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

@posts_bp.route("/posts/<int:post_id>", methods=["PATCH"])
def update_post(post_id):
  if not session.get("user_id"):
    return jsonify({"message": "login required"}), 401

  data = request.get_json()

  content = data.get("content")

  if is_blank(content):
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

@posts_bp.route("/posts/<int:post_id>", methods=["DELETE"])
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

