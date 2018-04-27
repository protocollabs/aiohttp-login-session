# aiohttp-login-session
# Aiohttp server with login mechanism. 


## Introduction:
![all text](https://github.com/muthuubalakan/aiohttp-login-session/blob/master/login.png)

A aiohttp server with login mechanism. This is a login system purely implemented on asyncio and aiohttp.
It has user interface html pages and data contains configuration file by default. 

## Installation:
aiohttp-login-session requires [Python3](https://www.python.org/download/releases/3.0/) or higher version to run.
You are recommended to install [aiohttp](https://aiohttp.readthedocs.io/en/stable/)

Pip install:
```sh
$ pip install aiohttp
```

### Info:
The system handles **GET** and **POST** requests and gives html responses. 
A cookie handling function has been implemented safely and It helps the server to protect its functions. 

### Error handling:
Login system can be easily cutomized to handle Bad requests. 
Single function error handling has been used for **Internal server error**.

#### 404 Not Found - Error handling with middlewares


```sh

# Define 404 html page 
not_found_page = open("sample404.html").read()

@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        if response.status != 404:
            return response
        message = response.message
    except web.HTTPException as ex:
        if ex.status != 404:
            raise
         return True
    return web.Response(text=not_found_page, content_type='text/html')

app = web.Application(middlewares=[error_middleware])
```

### Useful documents:
Aiohttp is a asyncio framework. You can find more information about aiohttp here http://aiohttp.readthedocs.io/en/stable/
For Asyncio, please refer python 3.5 document https://docs.python.org/3/library/asyncio.html

### Further Info:
aiohttp login model designed with default credentials.

Verify the deployment by navigating to your server address in your preferred browser.

```sh
127.0.0.1:8080
```
