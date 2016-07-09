### Author: EMF Badge team
### Description: A basic HTTP library, based on https://github.com/balloob/micropython-http-client
### License: MIT

import usocket
import ujson
import gc

try:
    import ussl
    SUPPORT_SSL = True
except ImportError:
    ussl = None
    SUPPORT_SSL = False

SUPPORT_TIMEOUT = hasattr(usocket.socket, 'settimeout')
CONTENT_TYPE_JSON = 'application/json'

class Response(object):
    def __init__(self):
        self.encoding = 'utf-8'
        self.headers = {}
        self.status = None
        self.content = b"";

    @property
    def text(self):
        return str(self.content, self.encoding) if self.content else ''

    def close(self):
        if self.raw is not None:
            self._content = None
            self.raw.close()
            self.raw = None

    def json(self):
        return ujson.loads(self.text)

    def raise_for_status(self):
        if 400 <= self.status_code < 500:
            raise OSError('Client error: %s' % self.status_code)
        if 500 <= self.status_code < 600:
            raise OSError('Server error: %s' % self.status_code)

def open_http_socket(method, url, json=None, timeout=None, headers=None):
    urlparts = url.split('/', 3)
    proto = urlparts[0]
    host = urlparts[2]
    urlpath = '' if len(urlparts) < 4 else urlparts[3]

    if proto == 'http:':
        port = 80
    elif proto == 'https:':
        port = 443
    else:
        raise OSError('Unsupported protocol: %s' % proto[:-1])

    if ':' in host:
        host, port = host.split(':')
        port = int(port)

    if json is not None:
        content = ujson.dumps(json)
        content_type = CONTENT_TYPE_JSON
    else:
        content = None

    ai = usocket.getaddrinfo(host, port)
    addr = ai[0][4]

    sock = usocket.socket()

    if timeout is not None:
        assert SUPPORT_TIMEOUT, 'Socket does not support timeout'
        sock.settimeout(timeout)

    sock.connect(addr)

    if proto == 'https:':
        assert SUPPORT_SSL, 'HTTPS not supported: could not find ussl'
        sock = ussl.wrap_socket(sock)

    sock.send('%s /%s HTTP/1.0\r\nHost: %s\r\n' % (method, urlpath, host))

    if headers is not None:
        for header in headers.items():
            sock.send('%s: %s\r\n' % header)

    if content is not None:
        sock.send('content-length: %s\r\n' % len(content))
        sock.send('content-type: %s\r\n' % content_type)
        sock.send('\r\n')
        sock.send(content)
    else:
        sock.send('\r\n')

    return sock

# Adapted from upip
def request(method, url, json=None, timeout=None, headers=None):
    sock = open_http_socket(method, url, json, timeout, headers)
    try:
        response = Response()
        state = 1
        hbuf = b"";
        remaining = None;
        while True:
            buf = sock.recv(1024)
            print(len(buf))
            if state == 1: # Status
                nl = buf.find(b"\n")
                if nl > -1:
                    hbuf += buf[:nl - 1]
                    response.status = int(hbuf.split(b' ')[1])
                    state = 2
                    hbuf = b"";
                    buf = buf[nl + 1:]
                else:
                    hbuf += buf

            if state == 2: # Headers
                hbuf += buf
                nl = hbuf.find(b"\n")
                while nl > -1:
                    if nl < 2:
                        if "Content-Length" not in response.headers:
                            raise Exception("No Content-Length")
                        remaining = int(response.headers["Content-Length"])
                        buf = hbuf[2:]
                        hbuf = None
                        state = 3
                        break

                    header = hbuf[:nl - 1].decode("utf8").split(':', 3)
                    response.headers[header[0].strip()] = header[1].strip()
                    hbuf = hbuf[nl + 1:]
                    nl = hbuf.find(b"\n")

            if state == 3: # Content
                response.content += buf
                remaining -= len(buf)
                if remaining < 1:
                    break

            pyb.delay(50)

        return response
    finally:
        sock.close()

def download(method, url, target, json=None, timeout=None, headers=None):
    sock = open_http_socket(method, url, json, timeout, headers)

    try:
        with open(target, 'wb') as f:
            state = 1
            hbuf = b"";
            remaining = None;
            while True:
                buf = sock.recv(1024)
                print(len(buf))
                if state == 1: # Status
                    nl = buf.find(b"\n")
                    if nl > -1:
                        hbuf += buf[:nl - 1]
                        status = hbuf.split(b' ')[1]
                        if status != b"200":
                            raise Exception("Invalid status " + str(status))

                        state = 2
                        hbuf = b"";
                        buf = buf[nl + 1:]
                    else:
                        hbuf += buf

                if state == 2: # Headers
                    hbuf += buf
                    nl = hbuf.find(b"\n")
                    while nl > -1:
                        if nl < 2:
                            if remaining == None:
                                raise Exception("No Content-Length")
                            buf = hbuf[2:]
                            hbuf = None
                            state = 3
                            break

                        header = hbuf[:nl - 1].decode("utf8").split(':', 3)
                        if header[0] == "Content-Length":
                            remaining = int(header[1].strip())

                        hbuf = hbuf[nl + 1:]
                        nl = hbuf.find(b"\n")

                if state == 3: # Content
                    f.write(buf)
                    remaining -= len(buf)
                    if remaining < 1:
                        break

                pyb.delay(50)
    finally:
        sock.close()

def get(url, **kwargs):
    return request('GET', url, **kwargs)

def post(url, **kwargs):
    return request('POST', url, **kwargs)

