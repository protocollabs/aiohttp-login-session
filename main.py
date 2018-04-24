#!/usr/bin/env python3
#
# Simple aiohttp login system with default user!.
# This system has been built by using aiohttp module.
# Require Python3 or higher.


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

# Html and json files defined!
LOGIN_HTML = 'login.html'
SITE_HTML = 'site.html'
REDIRECT_HTML = 'redirect.html'
CONFIG_FILE = 'configuration.json'


# Server error html for web view
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


# Login handles checking, reading files and user credentials
# We use cookie on client site after user successfully logged in
class Login:

    # check file existence
    def _check_the_file(self, filename):
        if not os.path.isfile(filename):
            print("Internal server error! " \
                  "file not found:{}".format(filename))
            return False
        return True

    # read html files
    # return False if requested file format is not .html
    def _load_html_file(self, filename):
        if not self._check_the_file(filename):
            return False
        if not filename.endswith(".html"):
            print("{} is not html file".format(filename))
            return False
        response = open(filename).read()
        return response

    # load json file and return to dictionary
    # return False if requested file format is not .json
    # or keys in dictionary is missing
    def _load_credentials(self, filename):
        if not self._check_the_file(filename):
            return False
        if not filename.endswith(".json"):
            print("{} is not a json file.".format(filename))
            return False
        configure_file = open(filename)
        load_json_data = json.load(configure_file)
        # check dictionary has following keys
        if not all(key in load_json_data for key in("USERNAME", "PASSWORD")):
            return False
        return load_json_data

    # check for the cookie on the requested page
    # return False if there is no authorized cookie
    def _check_cookie(self, request):
        cookie_value = request.cookies.get(COOKIE_NAME, None)
        if not cookie_value:
            return False
        try:
            # check the requested cookie value
            if not int(cookie_value) == COOKIE_VALUE:
                return False
            return True
        except ValueError:
            return False
        return False

    # check username and password
    def _check_credentials(self):
        credentials = self._load_credentials(CONFIG_FILE)
        if not credentials:
            return False
        authorized_username = credentials['USERNAME']
        authorized_password = credentials['PASSWORD']
        if not (self.username == authorized_username and
                self.password == authorized_password):
            return False
        return True

    async def server_error(self, request):
        """ Error when a requested file
        or content of the file is missing.
        """
        return web.Response(text=ERROR, content_type='text/html')

    async def home(self, request):
        site_file = self._load_html_file(SITE_HTML)
        if not site_file:
            return web.HTTPFound('/error')
        valid_cookie = self._check_cookie(request)
        if not valid_cookie:
            return web.HTTPFound('/log')
        return web.Response(text=site_file, content_type='text/html')

    async def redirect(self, request):
        redirect_file = self._load_html_file(REDIRECT_HTML)
        if not redirect_file:
            return web.HTTPFound('/error')
        valid_cookie = self._check_cookie(request)
        if not valid_cookie:
            return web.Response(text=redirect_file, content_type='text/html')
        return web.HTTPFound('/')

    async def login_page(self, request):
        login_file = self._load_html_file(LOGIN_HTML)
        if not login_file:
            return web.HTTPFound('/error')
        valid_cookie = self._check_cookie(request)
        if not valid_cookie:
            return web.Response(text=login_file, content_type='text/html')
        return web.HTTPFound('/')

    async def login(self, request):
        if not self._load_credentials(CONFIG_FILE):
            return web.HTTPFound('/error')
        form = await request.post()
        self.username = form.get('username')
        self.password = form.get('password')
        if not self._check_credentials():
            return web.HTTPFound('/redirect')
        # Set the time for 30 days long
        time_ = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        cookie_expiry_date = time_.strftime("%a, %d %b %Y %H:%M:%S GMT")
        response = web.HTTPFound('/')
        response.set_cookie(COOKIE_NAME,
                            value=COOKIE_VALUE, expires=cookie_expiry_date)
        return response


# Add routes
def aiohttp_login():
    app = web.Application()
    app.router.add_routes([web.get('/log', Login().login_page),
                           web.post('/login', Login().login),
                           web.get('/', Login().home),
                           web.get('/error', Login().server_error),
                           web.get('/redirect', Login().redirect)])
    return web.run_app(app, host=HOST, port=PORT)


if __name__ == '__main__':
    aiohttp_login()
