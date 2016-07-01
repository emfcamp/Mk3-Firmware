##################
# http_client.py #
##################

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
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content
        self.encoding = 'utf-8'

    @property
    def text(self):
        content = self.content

        return str(content, self.encoding) if content else ''

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

# Returns http status line
# Supports \n, \r and \r\n
def read_http_status(buffer):
    i = buffer.find(b"\n")
    j = buffer.find(b"\r")
    if i == -1 and j == -1:
        raise OSError('Invalid HTTP status header')
    if i == -1:
        j = i
    else:
        if j != -1:
            i = min(i, j)

    line = str(buffer[:i], 'utf-8')

    return line

# Returns index of first http content byte, skipping all headers
def get_content_index(buffer):
    indexes = [
        buffer.find(b"\n\n"),
        buffer.find(b"\r\r"),
        buffer.find(b"\r\n\r\n")
    ]

    indexes = [ index for index in indexes if index > -1 ] # remove -1s

    if len(indexes) == 0:
        raise OSError('Invalid HTTP response, no double newline found')

    i = min(indexes) + 2
    if buffer[i:i+2] == b"\r\n":
        i += 2
    return i

# Adapted from upip
def request(method, url, json=None, timeout=None, headers=None):
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

    # Consume the whole response
    buffer = sock.recv(1024)
    while True:
        received = sock.recv(1024)
        if len(received) == 0:
            break
        buffer += received

    # Read status line
    protover, status, msg = read_http_status(buffer).split(None, 2)

    content_index = get_content_index(buffer)

    # Return response object
    return Response(int(status), buffer[content_index:])

def download(method, url, target, json=None, timeout=None, headers=None):
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

    # write to disk
    # todo: skip headers
    with open(target, 'wb') as output:
        while True:
            received = sock.recv(1024)
            if len(received) == 0:
                break
            output.write(received)



def get(url, **kwargs):
    return request('GET', url, **kwargs)


def post(url, **kwargs):
    return request('POST', url, **kwargs)