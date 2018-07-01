import network
wlan = network.WLAN(network.AP_IF)
wlan.active(True)

def getParams(url):
    if len(url.split("?")) == 1: return ""
    params = url.split("?")[1]
    params = params.split('=')
    pairs = zip(params[0::2], params[1::2])
    answer = dict((k,v.split(" ")[0]) for k,v in pairs)
    return answer

import machine
pins = [machine.Pin(i, machine.Pin.IN) for i in (27, 26, 25, 33, 32, 35, 34, 23)]

html = """<!DOCTYPE html>
<html>
    <head> <title>ESP32 Pins</title> </head>
    <body> 
	<table border="0"> <tr><td>
	<form action="" method="GET">
		<textarea cols="40" rows="20" name="prog"></textarea><br>
		<input type="submit" value="Submit">
	</form></td>
"""
html2 = """
	<h1>ESP32 Pins</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""
import os
import socket
addr = socket.getaddrinfo('192.168.4.1', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    html3 = """
	    <td>
	    <canvas id="myCanvas" width="200" height="100"
		style="border:1px solid #c3c3c3;">
		Your browser does not support the canvas element.
	    </canvas>
	    <script>
		var canvas = document.getElementById("myCanvas");
		var ctx = canvas.getContext("2d");
	    """
    while True:
        line = cl_file.readline()
	print(line)
        if not line or line == b'\r\n':
            break
	text = line.decode('utf-8')
	if text[:3] == 'GET':
	    prog = getParams(text)
	    if len(prog) > 0:
		if prog['prog'] != '':
			print(prog)
			code = prog['prog']
			code = code.replace('+',' ')
			code = code.replace('print','output = output+"<br>"+str')
			code = code.replace('canvas','ctx = ctx+" "+str')
			code = code.replace('%22','"')
			code = code.replace('%23','#')
			code = code.replace('%27',"'")
			code = code.replace('%28','(')
			code = code.replace('%29',')')
			code = code.replace('%2B','+')
			code = code.replace('%2C',',')
			code = code.replace('%3A',':')
			code = code.replace('%3B',';')
			code = code.replace('%3D','=')
			
			code = code.replace('%0D%0A','\n')
			code = 'output =""\nctx=""\n'+code
			file = open('prog.py' ,'w')
			file.write(code)
			file.close()
    if len([item for item in os.listdir() if item=='prog.py'])>0:
   	try:
		output = ""
		ctx = ""
		execfile('prog.py')
		html3 = html3 + ctx + '</script>' + output +'<br>'
    	except SyntaxError as err:
		html3 = html3 + '</script>' + err.args[0] + '<br>'
    html4 = html + html3 + '</td></tr></table><br>' + html2
    rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
    response = html4 % '\n'.join(rows)
    cl.send(response)
    cl.close()
