import bottle
from bottle import run, template, request, hook, route
import beaker.middleware

# Set up a way to keep session variables
# Unimportant
session_opts = {
	'session.type': 'file',
	'session.data_dir': './session/',
	'session.auto': True,
}
app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)

# Session variables can be found at request.session
# Unimportant
@hook('before_request')
def setup_request():
	request.session = request.environ['beaker.session']

################ Interesting code below

# GET requests to index will return a form to fill out a name
@route('/', method='GET')
def index():
	return template('start')

# POST requests to index will acknowledge the user
# and set a session variable to be used with other requests
@route('/', method='POST')
def index():
	name = request.forms.get('name')
	request.session['name'] = name
	return template('welcome', name=name)

# Sample function using request.session dictionary
@route('/hi')
def hi():
	name = request.session.get('name', None)
	if name is not None:
		return 'logged in as {}'.format(name)
	return 'not logged in'

# Start the server
run(app, host='localhost', port=8080)
