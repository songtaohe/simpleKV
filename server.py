from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import pickle 
import json 
import os 
import logging


class S(BaseHTTPRequestHandler):
	def _set_response(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):
		#logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
		self._set_response()
		self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

	def do_POST(self):
		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length) # <--- Gets the data itself
		# logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\n\n",
		# 		str(self.path), str(self.headers))

		if os.path.isfile("data.p"):
			dataset = pickle.load(open("data.p","rb"))
		else:
			dataset = {}

		#try:
		data = json.loads(post_data.decode('utf-8'))
		result = ""

		if data["cmd"] == "set":
			k = data["key"]
			v = data["value"]

			dataset[k] = v 

			print("set", k, v)

		elif data["cmd"] == "get":
			k = data["key"]
			if k in dataset:
				result = [True, dataset[k]]
			else:
				result = [False,""]

			print("get", result)

		pickle.dump(dataset, open("data.p", "wb"))

		return_str = json.dumps(result)

		self._set_response()
		self.wfile.write(return_str.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
	logging.basicConfig(level=logging.INFO)
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	logging.info('Starting httpd...\n')
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	logging.info('Stopping httpd...\n')

if __name__ == '__main__':
	from sys import argv
	# 8006
	if len(argv) == 2:
		run(port=int(argv[1]))
	else:
		run()

