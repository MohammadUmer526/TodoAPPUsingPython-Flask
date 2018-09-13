from flask import Flask, render_template, request, url_for, redirect
import os
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \        # create a db "todo.db"
'sqlite:///' + os.path.join(basedir, 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)   

class Todo(db.Model):    #create class 'TODO' to stores the values(id, decp and status of complete/incomplete)
    id = db.Column(db.INTEGER, primary_key=True)
    descp = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

@app.route('/') 
def index():  # method for html file
    incomplete = Todo.query.filter_by(complete=False).all()  # for incomplete items and create flag = False for complete
    complete = Todo.query.filter_by(complete=True).all()
    return render_template('index.html', incomplete = incomplete, complete = complete)

@app.route('/add', methods=['POST'])
def add():   # method for adding todo items in list
    todo = Todo(descp=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/complete/<id>')
def complete(id): # for id of a individual items in order to mark as 'complete'
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)
