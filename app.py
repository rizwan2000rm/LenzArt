from flask import Flask, render_template, request, url_for, redirect, session

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class posts(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)

    name = db.Column("name", db.String(100), nullable=False)

    email = db.Column("email", db.String(100), unique=True, nullable=False)

    img = db.Column("img", db.String(1000))

    sensor = db.Column("sensor", db.String(10))

    camera = db.Column("camera", db.String(10))

    def __init__(self, name, email, img, sensor, camera):
        self.name = name
        self.email = email
        self.img = img
        self.sensor = sensor
        self.camera = camera


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/form", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        post = posts(
            name=request.form["name"], email=request.form["email"], img=request.form["img"], sensor=request.form["sensor"], camera=request.form["camera"])
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("showcase"))
    else:
        return render_template("form.html")


@app.route("/showcase")
def showcase():
    return render_template("showcase.html", posts=posts.query.all())


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
