from re import L
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.show import Show
from flask_app.models.liked import Liked

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    session['user'] = 0
    return render_template('index.html')
@app.route('/create_user', methods= ['POST'])
def created():

    if not User.validate(request.form):
        return redirect('/')
        
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    

    data = {
        'firstname' : request.form['firstname'],
        'lastname' : request.form['lastname'],
        'email' : request.form['email'],
        'password': pw_hash
    }


    x = {'email':request.form['email']}
    checker = User.verify_email(x)
    if checker == False:
        return redirect('/')

    else:
        y = User.create(data)
        flash('Succesfully Added in database', 'success')
        return redirect('/')


########################################################################


@app.route('/login', methods = ['POST'])
def logger():
    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password", 'login')
        return redirect("/")
    

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Must Enter Password", 'login')
        return redirect('/')
    if len(request.form['password']) < 1:
        flash('must enter passoword')
        return redirect('/')
    session['user'] = user_in_db.id
    session['name'] = f"{user_in_db.firstname} {user_in_db.lastname}"
    x = session['user']
    return redirect(f'/dashboard/{x}')

#############################################################################

@app.route('/dashboard/<int:num>/')
def home(num):
    if session['user'] != num:
        return redirect('/')
    x = num
    y = session['name']
    alls = Show.get_all_shows()
    data = {'id' : num}
    liked_by = Liked.liked_by(data)
    liked_list = []
    print(liked_by)
    for i in liked_by:
        liked_list.append(i['show_id'])
    print(liked_list)
    return render_template('home.html',y= y, all = alls, id = x, liked_by = liked_list)

@app.route('/like/<int:num2>/dashboard/<int:num>/')
def home2(num, num2):
    if session['user'] != num:
        return redirect('/')
    x = num
    y = session['name']
    alls = Show.get_all_shows()
    data = {'id' : num}
    liked_by = Liked.liked_by(data)
    liked_list = []
    for i in liked_by:
        liked_list.append(i['show_id'])
    print(liked_list)
    return render_template('home.html',y= y, all = alls, id = x, liked_by = liked_list)