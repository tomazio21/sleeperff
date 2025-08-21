import urllib.request
import urllib.parse
import json

def get(url, params=None, headers=None):
    if params is not None:
        urlEncodedParams = urllib.parse.urlencode(params)
        url = url + urlEncodedParams
    req = urllib.request.Request(url)
    if headers is not None:
        for name, value in headers.items():
            req.add_header(name, value)
    response = urllib.request.urlopen(req)
    return response


def post(url, data, headers=None):
    req = urllib.request.Request(url, method="POST")
    if headers is not None:
        for name, value in headers.items():
            req.add_header(name, value)
    data = json.dumps(data)
    data = data.encode()
    response = urllib.request.urlopen(req, data=data)
    return response
