# Import from peewee
import peewee as pw
import os
from flask import session



from config import Config
# Connect to the PostgresqlDatabase

# for local connecting purposes
# db = PostgresqlDatabase('janemap', user='postgres', password='password',
                           # host='127.0.0.1', port=5432)

db = pw.MySQLDatabase(Config.DATABASE,host=Config.HOST, user=Config.USERNAME, password=Config.SECRET_KEY,
                          port=Config.PORT)
# Connect to our database.
db.connect()

# Define what a 'data' is
class BaseModel(pw.Model):
	# These are all the fields it has
	# match up CharField/IntegerField/etc with correct type
	#uid = CharField(primary_key=True) # primary key = unique id
	id = pw.IntegerField(primary_key=True)
	#value = pw.IntegerField()
	username = pw.CharField()

	class Meta:
		database = db
		# and it's in the table called 'hpc'
		db_table = 'hpc'
		primary_key = False

# Define what a 'user' is
class User(pw.Model):
	# These are all the fields it has
	# match up CharField/IntegerField/etc with correct type
	#uid = CharField(primary_key=True) # primary key = unique id
	#value = pw.IntegerField()
	uid = pw.IntegerField(primary_key=True)
	username = pw.CharField()
	email = pw.CharField(unique=True)
	sponsor = pw.CharField()
	password = pw.CharField()
	activated = pw.BooleanField()

	class Meta:
		database = db
		db_table = 'users'
		primary_key = False


# Define what a 'sponsor' is
class Sponsor(pw.Model):
	# These are all the fields it has
	# match up CharField/IntegerField/etc with correct type
	uid = pw.IntegerField(primary_key=True)
	groupname = pw.CharField()
	email = pw.CharField()
	password = pw.CharField()

	class Meta:
		database = db
		db_table = 'group'
		primary_key = False