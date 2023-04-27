import sys
import subprocess
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        # decode JSON data
        request_data = json.loads(post_data.decode('utf-8'))
        
        # get arguments
        arg1 = request_data.get('arg1')
        arg2 = request_data.get('arg2')
        
        # run separate script with arguments
        output = subprocess.check_output(['python3', 'classifier.py', arg1])
        
        # decode output as JSON object
        response = json.loads(output)
        
        # send output as JSON response
        cleaned_response = json.dumps(response, ensure_ascii=False, indent=None).encode('utf-8')
        
        # send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(cleaned_response)

if __name__ == '__main__':
    # define server address and port
    server_address = ('', 8080)
    # create HTTP server
    httpd = HTTPServer(server_address, RequestHandler)
    # start HTTP server
    print('Starting server...')
    httpd.serve_forever()
