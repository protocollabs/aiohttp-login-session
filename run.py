#!/usr/bin/env python3
import os
import datetime
import json
from aiohttp import web


COOKIE_NAME = "OldTamil"
COOKIE_VALUE = 0
HOST = "localhost"
PORT = 8080

TEMPLATES = "app/templates/"

CONFIG_FILE = 'configuration.json'


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


class Login:

    def _check_the_file(self, filename):
        if not os.path.isfile(filename):
            print("Internal server error! "
                  "file not found:{}".format(filename))
            return False
        return True

    def _load_html_file(self, filename):
        if not self._check_the_file(filename):
            return False
        if not filename.endswith(".html"):
            print("{} is not html file".format(filename))
            return False
        return open(filename).read()

    def _load_credentials(self, filename):

        if not self._check_the_file(filename):
            return False
        if not filename.endswith(".json"):
            print("{} is not a json file.".format(filename))
            return False
        configure_file = open(filename)
        load_json_data = json.load(configure_file)
        if not all(key in load_json_data for key in("USERNAME", "PASSWORD")):
            return False
        return load_json_data

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

    def _check_credentials(self, username, password):
        credentials = self._load_credentials(CONFIG_FILE)
        if not credentials:
            return False
        authorized_username = credentials['USERNAME']
        authorized_password = credentials['PASSWORD']
        if not (username == authorized_username and
                password == authorized_password):
            return False
        return True

    async def server_error(self, request):
        return web.Response(text=ERROR, content_type='text/html')

    async def home_page(self, request):
        site_file = self._load_html_file(os.path.join(TEMPLATES, "site.html"))
        if not site_file:
            return web.HTTPFound('/error')
        valid_cookie = self._check_cookie(request)
        if not valid_cookie:
            return web.HTTPFound('/log')
        return web.Response(text=site_file, content_type='text/html')

    async def redirect_page(self, request):
        redirect_file = self._load_html_file(os.path.join(TEMPLATES, "redirect.html"))
        if not redirect_file:
            return web.HTTPFound('/error')
        valid_cookie = self._check_cookie(request)
        if not valid_cookie:
            return web.Response(text=redirect_file, content_type='text/html')
        return web.HTTPFound('/')

    async def login_page(self, request):
        login_file = self._load_html_file(os.path.join(TEMPLATES, "login.html"))
        if not login_file:
            return web.HTTPFound('/error')
        valid_cookie = self._check_cookie(request)
        if not valid_cookie:
            return web.Response(text=login_file, content_type='text/html')
        return web.HTTPFound('/')

    async def login_required(self, request):
        if not self._load_credentials(CONFIG_FILE):
            return web.HTTPFound('/error')
        form = await request.post()
        username = form.get('username')
        password = form.get('password')
        if not self._check_credentials(username, password):
            return web.HTTPFound('/redirect')
        time_ = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        cookie_expiry_date = time_.strftime("%a, %d %b %Y %H:%M:%S GMT")
        response = web.HTTPFound('/')
        response.set_cookie(COOKIE_NAME,
                            value=COOKIE_VALUE, expires=cookie_expiry_date)
        return response


def aiohttp_login():
    app = web.Application()
    login = Login()
    app.router.add_routes([web.get('/log', login.login_page),
                           web.post('/login', login.login_required),
                           web.get('/', login.home_page),
                           web.get('/error', login.server_error),
                           web.get('/redirect', login.redirect_page)])
    return web.run_app(app, host=HOST, port=PORT)


if __name__ == '__main__':
    aiohttp_login()