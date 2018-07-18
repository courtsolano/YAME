# Code adapted from https://pythonspot.com/flask-web-forms/

import os, sys
import datetime
import pymongo
import numpy as np
from flask import Flask, render_template, flash, request
from wtforms import Form, SelectField, TextField, TextAreaField, validators, StringField, SubmitField

#importing and using files from the db folder
sys.path.append('../db')
import retrieve_from_db, add_person, edit_person

# App config.
DEBUG = True
app = Flask(__name__)

app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

UPLOAD_FOLDER = 'static/imj'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def checkbox(id):
    try:
        value = request.form[id]
        value = 1
    except:
        value = 0
    return value

def image(img, newname):
    if img:
        f = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
        n = os.path.join(app.config['UPLOAD_FOLDER'], newname)
        img.save(f)
        os.rename(f, n)
        filename = newname
    # Use default photo
    else:
        filename = 'default.jpg'
    return filename

class ReusableForm(Form):
    name = TextField('Title: ', validators=[validators.required()])
    degree = TextField('Subtitle: ')
    occupation = TextField('Heading:')


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    print (form.errors)
    if request.method == 'POST':
        name = request.form['name'] # key value pairs
        degree = request.form['degree']
        occupation = request.form['occupation']
        icon = request.files['icon']
        image1 = request.files['image1']
        paragraph1 = request.form['paragraph1']
        image2 = request.files['image2']
        paragraph2 = request.form['paragraph2']
        image3 = request.files['image3']
        paragraph3 = request.form['paragraph3']
        hidden = checkbox('hidden')
        category = checkbox('category')
        # saving all images into folder and getting filenames
        icon_filename = image(icon, name + '_icon')
        image1_filename = image(image1, name + '_image1')
        image2_filename = image(image2, name + '_image2')
        image3_filename = image(image3, name + '_image3')

        if form.validate():
            add_person.addOne(name, degree, occupation, icon_filename, image1_filename, paragraph1, 
                image2_filename, paragraph2, image3_filename, paragraph3, hidden, category)
            print("Upload to database successful.")
        else:
            flash('The title field is required.')
    return render_template('hello.html', form=form)


@app.route("/people/", methods=['GET', 'POST'])
def people():
    personarr = retrieve_from_db.getAll() #returns all people in the database
    return render_template('people.html', people = personarr)


@app.route("/edit/", methods=['GET', 'POST'])
def edit():
    form = ReusableForm(request.form)
    name = request.args.get('name')
    person = retrieve_from_db.getOneforDisplay(name)
    if request.method == 'POST':
        name=request.form['name']
        degree=request.form['degree']
        school=request.form['school']
        year=request.form['year']
        ex = checkbox('ex')
        occupation=request.form['occupation']
        facts=request.form['facts']
        file = request.files['image']
        alt_txt = request.form['alt_txt']
        hidden = checkbox('hidden')
        if file:
            f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(f)
            filename = file.filename
        else:
            filename = person['image_name']
        if form.validate():
            flash(person['name'])
            edit_person.editOne(person['_id'], name, degree, school, ex, year, occupation, facts, filename, alt_txt, hidden)
            print("edit to database successful")
        else:
            flash('All the form fields are required.')
    return render_template('edit.html', person=person, form=form)


@app.route("/person/", methods=['GET', 'POST'])
def person():
    name = request.args.get('name')
    person = retrieve_from_db.getOneforDisplay(name)
    return render_template('person.html', person=person)


@app.route("/display/", methods=['GET', 'POST'])
def display():
    # name = request.args.get('name')
    # if name==None:
    #     personarr = retrieve_from_db.getAll()
    #     name = np.random.choice(personarr)
    # person = retrieve_from_db.getOneforDisplay(name)
    personarr = retrieve_from_db.getAllContent()
    return render_template('display.html', personarr=personarr) # person=person

@app.route("/search/", methods=['GET', 'POST'])
def search():
    form = ReusableForm(request.form)
    print (form.errors)
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    person = []
    toFind = {}
    if request.method == 'POST':
        try:
            letter = request.form['name']
            print (letter)
            person = retrieve_from_db.searchByLetter(letter)
        except:
            toFind['name'] = ''
        try:
            toFind['school'] = request.form['school']
            person = retrieve_from_db.getOne(toFind)
        except:
            toFind['school'] = ''
        try:
            toFind['year'] = request.form['year']
            person = retrieve_from_db.getOne(toFind)
        except:
            toFind['year'] = ''
    # person = retrieve_from_db.getOne(toFind)
    return render_template('search.html', form=form, person=person, alphabet=alphabet)
if __name__ == "__main__":
    app.run()
