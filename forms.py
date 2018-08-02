from flask_wtf import FlaskForm
from wtforms import TextField, StringField, BooleanField, DateField,DateTimeField, SelectField,PasswordField
from wtforms.validators import DataRequired, Email

EVENT_TYPES =[("canvassing","Canvassing"),("phone_banking","Phone banking"),
				("voter_reg","Voter Registration"),("meeting","Meeting"), 
				("fundraiser","Fundraiser"),("rally","Rally"),
				("house_party","House Party"),("forum", "Forum/Discussion"),
				("other","Other")]

class NewUser(FlaskForm):
	username = StringField('Username')
	email = StringField('Email Address')
	groupname = StringField('Sponsor')
	password = PasswordField()
	activated = BooleanField()

	
class RSVPform(FlaskForm):
	name = TextField("Host Name")
	email = TextField("Email")
	phone = TextField("Phone")
	event_id = BooleanField()