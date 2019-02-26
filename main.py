from src import server, client
import sys, os, socket
from optparse import OptionParser
import logging

def argv_error(usage):
    logging.error(usage)
    os._exit(-1)

if __name__=='__main__':
    usage = """usage: %prog [options]
    ex1) %prog --client -i 192.168.0.1 -p 65500
    ex2) %prog --server -i 127.0.0.1 -p 65500 --disable-show
    """

    if len(sys.argv) <= 1:
        argv_error(usage)
    
    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--client", dest="is_client", action="store_true",
                      help="set client mode", default=False)
    parser.add_option("-s", "--server", dest="is_server", action="store_true",
                      help="set server mode", default=False)
    parser.add_option("-d", "--disable-show", dest="is_enable_show", action="store_false",
                      help="disable open the slide show when you startup the server", default=True)
    parser.add_option("-i", "--ip", dest="ip", action="store", type="string",
                      help="set IPv4 number(not support the IPv6)",
                      default=str(socket.gethostbyname(socket.gethostname())))
    parser.add_option("-p","--port", dest="port", action="store", type="int",
                      help="set the port number(default:65500)", default=65500)

    options, args = parser.parse_args()

    if options.is_client and options.is_server:
        argv_error(usage)
    elif options.is_client:
        client.run(options.ip, options.port)
    elif options.is_server:
        server.run(options.ip, options.port, options.is_enable_show)
    else:
        argv_error(usage)