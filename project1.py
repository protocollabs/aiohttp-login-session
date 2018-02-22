from aiohttp import web


async def index(request):
    return web.Response(text='Hello world!')


app = web.Application()
app.router.add_get('/', index)      # port 8080  0.0.0.0.1
web.run_app(app)
