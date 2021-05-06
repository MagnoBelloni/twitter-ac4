from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///twitter"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(50))
    email = db.Column(db.String(60), unique=True)

    def login(self):
        return self.query.filter_by(username=self.username, password=self.password).first()


db.create_all()

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        usuario = User(username=username, password=password)
        login_correto = usuario.login()

        if(login_correto):
            return render_template("home.html")
        else:
            flash('Login incorreto!')
            return render_template("login.html")
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")

if __name__== "__main__":
    # executa a aplicação
    app.run(debug=True)