#!/usr/bin/env python3

import os
import cgi
import pickle
import re
from mimetypes import guess_type
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from pattern.en import tokenize
from keras.preprocessing import sequence
from keras.models import load_model
LBL = ('Negative', "Positive")

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        pos = self.path.find('?')
        if pos != -1:
            self.path = self.path[0:pos]
        self.path = 'www/' + self.path.strip('/')
        if os.path.isdir(self.path):
            self.path += '/index.html'
        if not os.path.exists(self.path):
            self.send_response(404)
            self.end_headers()
            return 404
        mime = guess_type(self.path)[0]
        if mime is None:
            mime = 'text/plain'
        self.send_response(200)
        self.send_header("Content-type", mime)
        self.end_headers()
        return 200
    
    def do_GET(self):
        status = self.do_HEAD()
        if status == 404:
            return status
        try:
            with open(self.path, 'rb') as f:
                self.wfile.write(f.read())
        except Exception:
            self.wfile.write(bytes('Error', encoding='utf8'))
        return status
    
    def do_POST(self):
        form = cgi.FieldStorage(
            fp = self.rfile,
            headers = self.headers,
            environ = {'REQUEST_METHOD': 'POST',
                       'CONTENT_TYPE': self.headers['Content-Type'],
                      }
        )
        if self.path != '/predict' or 'text' not in form.keys():
            self.send_response(404)
            self.end_headers()
            return 404
        self.send_response(200)
        self.send_header("Content-type", 'text/plain')
        self.end_headers()
        text = ' '.join(tokenize(re.sub('([a-z][.!?]+)([A-Z])', '\g<1> \g<2>',
                                        form['text'].value, 0))).lower().split()
        x = [[w2indx.get(word, 0) for word in text]]
        x = sequence.pad_sequences(x, maxlen = 200, padding='post', truncating='post')
        predict = model.predict_classes(x)[0][0]
        self.wfile.write(bytes(LBL[predict], encoding='utf8'))
        return 200

def run(server_class = HTTPServer, handler_class = BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open('w2indx.pkl', 'rb') as f:
    w2indx = pickle.load(f)
model = load_model('lstm.h5')
print('Data loaded. Starting server...')
run(handler_class = MyRequestHandler)