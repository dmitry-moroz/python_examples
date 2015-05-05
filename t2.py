import time
import subprocess
import sys
import urllib
import BaseHTTPServer
from urlparse import urlparse
from SocketServer import ThreadingMixIn


HOST_NAME = 'localhost'
PORT_NUMBER = 8080


def get_handler(path):
    def new_func(func):
        MyHandler.SIDE_HANDLERS.update({path: func})
        return func
    return new_func


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler, object):

    SHELL = u'/shell'
    CODING = 'UTF-8'

    SIDE_HANDLERS = {}

    def __init__(self, *args, **kwargs):
        object.__init__(self)
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
        MyHandler.collect_handlers()

    @staticmethod
    def collect_handlers():
        """Collects handlers from subclasses.
        """
        for cls in MyHandler.__subclasses__():
            if '__url__' in dir(cls) and 'get_handler' in dir(cls):
                MyHandler.SIDE_HANDLERS.update({cls.__url__: cls.get_handler})

    def run_cmd(self, cmd):
        """Performs command into subprocess routine and returns stdout,
        stderr and return code.

        cmd: target command for performing
        """
        cmd = cmd.encode(sys.stdin.encoding)
        process_cmd = subprocess.Popen(cmd, shell=True,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)

        output, stderr = process_cmd.communicate()
        return (output.decode(sys.stdout.encoding),
                stderr.decode(sys.stdout.encoding),
                process_cmd.returncode)

    def response(self, code, data=None):
        """Sends specified return code and provides header.

        code: return status for sending
        """
        self.send_response(code)
        self.send_header("Content-type",
                         "text/html; charset={0}".format(self.CODING))
        self.end_headers()
        if data is not None:
            self.wfile.write(data.encode(self.CODING))

    def do_GET(self):
        """Respond to a GET request.
        """
        request = urllib.unquote(self.path).decode('UTF-8')
        request = urlparse(request)
        if request.path == self.SHELL:
            out, err, code = self.run_cmd(request.params)
            if not code:
                self.response(200, out)
            else:
                self.response(418)
        elif request.path in MyHandler.SIDE_HANDLERS:
            try:
                result = MyHandler.SIDE_HANDLERS[request.path]()
                self.response(200, str(result))
            except:
                self.response(500)
        else:
            self.response(404)


class ThreadedHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """Handle requests in a separate thread.
    """
    pass


def run():
    httpd = ThreadedHTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - {0}:{1}".format(HOST_NAME,
                                                           PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - {0}:{1}".format(HOST_NAME,
                                                          PORT_NUMBER)
