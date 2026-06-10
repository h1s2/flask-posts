from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db
import sqlite3

auth_bp = Blueprint("auth", __name__)

def is_blank(value):
  return not value or not value.strip()

@auth_bp.route("/signup", methods=["POST"])
def signup():
  data = request.get_json()

  username = data.get("username")
  password = data.get("password")

  if is_blank(username):
    return jsonify({"message": "username and password required"}), 400

  if is_blank(password):
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

@auth_bp.route("/login", methods=["POST"])
def login():
  if "user_id" in session:
    return jsonify({"message": "already logged in"}), 400

  data = request.get_json()

  username = data.get("username")
  password = data.get("password")

  if is_blank(username):
    return jsonify({"message": "username and password required"}), 400

  if is_blank(password):
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

@auth_bp.route("/logout", methods=["POST"])
def logout():
  if "user_id" not in session:
    return jsonify({"message": "login required"}), 401

  session.pop("user_id", None)

  return jsonify({"message": "logout success"})

@auth_bp.route("/me", methods=["GET"])
def me():
  if "user_id" in session:
    return jsonify({"loggedIn": True})
  
  return jsonify({"loggedIn": False})

