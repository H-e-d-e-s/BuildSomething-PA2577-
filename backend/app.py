from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.config["MONGO_URI"] = "mongodb://mongodb-service:27017/todo_db"
mongo = PyMongo(app)
db = mongo.db.todos

logger.info(f"Configured MongoDB URI: {app.config['MONGO_URI']}")

@app.route('/todos', methods=['GET'])
def get_all_todos():
    logger.info("Fetching all todos.")
    todos = []
    for todo in db.find():
        todos.append({
            '_id': str(todo['_id']),
            'title': todo['title'],
            'description': todo['description']
        })
    return jsonify(todos), 200

@app.route('/todos/<id>', methods=['GET'])
def get_todo(id):
    todo = db.find_one({'_id': ObjectId(id)})
    if todo:
        return jsonify({
            '_id': str(todo['_id']),
            'title': todo['title'],
            'description': todo['description']
        }), 200
    else:
        return jsonify({'error': 'Not found'}), 404

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    logger.info(f"Adding todo: {data}")
    todo_id = db.insert_one({
        'title': data['title'],
        'description': data.get('description', '')
    }).inserted_id
    new_todo = db.find_one({'_id': todo_id})
    return jsonify({
        '_id': str(new_todo['_id']),
        'title': new_todo['title'],
        'description': new_todo['description']
    }), 201

@app.route('/todos/<id>', methods=['PUT'])
def update_todo(id):
    data = request.get_json()
    updated = db.update_one(
        {'_id': ObjectId(id)},
        {'$set': {
            'title': data['title'],
            'description': data.get('description', '')
        }}
    )
    if updated.matched_count:
        todo = db.find_one({'_id': ObjectId(id)})
        return jsonify({
            '_id': str(todo['_id']),
            'title': todo['title'],
            'description': todo['description']
        }), 200
    else:
        return jsonify({'error': 'Not found'}), 404

@app.route('/todos/<id>', methods=['DELETE'])
def delete_todo(id):
    logger.info(f"Deleting todo with ID: {id}")
    deleted = db.delete_one({'_id': ObjectId(id)})
    if deleted.deleted_count:
        return jsonify({'message': 'Deleted'}), 200
    else:
        return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)