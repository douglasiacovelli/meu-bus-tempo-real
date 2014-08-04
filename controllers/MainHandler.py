import os
import webapp2
import cgi
import json
import urllib
import datetime

from configs import config
from google.appengine.api import urlfetch

from google.appengine.ext.webapp import template

class home(webapp2.RequestHandler):
	def get(self):
		# We are using the template module to output the page.
	
		path = os.path.join(os.path.dirname(__file__), '..' , 'views' ,'home.html')
		self.response.out.write(
		
			# The render method takes the path to a html template,
			# and a dictionary of key/value pairs that will be
			# embedded in the page.
			
			template.render(path,{})
		)

		
	
	def post(self):

		class_aux = aux()
		api_credential = class_aux.auth_sptrans()


		print(api_credential)

		# Prepare and fetch the bus code
		bus_code = str(self.request.get('bus-code'))
		bus_code = urllib.quote_plus(bus_code)
		
		# To-Do: save requests already made and the result to avoid one more call to the API

		good_response = False

		while good_response is False:

			url = 'http://api.olhovivo.sptrans.com.br/v0/Linha/Buscar?termosBusca='+bus_code
			bus_lines = urlfetch.fetch(url = url, method = urlfetch.GET, deadline=15, follow_redirects=False, headers = {'Cookie': api_credential})

			if bus_lines.status_code != 401:
				good_response = True

		print(bus_lines.content)

		#send the response
		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(bus_lines.content)


class realtime(webapp2.RequestHandler):
	def post(self):
		class_aux = aux()
		api_credential = class_aux.auth_sptrans()

		good_response = False

		while good_response is False:
			url = 'http://api.olhovivo.sptrans.com.br/v0/Posicao?codigoLinha='+self.request.get('id')
			buses_positions = urlfetch.fetch(url = url, method = urlfetch.GET, deadline=15, follow_redirects=False, headers = {'Cookie': api_credential})

			if buses_positions.status_code != 401:
				good_response = True

		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(buses_positions.content)

	def get(self):
		class_aux = aux()
		api_credential = class_aux.auth_sptrans()


		bus_line = self.request.get('bus_line')
		
		positions = []

		if bus_line == '8012':
			bus_codes = ['2023','34791']
		else:
			bus_codes = ['2085', '34853']

		for bus_code in bus_codes:
			good_response = False

			while good_response is False:
				url = 'http://api.olhovivo.sptrans.com.br/v0/Posicao?codigoLinha='+bus_code
				buses_positions = urlfetch.fetch(url = url, method = urlfetch.GET, deadline=15, follow_redirects=False, headers = {'Cookie': api_credential})

				if buses_positions.status_code != 401:
					good_response = True
					data = buses_positions.content
					#print data
					data = json.loads(data)
					
					for position in data['vs']:
						positions.append(position)		

		#print positions
		positions = json.dumps(positions)

		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(positions)

class aux():
	def auth_sptrans(self):
		 
		url = 'http://api.olhovivo.sptrans.com.br/v0/Login/Autenticar?token='+config.token
		result = urlfetch.fetch(url = url, method = urlfetch.POST)

		api_credential = result.headers['set-cookie']

		return api_credential