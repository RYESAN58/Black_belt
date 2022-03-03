from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.liked import Liked
from flask_app.models.show import Show


@app.route('/make')
def report():
    x = session['user']
    y = session['name']
    return render_template('shows.html', x = x , name = y )

###################################################################################


@app.route('/add_site', methods = ['POST'])
def add():
    data = {
        'title' : request.form['title'],
        'network' : request.form['network'],
        'release' : request.form['release'],
        'description': request.form['description'],
        'user_id': request.form['user_id'],
    }
    if not Show.validate(request.form):
        return redirect('/make')
    Show.create(data)
    num = session['user']
    return redirect(f'/dashboard/{num}')

###################################################################

@app.route('/see/<int:num>')
def see(num):
    data = {'id': num}
    y = Show.get_join(data)
    total_likes = Liked.total_likes(data)
    print(total_likes)
    name = session['name']
    x = session['user']
    return render_template("site.html", it = y, name = name, x = x, total_likes = total_likes)

################################################################################################

@app.route('/del/<int:num>')
def get_rid(num):
    data = {'id' : num}
    Show.delete(data)
    x = session['user']
    return redirect(f'/dashboard/{x}')


############################################################################################

@app.route('/edit/<int:num>')
def update(num):
    data = {'id' : num}
    edit = Show.retrieve_by(data)

    return render_template('update.html' , name =  session['name'], update = edit, x = session['user'], y = num)


#######################################################################################################################


@app.route('/update_rec', methods =['POST'])
def edit():
    data = {
        'title' : request.form['title'],
        'network' : request.form['network'],
        'release' : request.form['release'],
        'description': request.form['description'],
        'id':  request.form['id']
    }
    if not Show.validate(request.form):
        x = session['user']
        return redirect(f"/edit/{request.form['id']}")
    Show.update(data)
    x = session['user']
    return redirect(f'dashboard/{x}')




###########################################################################################################################

@app.route('/like/<int:num1>/<int:num2>')
def like(num1, num2):
    data = {
        'show_id' : num1,
        'user_id' : num2
    }
    Liked.like(data)
    x = session['user']
    return redirect(f"dashboard/{x}")


################################################################################################
@app.route('/delete/<int:num1>/<int:num2>')
def unlike(num1,num2):
    data = {
        'user_id': num2,
        'show_id': num1
    }
    Liked.unlike(data)
    x = session['user']
    return redirect(f'/dashboard/{x}')