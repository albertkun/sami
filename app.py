from flask import Flask, session,render_template,flash, redirect, request, url_for,jsonify,abort,make_response, Response, abort, redirect, flash,request
#bring in module for safe signing in unsecure environment
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
#bring in module for flask admin
from flask_admin import Admin
#bring in ORM called peewee
from flask_admin.contrib.peewee import ModelView
# from flask_peewee.admin import Admin
from flask_peewee.db import Database

#bring in modules
from models import *
import bcrypt
#bring in flask mail
from flask_mail import Mail, Message

from forms import NewUser
import operator
import sys


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config.from_object('config.EmailServer')

#bring in a timed serializer
s = URLSafeTimedSerializer(Config.KEY)

mail = Mail(app)

def get_serializer(secret_key=None):
    if secret_key is None:
        secret_key = app.secret_key
    return URLSafeTimedSerializer(secret_key)
    print URLSafeTimedSerializer(secret_key)

#this is for admin view...
admin = Admin(app, name='microblog', template_mode='bootstrap3')

#pip install pymysql
admin.add_view(ModelView(User))

#new user route
@app.route("/newuser/", methods=['GET', 'POST'])
def host():
    form = NewUser(request.form)
    if request.method == 'POST':
        user = User()
        for field in form:
            if field.name != 'csrf_token':
                print field.name
                theField = str(field.name)
                setattr(user,theField,field.data)
                #check the data from the form
                #print getattr(user,theField)
        username = request.form['username']
        email = request.form['email']
        sponsorname = request.form['groupname']
        passhash = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        #print passhash
        form.data['password'] = passhash
        setattr(user,'sponsor',sponsorname)
        # user.sponsor = sponsor 
        setattr(user,'password',passhash)
        #app.logger.info(form.data)
        #print getattr(user,theField)
        user.save()
        query = Sponsor.get(Sponsor.groupname == sponsorname)
        sponsorEmail = query.email
        print sponsorEmail
        userEmail = email
        #####  send the username to the verify email function, to send an email out##### 7/16/2018
        verifyemail(username,sponsorEmail,userEmail)
        return redirect(url_for('userlist'))
    elif request.method =='GET':
        groups = Sponsor.select(Sponsor.groupname)
        return render_template('newuser.html', form=form,groups=groups)


# working on sending email confirmation link from here:
# https://www.youtube.com/watch?v=vF9n248M1yk

@app.route('/verify/', methods=['GET','POST'])
def verifyemail(theUser,theEmail,userEmail):
    #token = request.token

    if request.method == 'GET':
        return '<form action="/verify/" method="POST"><input name="email"><input type="submit"></form>'

    email = theEmail
    token = s.dumps(userEmail,salt=Config.SALT)
    text = 'Confirm New User: {}'.format(theUser)
    msg = Message(text, sender='albertk@gmx.com',recipients=[email])
    link = url_for('.confirm_email',token=token, _external=True)
    msg.body = 'Click here to confirm {} as new active user <br> {}'.format(theUser,link)
    mail.send(msg)
    # clean up and return as html
    return 'an email has been sent for verification'

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        # SHA-256 to encode the token via email
        email = s.loads(token, max_age=10000,salt=Config.SALT)
        print email
        user = User.get(User.email == email)
        # print user
        user.activated = 1
        user.save()
        return '{} has been activated!'.format(user.username)

    except:
        return render_template('token.html',token=token)



@app.route('/deactivate_account/<token>')
def deactivate_email(token):
    try:
        # SHA-256 to encode the token via email
        email = s.loads(token, max_age=10000,salt="email-confirm")
        print email
        user = User.get(User.email == email)
        # print user
        user.activated = 0
        user.save()
        return '{} has been deactivated!'.format(user.username)
    except SignatureExpired:
        return "token doesn't work"

# this handles the group/sponsors page, after sponsor logs on it they can:
# 1. list all the users for the sponsor *done
# 2. allow to activate/deactivate sponsor's accounts
# 3. change password
# 4. see user's storage/compute time
# 5. set provisions on user's storage/compute time

@app.route('/group/<groupname>', methods=['GET','POST'])
def group(groupname):
    sponsor = Sponsor.get(Sponsor.groupname == groupname)
    #users = User.username
    email = sponsor.groupname
    users = User.select().where(User.sponsor == groupname)
    return render_template('default.html',username=users,groupname=groupname)


# this handles the login for the sponsors, then sends them to the group page if logged in
@app.route('/sponsor', methods=['POST'])
def do_admin_sponsor():
    sponsor = Sponsor()
    passwordAttempt = bcrypt.hashpw(request.form['password'])
    if passwordAttempt == sponsor.password and request.form['username'] == sponsor.username:
        print 'did it!'
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return grouppage()


@app.route("/")
def index():
    username = BaseModel.select(BaseModel.username)
    return render_template('default.html',username=username)
    db.close()
    
@app.route("/newgroup/")
def newuser():
    return "hello, sign up here"
    db.close()


if __name__ == "__main__":
        app.run(debug=True)