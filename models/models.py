from google.appengine.ext import db

# These classes define the data objects
# that you will be able to store in
# AppEngine's data store.

class ApiCredential(db.Model):
	api_cookie = db.StringProperty(required = True)
	date = db.DateTimeProperty(auto_now_add=True)