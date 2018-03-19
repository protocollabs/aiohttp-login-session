"""A simple aiohttp login server with default username and password!
Pure python!
"""
import base64
from cryptography import fernet
from aiohttp import web
import aiohttp_jinja2
import jinja2
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_session import session_middleware


# The home page
async def homepage(request):
    resp = aiohttp_jinja2.render_template('index.html', request, context={})
    return resp


# Login required
async def login(request):

    resp = web.HTTPFound(location='/')
    resp.set_cookie('session_cookie', 'secret', max_age=50)  # Set a cookie on the client side. 
    form = await request.post()
    username = form.get('username')
    if username == 'hippod':
        password = form.get('password')
        if password == 'admin':
            response = aiohttp_jinja2.render_template('site.html', request, context={})
            return response
    return resp                                  # Redirect to the login page. 

# Web app 
fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)

# Using jinja2 framework 
app = web.Application(middlewares=[session_middleware(EncryptedCookieStorage(secret_key, cookie_name='session_cookie'))])
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('/aiohttp Login'))          # Templates loader

# Router
app.router.add_get('/', homepage)
app.router.add_post('/login', login)


web.run_app(app, host='127.0.0.1', port=8080)
