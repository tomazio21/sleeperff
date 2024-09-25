import urllib.request
import urllib.parse

def get(url, params=None, headers=None): 
    if params != None:
        urlEncodedParams =  urllib.parse.urlencode(params)
        url = url + urlEncodedParams
    req = urllib.request.Request(url)
    if headers != None:
        for name, value in headers.items():
            req.add_header(name, value)
    response = urllib.request.urlopen(req)
    return response

def post(url, params, headers=None, json=False):
    req = urllib.request.Request(url)
    data = ''
    if json == False:
        params = urllib.parse.urlencode(params)
    if headers != None:
        for name, value in headers.items():
            req.add_header(name, value)
    data = params.encode('utf-8')
    response = urllib.request.urlopen(req, data)
    return response
