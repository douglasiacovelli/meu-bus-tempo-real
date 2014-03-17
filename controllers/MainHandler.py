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
		self.response.headers['Content-Type'] = 'application/json'

		bus_code = self.request.get('bus-code')

		api_credential = memcache.get('api_credential')
		expiration_time = memcache.get('expiration_time')

		now = datetime.datetime.now()

		# Avoid a lot of Auth requests. Only one is necessary
		if api_credential is None:

			url = 'http://api.olhovivo.sptrans.com.br/v0/Login/Autenticar?token='+config.token
			result = urlfetch.fetch(url = url, method = urlfetch.POST)
			
			api_credential = result.headers['set-cookie']

			memcache.add('api_credential', api_credential, 1800)
			print('criado memcache')
		

		bus_code = str(bus_code)
		url = 'http://api.olhovivo.sptrans.com.br/v0/Linha/Buscar?termosBusca='+bus_code

		bus_lines = urlfetch.fetch(url = url, method = urlfetch.GET, headers = {'Cookie': api_credential})


		print(bus_lines.content)
		self.response.write(bus_lines.content)
		

			

		
		
		
