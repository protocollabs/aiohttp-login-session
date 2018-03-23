''' Simple aiohttp login system with default user!:
This system is built with aiohttp module.
Required Python-3 or 3+
'''

from aiohttp import web

# Customize the cookie name, value and cookie expire date
COOKIE_NAME = "OldTamil"
COOKIE_VALUE = 0
COOKIE_LIFE_TIME = 24*60*60*30

# User credentials and here we could use more users in future.
User ='Hippod'
Password = 'admin'

# Define the required host and port
HOST = '127.0.0.1'
PORT = 8080

''' cookie_check function will check for valid cookie on all pages!
Return True if there is cookie with requested name.
'''
def cookie_check(request):
    cookie = request.cookies.get(COOKIE_NAME, None)
    if cookie:
        if COOKIE_NAME == COOKIE_NAME:
            return True
        # Normal test for checking the COOKIE_NAME
        else:
            print("COOKIE_NAME has been modified!.")
    # Return False when there is no cookie at all.
    else:
        return False

# The main page of the website
async def index(request):
    Check = cookie_check(request)
    if Check is True:
        page = open('site.html').read()
        return web.Response(text=page, content_type='text/html')
    else:
        return web.HTTPFound(location='/loginpage')

# When the user is unknown or the user's cookie is expired, will redirect to login page
async def login_page(request):
    Check = cookie_check(request)
    # check for cookies in the login_page and return to main page if there is valid cookie.
    if Check is True:
        return web.HTTPFound('/')
    else:
        resp = open('login.html').read()
        return web.Response(text=resp, content_type='text/html')

# Login required if the user is new or user's cookie expired and check the user credentials.
async def login(request):
        form = await request.post()
        username = form.get('username')
        if username == User:
            password = form.get('password')
            if password == Password:
                # Give access to the index page when user enters valid credentials
                response = web.HTTPFound(location='/')
                # If the user is successfully logged in, set the cookie on the index page.
                response.set_cookie(COOKIE_NAME, value=COOKIE_VALUE, max_age=COOKIE_LIFE_TIME)
                return response
        else:
            # Here we need to implement the redirect page when the user enter invalid credentials
            # But now by default it redirects to the index page
            return web.HTTPFound(location='/')


app = web.Application()
app.router.add_get('/', index)
app.router.add_get('/loginpage', login_page)
app.router.add_post('/login', login)
web.run_app(app, host= HOST, port=PORT)
