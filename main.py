#!/usr/bin/env python3
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
class FileReader:
    def _check_the_file(self, filename):
        self.__filename = filename
        _file = os.path.isfile(self.__filename)
        if not _file:
            print("Internal server error! file not found:{}".format(self.__filename))
            return False
        if self.__filename.endswith(".html"):
            response = open(self.__filename).read()
            return response
        elif self.__filename.endswith(".json"):
            configure_file = open(self.__filename)
            load_data = json.load(configure_file)
            try:
                if not(load_data['USERNAME'] and load_data['PASSWORD']):
                    return False
                return load_data
            except KeyError:
                print("{} doesn't have valid keys".format(self.__filename))
                return False
        else:
            message = ("{} is not in required format".format(self.__filename))
            print(message)
            return False


class Login(FileReader):
    def __init__(self):
        super().__init__()

    def _check_cookie(self, request):
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

    def _check_credentials(self):
        credentials = self._check_the_file(CONFIG_FILE)
        if not credentials:
            return False
        USERNAME = credentials['USERNAME']
        PASSWORD = credentials['PASSWORD']
        if not(self.username == USERNAME and self.password == PASSWORD):
            return False
        return True

    async def server_error(self, request):
        valid_cookie = self._check_cookie(request)
        if not valid_cookie:
            check_login_file = self._check_the_file(LOGIN_HTML)
            if not check_login_file:
                return web.Response(text=ERROR, content_type='text/html')
            return web.HTTPFound('/log')
        return web.HTTPFound('/')

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
        form = await request.post()
        self.username = form.get('username')
        self.password = form.get('password')
        if not self._check_the_file(CONFIG_FILE):
            return web.HTTPFound('/error')
        if not self._check_credentials():
            return web.HTTPFound('/redirect')
        response = web.HTTPFound('/')
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        COOKIE_EXPIRE = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
        response.set_cookie(COOKIE_NAME,
                            value=COOKIE_VALUE, expires=COOKIE_EXPIRE)
        return response


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
