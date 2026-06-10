from flask import Flask, render_template
from routes.auth import auth_bp
from routes.posts import posts_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(auth_bp)
app.register_blueprint(posts_bp)

@app.route("/")
def home():
  return render_template("index.html")

if __name__ == "__main__":
  app.run(debug=True)