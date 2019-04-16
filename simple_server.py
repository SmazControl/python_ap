import network
wlan = network.WLAN(network.AP_IF)
wlan.active(True)

import machine
pins = [machine.Pin(i, machine.Pin.IN) for i in (27, 26, 25, 33, 32, 35, 34, 23)]

html = """<!DOCTYPE html>
<html>
<head> <title>ESP32 Pins</title> </head>
<body> <h1>ESP32 Pins</h1>
<table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
</body>
</html>
"""

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
  while True:
    line = cl_file.readline()
    if not line or line == b'\r\n':
      break
  rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
  response = html % '\n'.join(rows)
  cl.send(response)
  cl.close()
