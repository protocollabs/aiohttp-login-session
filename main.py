#!/usr/bin/env python
#
# Simple aiohttp login system with default user!.
# This system is built with aiohttp module.
# Requires Python3 or higher.


import os
from aiohttp import web
import json
import datetime


# Customize the cookie name, value and cookie expire date.
# The cookie will be stored on the client site for 30 days long.
COOKIE_NAME = "OldTamil"
COOKIE_VALUE = 0


# Define the required host and port.
HOST = '127.0.0.1'
PORT = 8080


# All html and other files required from outside.
# All these files required by the server, modifying contents inside the file
# may cause server error.
LOGIN_HTML = 'login.html'
SITE_HTML = 'site.html'
REDIRECT_HTML = 'redirect.html'
CONFIG_FILE = 'configuration.json'


# Simple error web view for server error.
# Server error can be caused by missing required files.
ERROR = '''<!DOCTYPE html>
<html>
  <head>
    <title>SERVER ERROR</title>
    <style type ="text/css">
    body { text-align:center; padding: 10%;
    font-weight: bold; font: 20px Helvetica, sans-serif; }
    a {padding: 30px;}
    h1 {color:#FF0000 ; font-family: Arial, Helvetica, sans-serif;
        font-size: 30px;}
    </style>
  </head>
     <body>
     <h1> ERROR: Unexpected server error </h1>
       <p> Please try again later</p>
       <p>The Team</p>
     </body>
</html>'''


# Check the requested file by user, and return server error if the file is
# missing.
def check_the_file(filename):
    if not os.path.isfile(filename):
        print("Internal server error! file not found: {}".format(filename))
        return False
    response = open(filename).read()
    return response


# Checking the configuration file and valid the data.
# The checking may fail by missing json file, missing valid data in the file.
# Cause server error when configuration file has been modified.
def json_reader(filename):
    check_file = check_the_file(filename)
    if not check_file:
        return False
    configure_file = open(filename)
    load_data = json.load(configure_file)
    try:
        if not(load_data['USERNAME'] and load_data['PASSWORD']):
            return False
        return load_data
    except KeyError:
        print("{} doesn't have valid keys and value".format(filename))
        pass


# Identifying the user by validate the cookie. User must login if there is no
# valid cookie
# Cookie safety has been implemented. If user tries to
# modify the cookie value it returns False.
# Make sure user cannot modify cookie expire date.
def check_cookie(request):
    cookie_value = request.cookies.get(COOKIE_NAME, None)
    if not cookie_value:
        return False
    try:
        if not int(cookie_value) == COOKIE_VALUE:
            return False
        return True
    except ValueError:
        return False
    return False


# Validate user credentials
def check_credentials(username, password):
    credentials = json_reader(CONFIG_FILE)
    if not credentials:
        return False
    USERNAME = credentials['USERNAME']
    PASSWORD = credentials['PASSWORD']
    if not(username == USERNAME and password == PASSWORD):
        return False
    return True


async def server_error(request):
    valid_cookie = check_cookie(request)
    if not valid_cookie:
        check_login_file = check_the_file(LOGIN_HTML)
        if not check_login_file:
            return web.Response(text=ERROR, content_type='text/html')
        return web.HTTPFound('/log')
    return web.HTTPFound('/')


# The main page of the website
async def home(request):
    site_file = check_the_file(SITE_HTML)
    if not check_the_file:
        return web.HTTPFound('/error')
    valid_cookie = check_cookie(request)
    if not valid_cookie:
        return web.HTTPFound('/log')
    return web.Response(text=site_file, content_type='text/html')


# Redirect to home page if user enters invalid credentials!.
async def redirect(request):
    redirect_file = check_the_file(REDIRECT_HTML)
    if not redirect_file:
        return web.HTTPFound('/error')
    valid_cookie = check_cookie(request)
    if not valid_cookie:
        return web.Response(text=redirect_file, content_type='text/html')
    return web.HTTPFound('/')


async def login_page(request):
    """ When the user is unknown or the user's cookie is expired,
    will redirect to login page.Check for cookies in the login_page.
    Return to main page if there is valid cookie.
    """
    login_file = check_the_file(LOGIN_HTML)
    if not login_file:
        return web.HTTPFound('/error')
    valid_cookie = check_cookie(request)
    if not valid_cookie:
        return web.Response(text=login_file, content_type='text/html')
    return web.HTTPFound('/')


# Check the user credentials and set cookie on home page.
async def login(request):
    form = await request.post()
    username = form.get('username')
    password = form.get('password')
    if not json_reader(CONFIG_FILE):
        return web.HTTPFound('/error')
    if not check_credentials(username, password):
        return web.HTTPFound('/redirect')
    # The user is successfully logged in, set the cookie on the index page.
    response = web.HTTPFound('/')
    expires = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    COOKIE_EXPIRE = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
    response.set_cookie(COOKIE_NAME, value=COOKIE_VALUE, expires=COOKIE_EXPIRE)
    return response


# Routes
app = web.Application()
app.router.add_get('/', home)
app.router.add_get('/log', login_page)
app.router.add_post('/login', login)
app.router.add_get('/redirect', redirect)
app.router.add_get('/error', server_error)
web.run_app(app, host=HOST, port=PORT)
