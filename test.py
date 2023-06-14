from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:laspi@localhost:5432/contact"

db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    numero = db.Column(db.Integer)


@app.route("/")
def index():
    return render_template("index.html")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5008)
