import codecs
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from twilio.twiml.voice_response import Play, VoiceResponse
from modules import settings
from socketserver import ThreadingMixIn


class RequestHandler(BaseHTTPRequestHandler):
    """
    Class for handling get requests to the server.
    """

    def do_POST(self):
        """
        Handle POST request.
        """

        if self.path == '/play':
            
            # Return the TWIML XML.
            type = 'text/xml'
            self.send_response(200)
            self.send_header('Content-type', type)
            self.end_headers()
            self.wfile.write(str.encode(self.play()))

        else:
            self.send_error(404)

        return

    def do_GET(self):
        """
        Handle GET request.
        """

        if self.path.lstrip('/').endswith('.mp3'):

            # Return the MP3 File to be played
            type = 'audio/mpeg'
            if os.path.isfile(self.path.lstrip('/')):
                self.send_response(200)
                self.send_header('Content-type', type)
                self.end_headers()
                with open('call.mp3', 'rb') as file:
                    self.wfile.write(file.read())

            else:
                self.send_error(404)

        else:
            self.send_error(404)

        return

    def play(self):
        """
        Return valid TwiML to Twilio for call.
        """
        response = VoiceResponse()
        response.play('http://%s:%s/call.mp3' % (settings.ROOT_URL, settings.PORT))
        return str(response)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """
    Class for threading the basic HTTPServer.
    Available by default in Python 3.7 onwards, 
    but since this is built for Python 3.5 must be
    created. 
    """

def run(server=ThreadedHTTPServer, handler=RequestHandler, port=settings.PORT):
    address = ('', port)
    httpd = server(address, handler)
    print('Starting server...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()