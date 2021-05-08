from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///twitter.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'chave secreta @$%&'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(50))
    email = db.Column(db.String(60))

    def login(self):
        return self.query.filter_by(username=self.username, password=self.password).first()

    def cadastrar(self):
        db.session.add(self)
        db.session.commit()

    def buscar_por_username(self):
        return self.query.filter_by(username=self.username).first()

    def buscar_por_id(self):
        return self.query.get(self.id)

    def buscar_followers(self):
        return self.query.join(Follow, Follow.id_follower == User.id).filter(Follow.id_user == self.id)

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer)
    id_follower = db.Column(db.Integer)

db.create_all()

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        usuario = User(username=username, password=password)
        login_correto = usuario.login()

        if(login_correto):
            session["user"] = login_correto.id
            return redirect("/home")
        else:
            flash('Login incorreto!')
            return render_template("login.html")
    return render_template("login.html")


@app.route("/cadastrar", methods=['GET', 'POST'])
def cadastrar_usuario():
        if request.method == 'POST':
            username = request.form["username"]
            password = request.form["password"]
            name = request.form["name"]
            email = request.form["email"]
            usuario = User(username=username, password=password, name=name, email=email)
            username_em_uso = usuario.buscar_por_username()
            if(username_em_uso):
                flash('Usuário já está em uso!')
                return render_template("cadastrar.html")
            usuario.cadastrar()
            return render_template("login.html")
        return render_template("cadastrar.html")
    

@app.route("/sair")
def sair():
    session["user"] = ""
    return redirect("/")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/followers")
def followers():
    id_user = session['user']

    usuario = User(id=id_user)
    followers = usuario.buscar_followers()

    return render_template("followers.html", followers=followers)


if __name__== "__main__":
    app.run(debug=True)