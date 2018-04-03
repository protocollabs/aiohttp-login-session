#!/usr/bin/env python
# 
# Simple aiohttp login system with default user!.
# This system is built with aiohttp module.
# Requires Python3 or higher.  


import os
import os.path
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


# Check for the requested file in the system, return server error! if file not found.
def check_file(filename):
    if not os.path.isfile(filename):
        print("Internal server error! file not found: {}".format(filename))
        return False
    response = open(filename).read()
    return response


# User credentials stored in a json file. Loads the json file to access the values.
# Check if json file can be accessible.
check = check_file('configuration.json')
if check:
    users = open('configuration.json')
    load_data = json.load(users)


def check_cookie(request):
    """cookie_check!
    This function will check for valid cookie on all pages!
    Return True if there is valid cookie.
    """
    cookie = request.cookies.get(COOKIE_NAME, None)
    # If there is a cookie, return True.
    if cookie:
        return True
    return False


# Get the user credentials from json data and validate the user inputs.
def check_credentials(username, password):
    if username == load_data['USERNAME'] and password == load_data['PASSWORD']:
        return True
    return False


# Simple error html page for server error.
# Server error can be caused by missing required files.
ERROR = '''<!DOCTYPE html>
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
       <a href="log"> Return </a>
     </body>
</html>'''


# A separate server error get request to display error.
async def server_error(request):
    return web.Response(text=ERROR, content_type='text/html')


# The main page of the website
async def index(request):
    valid_cookie = check_cookie(request)
    if valid_cookie:
        page = check_file('site.html')
        if not page:
            # By default, return to server error if the file is not found.
            return web.HTTPFound('/error')
        return web.Response(text=page, content_type='text/html')
    return web.HTTPFound('/log')


# Redirect to home page if user enters invalid credentials !
async def redirect_page(request):
    valid_cookie = check_cookie(request)
    if not valid_cookie:
        page = check_file('redirect.html')
        return web.Response(text=page, content_type='text/html')
    return web.HTTPFound('/')


async def login_page(request):
    """ When the user is unknown or the user's cookie is expired, will redirect to login page
    check for cookies in the login_page and return to main page if there is valid cookie.
    """
    valid_cookie = check_cookie(request)
    if not valid_cookie:
        page = check_file('login.html')
        if not page:
            return web.HTTPFound('/error')
        return web.Response(text=page, content_type='text/html')
    return web.HTTPFound('/')


# Login required if the user is new or user's cookie expired.
async def login(request):
    form = await request.post()
    username = form.get('username')
    password = form.get('password')
    if not check_credentials(username, password):
        return web.HTTPFound('/redirect')
    # The user is successfully logged in, set the cookie on the index page.
    response = web.HTTPFound(location='/')
    response.set_cookie(COOKIE_NAME, value=COOKIE_VALUE, max_age=COOKIE_LIFE_TIME)
    return response


# Routes
app = web.Application()
app.router.add_get('/', index)
app.router.add_get('/log', login_page)
app.router.add_post('/login', login)
app.router.add_get('/redirect', redirect_page)
app.router.add_get('/error', server_error)
web.run_app(app, host=HOST)
