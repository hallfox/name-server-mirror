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
	request.session['user'] = {'name':name, 'solved_1':False, 'key':False}
	return template('welcome', name=name)

# Sample function using request.session dictionary
@route('/hi')
def hi():
	user = request.session.get('user', None)
	if user is not None:
		name = user.get('name')
		return 'logged in as {}'.format(name)
	return 'not logged in'
	
@route('/maze')
def maze():
	user = request.session.get('user', None)
	if user is not None:
		name = user.get('name')
		return template('maze', name=name)
	return 'you must log in to play the maze game'

@route('/maze', method='POST')
def maze():
	answer = request.forms.get('in')
	if answer is not None:
		if answer[:4] == "open":
			request.session['user']['solved_1'] = True
			return '<a href="/maze/lobby">The door opens easily. Good thing it was unlocked.</a>'
		return template('game_over')

@route('/maze/lobby')
def lobby():
	solved_p1 = request.session['user'].get('solved_1')
	if solved_p1:
		return template('lobby')
	return "This story is told in a linear way. Don't try to get all timey-wimey with me."

@route('/maze/lobby', method='POST')
def lobby():
	has_key = request.session['user'].get('key')
	if has_key:
		return template('end')
	return template('game_over')
	
@route('/maze/key')
def key():
	request.session['user']['key'] = True
	return template('key')

# Start the server
run(app, host='localhost', port=8080)
