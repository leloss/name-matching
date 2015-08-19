#!flask/bin/python
from train import learn
from query import match
from flask import Flask, request, send_from_directory

app = Flask(__name__, static_url_path='')

@app.route('/')
def names():
	# thread = threading.Thread(target=learn())
	# thread.start()
	# thread.daemon = True
    return app.send_static_file('index.html')

@app.route('/query/')
def query():
	query_name=request.args.get('name', '')
	res = match(query_name) 
	return str(res)

@app.route('/data/<filename>')
def serve_data(filename):
    if filename == '':
		return ''
    return send_from_directory('data', filename, as_attachment=False)


@app.route('/js/<filename>')
def serve_js(filename):
    if filename == '':
		return ''
    return send_from_directory('js', filename, as_attachment=False)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static','favicon.ico', as_attachment=False)

if __name__ == '__main__':
  app.run(debug=True)

