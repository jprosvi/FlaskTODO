from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
import socket

# Define flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mystring'

# Connect to MongoDB
client = MongoClient(os.environ['APP_URI'])
db = client['mydb']
collection = db['mycol']

#Hostname and IP
myhost = socket.gethostname()
myip = socket.gethostbyname(myhost)


# Class Form
class myform(FlaskForm):
     input_todo = StringField("Todo:", validators=[DataRequired()])
     input_description = StringField(" Todo Description", validators=[DataRequired()])
     submit_btn = SubmitField("Add Todo")

@app.route('/')
def index():
    items = collection.find()
    form_in_index = myform()
    return render_template('index.html', items=items,todo_form=form_in_index)


@app.route('/add', methods=['GET','POST'])
def add_item():
    form_in_add = myform()
    todo_name = form_in_add.input_todo.data
    todo_desc = form_in_add.input_description.data
    if todo_name and todo_desc:
        collection.insert_one({'name': todo_name, 'description': todo_desc})
    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete_item():
    item_name = request.form.get('mydelete')
    if item_name:
        collection.delete_one({'name': item_name})
    return redirect(url_for('index'))

@app.route('/about')
def about():
     return render_template('about.html', myhost=myhost, myip=myip)

if __name__ == '__main__':
	from waitress import serve
	serve(app, host='0.0.0.0', port=5000)
