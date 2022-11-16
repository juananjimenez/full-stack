from flask import Flask, request, render_template, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:abc@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    db.init_app(app)
    #db.create_all()

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    descripcion= db.Column(db.String(), nullable=False)
    completado = db.Column(db.Boolean, nullable=True, default= False)
    
def __repr__(self):
    return f'<Todo ID: {self.id}, descripcion: {self.descripcion}>'

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())

@app.route('/todos/create', methods=['Post'])
def create_todo():
    body={}
    error = False
    try:
        descripcion  = request.get_json()['descripcion']
        todo = Todo(descripcion = descripcion)
        body['descripcion'] = todo.descripcion
        db.session.add(todo)
        db.session.commit()
    except:
        error == True
        db.session.rollback()
        print(sys.exec_info())
    finally:
        db.session.close()
        if error == True:
            abort(400)
        else:
            return jsonify(body)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    

