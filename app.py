from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abc@localhost:5432/todoapp'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  descripcion = db.Column(db.String(), nullable=False)
  completado = db.Column(db.Boolean, nullable=False, default=False)
  list_id = db.Column(db.Integer, db.ForeignKey('todolist.id'), nullable=False)

def __repr__(self):
  return f'<Todo {self.id} {self.descripcion}, list {self.list_id}>'

class TodoList(db.Model):
  __tablename__ = 'todolist' 
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  todos = db.relationship('Todo', backref='list', lazy=True)
  
def __repr__(self):
    return f'<TodoList {self.id} {self.name}>'
  

# note: more conventionally, we would write a
# POST endpoint to /todos for the create endpoint:
# @app.route('/todos', method=['POST'])
@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try: 
    descripcion = request.get_json()['descripcion']
    todo = Todo(descripcion=descripcion, completed=False)
    db.session.add(todo)
    db.session.commit()
    body['id'] = todo.id
    body['completado'] = todo.completado
    body['descripcion'] = todo.descripcion
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
  try:
    completado = request.get_json()['completado']
    print('completado', completado)
    todo = Todo.query.get(todo_id)
    todo.completado = completado
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
  try:
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({'success': True})


@app.route('/')
def index():
  return render_template('index.html', todo=Todo.query.order_by('id').all())


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5000)