from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pendencias.sqlite3"

db = SQLAlchemy(app)

class Pendencias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer)
    descricao = db.Column(db.String(100))
    status = db.Column(db.String(50))
    dataInclusao = db.Column(db.Date, default=datetime.date)
    dataFinalizacao = db.Column(db.Date)

    def __init__(self, numero, descricao, status, dataInclusao, dataFinalizacao):
        self.numero = numero
        self.descricao = descricao
        self.status = status
        self.dataInclusao = dataInclusao
        self.dataFinalizacao = dataFinalizacao

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/pendencias")
def lista_pendencias():
    pendencias=Pendencias.query.all()
    print(pendencias)
    return render_template("pendencias.html", pendencias=Pendencias.query.all())

@app.route("/nova_pendencia", methods=["POST","GET"])
def nova_pendencia():
    numero = request.form.get("numero")
    descricao = request.form.get("descricao")
    status = request.form.get("status")
    dataInclusao = datetime.today()

    #dataFinalizada = None if status != "Finalizada" else datetime.today()
   
    

    if request.method == "POST":
        pendencia = Pendencias(int(numero), descricao, status, dataInclusao, None)
        db.session.add(pendencia)
        db.session.commit()
        return redirect(url_for("lista_pendencias"))


    return render_template("adicionar.html")

@app.route("/<int:id>/atualiza_pendencia", methods=["POST", "GET"])
def atualiza_pendencia(id):
    pendencia = Pendencias.query.filter_by(id=id).first()

    if request.method == "POST":
        numero = request.form.get("numero")
        descricao = request.form.get("descricao")
        status = request.form.get("status")
        dataFinalizada = None if status != "Finalizada" else datetime.today()
        Pendencias.query.filter_by(id=id).update({"numero":numero, "descricao":descricao, "status": status, "dataFinalizacao": dataFinalizada})
        db.session.commit()
        return redirect(url_for("lista_pendencias"))        
    
    return render_template("atualiza_pendencia.html", pendencia= pendencia)

@app.route("/<int:id>/remove_pendencia")
def remove_pendencia(id):
    pendencia = Pendencias.query.filter_by(id=id).first()
    db.session.delete(pendencia)
    db.session.commit()
    return redirect(url_for("lista_pendencias"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)