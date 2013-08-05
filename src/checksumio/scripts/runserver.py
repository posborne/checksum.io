from checksumio import make_checksumio_wsgiapp
from wsgiref.simple_server import make_server


def runserver():
    app = make_checksumio_wsgiapp()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()


if __name__ == '__main__':
    runserver()
