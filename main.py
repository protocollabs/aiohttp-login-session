from aiohttp import web


COOKIE_NAME = "kerla"


async def index(request):
    cookie = request.cookies.get(COOKIE_NAME, None)
    if cookie:
        page = open('site.html').read()
        return web.Response(text=page, content_type='text/html')
    else:
        return web.HTTPFound(location='/loginpage')


async def login_page(request):
    resp = open('login.html').read()
    return web.Response(text=resp, content_type='text/html')


async def login(request):
    form = await request.post()
    username = form.get('username')
    if username == 'hippod':
        password = form.get('password')
        if password == 'admin':
            response = web.HTTPFound(location='/')
            # set a cookie valid for 30 days long.
            response.set_cookie(COOKIE_NAME, value=0, path='/', max_age=24*60*60*30)
            return response
    # Redirect to login page
    return web.HTTPFound(location='/')


app = web.Application()
app.router.add_get('/', index)
app.router.add_get('/loginpage', login_page)
app.router.add_post('/login', index)
web.run_app(app, host='127.0.0.1', port=8080)