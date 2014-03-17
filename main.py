#importing the webapp2 framework
import webapp2

# importing the controllers that will handle
# the generation of the pages:  
from controllers import MainHandler

#importing template from django
from google.appengine.ext.webapp import template


#running webapp2 view and setting URL routing
app = webapp2.WSGIApplication([
		('/', MainHandler.home),
		('/realtime', MainHandler.realtime)

	],debug = True)