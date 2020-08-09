from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

import os
from datetime import datetime 



basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todoDatabase.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

user = {
	"user":'vighnesh',
	"password":generate_password_hash('password', method='sha256')
}

def login_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if auth and auth.username == user['user'] and check_password_hash(user['password'], auth.password):
			return f(*args, **kwargs)

		return jsonify({'message' : 'login required '})
		

	return decorated



class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	task = db.Column(db.String(100), unique=True)
	completed = db.Column(db.Boolean)
	date_added = db.Column(db.DateTime,nullable=False,default=datetime.now)



# Login
@app.route('/login')		
def login():
	auth = request.authorization
    
	if auth and auth.username == user['user'] and check_password_hash(user['password'], auth.password):
		return jsonify({'message' : 'Login Successful'})

	return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


# Add New Todo
@app.route('/todo', methods=['POST'])	
@login_required	
def add_one():

	task = request.json['task']
	completed = request.json['completed']
	# date_added = request.json['date_added']
	todo = Todo(task=task,completed=completed)

	db.session.add(todo)
	db.session.commit()

	todos_json = {}
	todos_json['task'] = task
	todos_json['completed'] = completed
	todos_json['date_added'] = datetime.now()
	return jsonify(todos_json)

# Get All Todos
@app.route('/todo', methods=['GET'])
def get_all():
	list_of_todos = Todo.query.all()
	if not list_of_todos:
	    return jsonify({'message' : 'There are no Todos in Database'})


	output = []
	for todo in list_of_todos:
		todos_json = {}
		todos_json['task'] = todo.task
		todos_json['completed'] = todo.completed
		todos_json['date_added'] = todo.date_added
		output.append(todos_json)
	return jsonify({"todos": output})

# Get Single Todo
@app.route('/todo/<id>', methods=['GET'])
@login_required
def get_one(id):
	# todo = Todo.query.get(id)
	todo = Todo.query.filter_by(id=id).first()

	if not todo:
	    return jsonify({'message' : 'No todo found!'})

	todos_json = {}
	todos_json['task'] = todo.task
	todos_json['completed'] = todo.completed
	todos_json['date_added'] = todo.date_added
	return jsonify(todos_json)

# Update  Todo
@app.route('/todo/<id>', methods=['PUT'])
@login_required
def update_one(id):
	# todo = Todo.query.get(id)
	todo = Todo.query.filter_by(id=id).first()

	if not todo:
	    return jsonify({'message' : 'No todo found!'})


	task = request.json['task']
	completed = request.json['completed']

	todo.task = task
	todo.completed = completed

	db.session.commit()
	todos_json = {}
	todos_json['task'] = todo.task
	todos_json['completed'] = todo.completed
	todos_json['date_added'] = todo.date_added
	return jsonify(todos_json)


# Delete Todo
@app.route('/todo/<id>', methods=['DELETE'])
@login_required
def delete_one(id):
	todo = Todo.query.filter_by(id=id).first()

	if not todo:
	    return jsonify({'message' : 'No todo found!'})

	db.session.delete(todo)
	db.session.commit()

	return jsonify({'message' : 'todo is deleted.'})

if __name__ == '__main__':
  app.run(debug=True)