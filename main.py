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

    # Check html and json files
    def _check_the_file(self, filename):
        self.__filename = filename
        _file = os.path.isfile(self.__filename)
        if not _file:
            print("Internal server error! " \
                  "file not found:{}".format(self.__filename))
            return False

        # Read html files
        if self.__filename.endswith(".html"):
            response = open(self.__filename).read()
            return response

        # Read json file
        elif self.__filename.endswith(".json"):
            configure_file = open(self.__filename)
            load_data = json.load(configure_file)
            if all(key in load_data for key in("USERNAME", "PASSWORD")):
                return load_data
            return False

        # Unsupported file format
        else:
            message = ("{} is not in a required format".format(self.__filename))
            print(message)
            return False

    def _check_cookie(self, request):
        # Get cookie value
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

    def _check_credentials(self):
        credentials = self._check_the_file(CONFIG_FILE)
        if not credentials:
            return False
        username = credentials['USERNAME']
        password = credentials['PASSWORD']
        if not (self.username == username and self.password == password):
            return False
        return True

    async def server_error(self, request):
        """ Error when a requested file
        or content of the file is missing.
        """
        return web.Response(text=ERROR, content_type='text/html')

    async def home(self, request):
        site_file = self._check_the_file(SITE_HTML)
        if not site_file:
            return web.HTTPFound('/error')
        valid_cookie = self._check_cookie(request)
        if not valid_cookie:
            return web.HTTPFound('/log')
        return web.Response(text=site_file, content_type='text/html')

    async def redirect(self, request):
        redirect_file = self._check_the_file(REDIRECT_HTML)
        if not redirect_file:
            return web.HTTPFound('/error')
        valid_cookie = self._check_cookie(request)
        if not valid_cookie:
            return web.Response(text=redirect_file, content_type='text/html')
        return web.HTTPFound('/')

    async def login_page(self, request):
        login_file = self._check_the_file(LOGIN_HTML)
        if not login_file:
            return web.HTTPFound('/error')
        valid_cookie = self._check_cookie(request)
        if not valid_cookie:
            return web.Response(text=login_file, content_type='text/html')
        return web.HTTPFound('/')

    async def login(self, request):
        if not self._check_the_file(CONFIG_FILE):
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
