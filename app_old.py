from flask import Flask, render_template,flash, redirect, request, url_for,jsonify,abort,make_response, Response, abort, redirect, flash,request
#bring in module for safe signing in unsecure environment
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
#bring in module for flask admin
from flask_admin import Admin
#bring in ORM called peewee
from flask_admin.contrib.peewee import ModelView
#bring in modules
from models import *
import bcrypt
#bring in flask mail
from flask_mail import Mail, Message


from forms import NewUser
import operator
import sys

# #from .forms import EmailPasswordForm
# from util import ts, send_email

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config.from_object('config.EmailServer')

s = URLSafeTimedSerializer('thissceret')

mail = Mail(app)

def get_serializer(secret_key=None):
    if secret_key is None:
        secret_key = app.secret_key
    return URLSafeTimedSerializer(secret_key)
    print URLSafeTimedSerializer(secret_key)

admin = Admin(app, name='microblog', template_mode='bootstrap3')
#global events
#pip install pymysql
#events = Event.select().order_by(Event.event_date.asc())

admin.add_view(ModelView(BaseModel))


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
                #print getattr(user,theField)
        username = request.form['username']
        passhash = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        #print passhash
        form.data['password'] = passhash
        setattr(user,'password',passhash)
        #app.logger.info(form.data)
        #print getattr(user,theField)
        user.save()
        return redirect(url_for('userlist'))
    elif request.method =='GET':
        return render_template('newuser.html', form=form)


# working on sending email confirmation link from here:
# https://www.youtube.com/watch?v=vF9n248M1yk

@app.route('/verify/', methods=['GET','POST'])
def verifyemail():
    #token = request.token
    if request.method == 'GET':
        return '<form action="/verify/" method="POST"><input name="email"><input type="submit"></form>'

    email = request.form['email']
    token = s.dumps(email,salt='email-confirm')
    
    msg = Message('Confirm Email', sender='albertk@gmx.com',recipients=[email])
    link = url_for('.confirm_email',token=token, _external=True)
    msg.body = 'Click here to confirm your email {}'.format(link)
    mail.send(msg)

    return '<h1>the email you entered is {}'.format(email)
    #return make_response('Could notverify!',401,{'lo':'li'})

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, max_age=1000,salt="email-confirm")
        User.get(User.username == email)
        User.activated = 1
        User.save()
        return 'email has been activated!'
    except SignatureExpired:
        return "token doesn't work"


# old activation procedures

@app.route('/activate/<payload>')
def confirm_email_v2(token):
    try:
        #email = ts.loads(token, salt="email-confirm-key", max_age=86400)
        print hello
    except:
        abort(404)

    user = User.query.filter_by(email=email).first_or_404()

    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('signin'))
def get_activation_link(user):
    s = get_serializer()
    payload = s.dumps(user.id)
    return url_for('activate_user', payload=payload, _external=True)

@app.route("/")
def index():
    username = BaseModel.select(BaseModel.username)
    return render_template('default.html',username=username)
    db.close()

@app.route("/users")
def userlist():
    userlist = User.select(User.username,User.password)
    test = User.get(User.username == 'aaron')
    #print test.username
    new_password = '24243'
    testpw = bcrypt.hashpw(new_password.encode('utf-8'),test.password.encode('utf-8'))
    if testpw == test.password:
        print "same pass"
    else:
        print "different pass"
    return render_template('default2.html',username=userlist)
    db.close()    

@app.route("/newgroup/")
def newuser():
    return "hello, sign up here"
    db.close()


if __name__ == "__main__":
        app.run(debug=True)