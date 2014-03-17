import os
import webapp2
import cgi
import json
import urllib
import datetime

from configs import config
from google.appengine.api import urlfetch

from google.appengine.ext.webapp import template

from google.appengine.api import memcache


class home(webapp2.RequestHandler):
	def get(self):
		# We are using the template module to output the page.
	
		path = os.path.join(os.path.dirname(__file__), '..' , 'views' ,'home.html')
		self.response.out.write(
		
			# The render method takes the path to a html template,
			# and a dictionary of key/value pairs that will be
			# embedded in the page.
			
			template.render( path,{
				"title"	: 'Meu App do bus'
		}))

		
	
	def post(self):

		class_aux = aux()
		api_credential = class_aux.auth_sptrans()

		print(api_credential)
		#Prepare and fetch the bus code
		bus_code = str(self.request.get('bus-code'))

		bus_code = urllib.quote_plus(bus_code)
		print(bus_code)

		url = 'http://api.olhovivo.sptrans.com.br/v0/Linha/Buscar?termosBusca='+bus_code

		bus_lines = urlfetch.fetch(url = url, method = urlfetch.GET, headers = {'Cookie': api_credential})

		print(bus_lines.content)

		#send the response
		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(bus_lines.content)


class realtime(webapp2.RequestHandler):
	def post(self):
		class_aux = aux()
		api_credential = class_aux.auth_sptrans()

		url = 'http://api.olhovivo.sptrans.com.br/v0/Posicao?codigoLinha='+self.request.get('id')
		buses_positions = urlfetch.fetch(url = url, method = urlfetch.GET, headers = {'Cookie': api_credential})

		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(buses_positions.content)


class aux():
	def auth_sptrans(self):
		# api_credential = memcache.get('api_credential')

		# # Only make one Auth request between 30 min (1800s) 
		# if api_credential is None:

		url = 'http://api.olhovivo.sptrans.com.br/v0/Login/Autenticar?token='+config.token
		result = urlfetch.fetch(url = url, method = urlfetch.POST)

		api_credential = result.headers['set-cookie']

		api_credential = api_credential.split(';')[0]

		return str(api_credential)
			

		
		
		
