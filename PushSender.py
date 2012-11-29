# -*- coding: utf-8 -*-
__author__ = 'Dariusz Aniszewski,Polidea'
import ssl,socket,struct,simplejson

class PushSender():
    ssl_connection = None
    notifications = []
    sandbox = False
    sandbox_host = ( "gateway.sandbox.push.apple.com", 2195 )
    production_host = ( "gateway.push.apple.com", 2195 )
    verbose = True
    def __init__(self,certificate_file,sandbox=False,verbose=True):
        self.ssl_connection = ssl.wrap_socket( socket.socket(), certfile = certificate_file )
        self.sandbox = sandbox
        self.verbose = verbose
        if self.verbose:
            print "Initiate PushSender"
            print "Using cert: %s" % certificate_file
            print "Using sandbox: %s" % sandbox

    def _connect(self):
        if self.sandbox:
            host = self.sandbox_host
        else:
            host = self.production_host
        self.ssl_connection.connect( host )
        if self.verbose:
            print "Connected to %s at port %s" % (host[0],host[1])

    def _disconnect(self):
        self.ssl_connection.close()
        if self.verbose:
            print "Connection closed"

    def _write(self,data):
        self.ssl_connection.write( data )


    def addNotification(self,payload_dict,device_token):
        if None in [payload_dict,device_token]:
            raise ValueError("wrong params")
        self.notifications.append((payload_dict,device_token))

    def push(self):
        if len(self.notifications) == 0:
            if self.verbose:
                print "Nothing to push"
            return
        self._connect()
        for notification in self.notifications:
            payload = simplejson.dumps(notification[0])
            if self.verbose:
                print "Sending %s to %s" % (payload,notification[1])
            token = bytes(notification[1].decode('hex'))
            format = "!BH32sH%ds" % len(payload)
            push = struct.pack( format, 0, 32, token, len(payload), payload )
            self._write(push)
        self._disconnect()

