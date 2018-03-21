from aiohttp import web
import time

COOKIE_NAME = "default"

async def index(request):
    cookie = request.cookies.get(COOKIE_NAME, None)
    if cookie and cookie_valid(cookie):
        page = open('site.html').read()
        return web.Response(text=page, content_type='text/html')
    else:
        return web.HTTPFound(location='/loginpage')

def cookie_valid(cookie):
    if time.time() - cookie < 60 * 60 * 24:
        # cookie older then 1 day
        return False
    else:
        return True

async def login_page(request):
    resp = open('login.html').read()
    return web.Response(text=resp, content_type='text/html')

def cookie_create():
    """
    retuns a base64 encoded value of the cookie creation
    time and  it with key key
    """
    t = str(time.time())

def cookie_demarshall(cookie):
    """
    return time as float, cookie is converted from
    base74 to binary,  and converted to float
    """
    return


async def login(request):
    form = await request.post()
    username = form.get('username')
    if username == 'hippod':
        password = form.get('password')
        if password == 'admin':
            response = web.HTTPFound(location='/')
            response.set_cookie('default', value=cookie_create(), max_age=1, path='/')
            return response
    else:
        resp = web.HTTPFound(location='/loginpage')
        return resp

app = web.Application()
app.router.add_get('/', index)
app.router.add_get('/loginpage', login_page)
app.router.add_post('/login', login)
web.run_app(app, host='127.0.0.1', port=8080)