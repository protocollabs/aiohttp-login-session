from views import index, input1


def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/', input1)
    

