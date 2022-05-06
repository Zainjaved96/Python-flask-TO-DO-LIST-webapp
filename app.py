from tkinter.tix import Form
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template("index.html", Todos=allTodo)


@app.route("/delete/<int:sno>")
def delete(sno):
    record = Todo.query.filter_by(sno=sno).first()
    db.session.delete(record)
    db.session.commit()
    return redirect("/")


@app.route("/todo-list")
def TodoList():
    allTodo = Todo.query.all()
    return render_template("todo_list.html", Todos=allTodo)

@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    if request.method=="POST":
        title = request.form['title']
        description = request.form['description']
        record = Todo.query.filter_by(sno=sno).first()
        record.title = title
        record.description = description
        db.session.add(record)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)

    


if __name__ == "__main__":
    app.run(debug=True, port=8000)
