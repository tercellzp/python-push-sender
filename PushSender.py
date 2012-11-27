# -*- coding: utf-8 -*-
__author__ = 'Dariusz Aniszewski,Polidea'
import ssl,socket,struct,simplejson

class PushSender():
    ssl_connection = None
    notifications = []
    sandbox = False
    sandbox_host = ( "gateway.sandbox.push.apple.com", 2195 )
    production_host = ( "gateway.push.apple.com", 2195 )
    def __init__(self,certificate_file,sandbox=False):
        self.ssl_connection = ssl.wrap_socket( socket.socket(), certfile = certificate_file )
        self.sandbox = sandbox

    def _connect(self):
        if self.sandbox:
            self.ssl_connection.connect( self.sandbox_host )
        else:
            self.ssl_connection.connect( self.production_host )

    def _disconnect(self):
        self.ssl_connection.close()

    def _write(self,data):
        self.ssl_connection.write( data )


    def addNotification(self,payload_dict,device_token):
        if None in [payload_dict,device_token]:
            raise ValueError("wrong params")
        self.notifications.append((payload_dict,device_token))

    def push(self):
        self._connect()
        for notification in self.notifications:
            payload = simplejson.dumps(notification[0])
            token = bytes(notification[1].decode('hex'))
            format = "!BH32sH%ds" % len(payload)
            push = struct.pack( format, 0, 32, token, len(payload), payload )
            self._write(push)
        self._disconnect()

