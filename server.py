import bottle
from bottle import run, template, request, hook, route, redirect, static_file
import beaker.middleware
import os

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

# Static routes for serving files in the assets directory
@route('/<filename:re:.*\.js>', method="GET")
def javascripts(filename):
    return static_file(filename, root='assets/js')

@route('/<filename:re:.*\.css>', method="GET")
def stylesheets(filename):
    return static_file(filename, root='assets/css')

@route('/<filename:re:.*\.(jpg|png|gif|ico)>', method="GET")
def images(filename):
    return static_file(filename, root='assets/img')

################ Interesting code below

@route('/')
def index():
        return redirect('/dashboard', code=302)

# GET requests to index will return a form to fill out a name
@route('/dashboard', method='GET')
def dashboard():
        name = request.session.get('name', None)
        city = request.session.get('city', None)
        state = request.session.get('state', None)
        session_list = [name, city, state]
        if all(session_var is not None for session_var in session_list):
                return template('welcome', name=name, city=city, state=state)
        return template('dashboard')
                

# POST requests to index will acknowledge the user
# and set a session variable to be used with other requests
@route('/dashboard', method='POST')
def dashboard():
	name = request.forms.get('name')
	request.session['name'] = name
	city = request.forms.get('city')
	request.session['city'] = city
	state = request.forms.get('state')
	request.session['state'] = state	
	return template('welcome', name=name, city=city, state=state)

# Open weather dashboard
@route('/weather', method='GET')
def weather():
        return template('weather', name=request.session['name'], \
                        city=request.session['city'], \
                        state=request.session['state'])

# Exit current session
@route('/logout')
def logout():
        request.session.clear()
        return redirect("/")

# Start the server
run(app, host='localhost', port=8080)
