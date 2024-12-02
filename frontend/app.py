from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

API_URL = 'http://backend-service:5000/todos'

@app.route('/')
def index():
    response = requests.get(API_URL)
    todos = response.json()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form['title']
    description = request.form['description']
    requests.post(API_URL, json={'title': title, 'description': description})
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete_todo(id):
    requests.delete(f"{API_URL}/{id}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
