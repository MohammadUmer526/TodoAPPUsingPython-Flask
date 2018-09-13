from flask import Flask, render_template, request, url_for, redirect
import os
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
'sqlite:///' + os.path.join(basedir, 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    descp = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    return render_template('index.html', incomplete = incomplete, complete = complete)

@app.route('/add', methods=['POST'])
def add():
    todo = Todo(descp=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/complete/<id>')
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)
