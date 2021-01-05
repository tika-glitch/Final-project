#Import everything
from flask import Flask, render_template, request
from cs50 import SQL
from functools import reduce
import csv
#Get access to flask and sql
app = Flask(__name__)
db = SQL("sqlite:///dogs.db")
#This is the homepage
@app.route("/")
def homepage():
    return render_template("homepage.html")

#This is the search page
@app.route("/search",methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html",show="yes")
    else:
        Input = request.form.get("search")
        input1 = Input.lower()
        dev = "%" + input1 + "%"
        found = db.execute("SELECT Breed_name, Intelligence_ranking, Description FROM dogs WHERE LOWER(Breed_name) LIKE :name;",name=dev)
        dog = []
        for i in range(len(found)):
            dictionary = found[i]
            name = dictionary.get("Breed_name", "")
            inte = dictionary.get("Intelligence_ranking", "")
            des = dictionary.get("Description", "")
            dog.append(name)
            dog.append(inte)
            dog.append(des)
        return render_template("search.html",show="no",dog = dog)


#This is the breed finding...
@app.route("/breed",methods=["GET", "POST"])
def breed():
    dogs = []
    if request.method=="GET":
        return render_template("breed.html",on="no")
    else:
        size = "none"
        fur = "none"
        family = "none"
        guard = "none"
        if 'submit_button' in request.form:
            size=request.form['Size']
        if 'submit_button' in request.form:
            sheds=request.form['Sheds']
        if 'submit_button' in request.form:
            family=request.form['Family']
        if 'submit_button' in request.form:
            guard=request.form['Guard']
        found = db.execute("SELECT Breed_name, Intelligence_ranking, Description FROM dogs WHERE Size=:size AND Sheds=:sheds AND Family_friendly=:family AND Guard=:guard;",size=size, sheds=sheds, family=family, guard=guard)
        dogs = []
        for i in range(len(found)):
            dictionary = found[i]
            name = dictionary.get("Breed_name", "")
            inte = dictionary.get("Intelligence_ranking", "")
            des = dictionary.get("Description", "")
            dogs.append(name)
            dogs.append(inte)
            dogs.append(des)
        return render_template("breed.html",on="yes",dogs = dogs)




        return render_template("breed.html", no="no", on="yes")
@app.route("/searched/<s>")
def searched(s):
    return render_template("searched.html",s=s)
#This is the info page
@app.route("/info/<i>")
def info(i):
    e = i
    return render_template("info.html",i=e)

#And this is the contact page.
@app.route("/Add",methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html",added = "no")
    else:
        breed_name = request.form.get("Breed_name")
        breed1 = breed_name.lower()
        intelligence_ranking = request.form.get("Intelligence_ranking")
        description = request.form.get("Description")
        size = request.form.get("Size")
        sheds = request.form.get("Sheds")
        family_friendly = request.form.get("Family_friendly")
        guard = request.form.get("Guard")
        found = db.execute("SELECT Breed_name FROM dogs WHERE LOWER(Breed_name) == :b",b=breed1)
        if len(found) == 0:
            db.execute("INSERT INTO dogs (Breed_name, Intelligence_ranking, Description, Size, Sheds, Family_friendly, Guard) VALUES (:b, :i, :d, :si, :sh, :f, :g)", b=breed_name, i=intelligence_ranking, d=description, si=size, sh=sheds, f=family_friendly, g=guard)
            return render_template("contact.html",added = "yes")
        else:
            
            return render_template("contact.html",added = "already")