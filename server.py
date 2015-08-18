#!flask/bin/python
#import os
from train import learn
from query import match
from flask import Flask, request, send_from_directory
#import threading
#import json

server = Flask(__name__, static_url_path='')
#server= application

# @server.route('/')
# def root():
# 	return server.send_static_file('index.html')

@server.route('/')
def names():
	# thread = threading.Thread(target=learn())
	# thread.start()
	# thread.daemon = True
    return server.send_static_file('index.html')

@server.route('/query/')
def query():
	query_name=request.args.get('name', '')
	res = match(query_name) 
	return str(res)

@server.route('/data/<filename>')
def serve_data(filename):
    if filename == '':
		return ''
    return send_from_directory('data', filename, as_attachment=False)


@server.route('/js/<filename>')
def serve_js(filename):
    if filename == '':
		return ''
    return send_from_directory('js', filename, as_attachment=False)


if __name__ == '__main__':
  server.run(debug=True)

