from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['students']
collection = db['students']

@app.route('/')
def index():
    # retrieve all students from database
    students = db['students'].find()
    
    # calculate sum and average of marks for all students
    total_marks = 0
    count = 0
    for student in students:
        total_marks += int(student['marks'])
        count += 1
    avg_marks = total_marks / count if count > 0 else 0
    
    # render template with students, total marks and average marks
    return render_template('index.html', context=students, total_marks=total_marks, avg_marks=avg_marks)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # get student details from form
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        marks = request.form['marks']
        
        # insert student into database
        collection.insert_one({
            'name': name,
            'email': email,
            'phone': phone,
            'marks' : marks
        })
        
        # redirect to home page
        return redirect('/')
    else:
        return render_template('add.html')

@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = collection.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        # get updated student details from form
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        marks = request.form['marks']
        
        # update student in database
        collection.update_one({'_id': ObjectId(id)}, {'$set': {
            'name': name,
            'email': email,
            'phone': phone,
            'marks': marks
        }})
        
        # redirect to home page
        return redirect(url_for('index'))
    else:
        return render_template('edit.html', student=student)

@app.route('/delete/<string:id>', methods=['POST'])
def delete_student(id):
    # delete student from database
    collection.delete_one({'_id': ObjectId(id)})
    
    # redirect to home page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
