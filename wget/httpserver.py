import BaseHTTPServer, sys

hex_data = ""

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	# define what to do with GET requests
	def do_GET(s):
		global hex_data
		s.send_response(200)
	  	hex_data = s.path[2:]
	def log_message(self, format, *args):
        	return

# receive some hex data and convert it to ascii
def keep_running():
	global hex_data
	if hex_data == "66696e65": # stop
		hex_data = ""
		return False
	else:
		try:
			data = hex_data.decode("hex")
			sys.stdout.write(data)
		except Exception, e:
			print "\nException: "+str(e)		
		return True

# listen on 0.0.0.0:80 till hex_data is not empty
def listen():
	httpd = BaseHTTPServer.HTTPServer(('', 80), MyHandler)
	while keep_running():
		httpd.handle_request()
