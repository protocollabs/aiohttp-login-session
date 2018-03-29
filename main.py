#!/usr/bin/env python
# 
# Simple aiohttp login system with default user!.
# This system is built with aiohttp module.
# Requires Python3 or higher.  


import os
import os.path
from aiohttp import web


# Customize the cookie name, value and cookie expire date. 
# The cookie will be stored 30 days long.
COOKIE_NAME = "OldTamil"
COOKIE_VALUE = 0
COOKIE_LIFE_TIME = 24 * 60 * 60 * 30   


# User credentials.
USERNAME = 'Hippod'
PASSWORD = 'admin'

# Define the required host and port.
HOST = '127.0.0.1'
PORT = 8888


def check_cookie(request):
    """cookie_check!
    This function will check for valid cookie on all pages!
    Return True if there is valid cookie.

    """
    cookie = request.cookies.get(COOKIE_NAME, None)
    if not cookie:
        return False
    if COOKIE_VALUE == 0:
        return True


def check_credentials(username, password):
    if username == USERNAME and password == PASSWORD:
        return True
    return False


def check_file(filename):
    if not os.path.isfile(filename):
        print("Internal server error! file not found: {}".format(filename))
        return False
    return open(filename).read()


# The main page of the website
async def index(request):
    valid_cookie = check_cookie(request)
    if valid_cookie is True:
        page = check_file('site.html')
        if page:
            return web.Response(text=page, content_type='text/html')
        else:
            response = check_file('error.html')
            return web.Response(text=response, content_type='text/html')
    return web.HTTPFound(location='/log')


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
        if page:
            return web.Response(text=page, content_type='text/html')
        else:
            response = check_file('error.html')
            return web.Response(text=response, content_type='text/html')

    return web.HTTPFound('/')
        

# Login required if the user is new or user's cookie expired and check the user credentials.
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
web.run_app(app, host=HOST, port=PORT)
