import argparse

import cherrypy

from sale.wsgi import application


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, action='store', dest='port', help='Port to attach server')
    parser.add_argument('--certfile', type=str, action='store', dest='certfile',
                        help='SSL certificate to attach server')
    parser.add_argument('--keyfile', type=str, action='store', dest='keyfile',
                        help='SSL private key to to attach server')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    print("Your app is running at 0.0.0.0:%s" % args.port)

    # disable auto reload
    cherrypy.config.update({'engine.autoreload.on': False})

    # Mount the application
    cherrypy.tree.graft(application, "/")

    # Unsubscribe the default server
    cherrypy.server.unsubscribe()

    # Instantiate a new server object
    server = cherrypy._cpserver.Server()

    # Configure the server object
    server.socket_host = '0.0.0.0'
    server.socket_port = args.port
    server.thread_pool = 50

    # For SSL Support
    if args.certfile:
        # server.ssl_module = 'pyopenssl'
        server.ssl_certificate = args.certfile
        server.ssl_private_key = args.keyfile

    # Subscribe this server
    server.subscribe()

    # Start the server engine (Option 1 *and* 2)

    cherrypy.engine.start()
    cherrypy.engine.block()
