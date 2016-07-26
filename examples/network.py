import network, micropython, gc, socket, pyb

nic = network.CC3100()
nic.connect("ssid","password")

i=0
while (i <= 20):
  i = i + 1
  print("Loop:")
  print(i)
  s=socket.socket()
  s.connect(socket.getaddrinfo('baconipsum.com',80)[0][4])
  s.send("GET /api/?type=meat-and-filler&paras=100 HTTP/1.1\r\nHost:baconipsum.com\r\nConnection: close\r\n\r\n")
  
  buf = s.recv(1024)
  while len(buf) > 0:
    print(buf)
    buf = s.recv(1024)
    pyb.delay(5)
    gc.collect()
  s.close()