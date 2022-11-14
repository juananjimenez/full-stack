from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


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
    completado = db.Column(db.Boolean, nullable=False, default= False)
    
def __repr__(self):
    return f'<Todo ID: {self.id}, descripcion: {self.descripcion}>'

@app.route('/todos/create', methods=['Post'])
def create_todo():
    descripcion = request.data.get('descripcion', '')
    todo = Todo(descripcion=descripcion)
    db.session.add(todo)
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
    

