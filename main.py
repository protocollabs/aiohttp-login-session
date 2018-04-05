#!/usr/bin/env python
#
# Simple aiohttp login system with default user!.
# This system is built with aiohttp module.
# Requires Python3 or higher.


import os
from aiohttp import web
import json

# Customize the cookie name, value and cookie expire date.
# The cookie will be stored 30 days long.
COOKIE_NAME = "OldTamil"
COOKIE_VALUE = 0
COOKIE_LIFE_TIME = 24 * 60 * 60 * 30

# Define the required host and port.
HOST = '127.0.0.1'
PORT = 8888

# Files
LOGIN_HTML = 'login.html'
SITE_HTML = 'site.html'
REDIRECT_HTML = 'redirect.html'
CONFIG_FILE = 'configuration.json'


# Simple error html page for server error.
# Server error can be caused by missing required files.
ERROR ='''<!DOCTYPE html>
<html>
  <head>
    <title>SERVER ERROR</title>
    <style type ="text/css">
    body { text-align:center; padding: 10%; font-weight: bold; font: 20px Helvetica, sans-serif; }
    a {padding: 30px;}
    h1 {color:#D0AA0E ; font-family: Arial, Helvetica, sans-serif; font-size: 30px;}
    </style>
  </head>
     <body>
       <h1> Unexpected server error </h1>
       <p> Please try again later</p>
     </body>
</html>'''


# A separate server error get request to display error.
def check(filename):
    if not os.path.isfile(filename):
        print("Internal server error! file not found: {}".format(filename))
        return False
    response = open(filename).read()
    return response


def json_file_read(filename):
    check_file = check(filename)
    if not check_file:
        return False
    configure_file = open(filename)
    load_data = json.load(configure_file)
    try:
        if not load_data['USERNAME'] and load_data['PASSWORD']:
            return False
        return load_data
    except KeyError:
        print("Dictionay don't have correct keys and value")
        return False


# Check for the requested file in the system, return server error! if file not found.
# User credentials stored in a json file. Loads the json file to access the values.
# Check if json file can be accessible.
def check_cookie(request):
    """cookie_check!
    This function will check for valid cookie on all pages!
    Return True if there is valid cookie.
    """
    cookie = request.cookies.get(COOKIE_NAME, None)
    # If there is a cookie, return True.
    if not cookie:
        return False
    try:
        if not int(cookie) == COOKIE_VALUE:
            return False
        return True
    except ValueError:
        alert_message = """Warning:Cookie has been modified by the user!.
        Details:
            Cookie Name: {} and Cookie value: {}
            \nModified Cookie Value: {}"""
        print(alert_message.format(COOKIE_NAME, COOKIE_VALUE, cookie))
        return False
    return False

# Get the user credentials from json data and validate the user inputs.
def check_credentials(username, password):
    credentials = json_file_read(CONFIG_FILE)
    if not credentials:
        return False
    if username == credentials['USERNAME'] and password == credentials['PASSWORD']:
        return True
    return False



async def server_error(request):
    valid_cookie = check_cookie(request)
    if not valid_cookie:
        return web.Response(text=ERROR, content_type='text/html')
    return web.HTTPFound('/')


# The main page of the website
async def home(request):
    check_the_file = check(SITE_HTML)
    if not check_the_file:
        # By default, return to server error if the file is not found.
        return web.HTTPFound('/error')
    valid_cookie = check_cookie(request)
    if not valid_cookie:
        return web.HTTPFound('/log')
    return web.Response(text=check_the_file, content_type='text/html')


# Redirect to home page if user enters invalid credentials !
async def redirect(request):
    redirect_page = check(REDIRECT_HTML)
    if not redirect_page:
        return web.HTTPFound('/error')
    valid_cookie = check_cookie(request)
    if not valid_cookie:
        return web.Response(text=redirect_page, content_type='text/html')
    return web.HTTPFound('/')


async def login_page(request):
    """ When the user is unknown or the user's cookie is expired, will redirect to login page
    check for cookies in the login_page and return to main page if there is valid cookie.
    """
    login_file = check(LOGIN_HTML)
    if not login_file:
        return web.HTTPFound('/error')
    valid_cookie = check_cookie(request)
    if not valid_cookie:
        return web.Response(text=login_file, content_type='text/html')
    response = web.HTTPFound('/log')
    if not check_cookie(request):
        return response.del_cookie(COOKIE_NAME)
    return web.HTTPFound('/')


# Login required if the user is new or user's cookie expired.
async def login(request):
    form = await request.post()
    username = form.get('username')
    password = form.get('password')
    if not json_file_read(CONFIG_FILE):
        return web.HTTPFound('/error')
    if not check_credentials(username, password):
        return web.HTTPFound('/redirect')
    # The user is successfully logged in, set the cookie on the index page.
    response = web.Httpfound('/')
    response.set_cookie(COOKIE_NAME, value=COOKIE_VALUE, max_age=COOKIE_LIFE_TIME)
    return response

# Routes
app = web.Application()
app.router.add_get('/', home)
app.router.add_get('/log', login_page)
app.router.add_post('/login', login)
app.router.add_get('/redirect', redirect)
app.router.add_get('/error', server_error)
web.run_app(app, host=HOST, port=PORT)

