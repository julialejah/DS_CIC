
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
import time
import threading

import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()



class myPing (threading.Thread):
   def __init__(self, src,dest,pcks):
      threading.Thread.__init__(self)
      self.src = src
      self.dest = dest
      self.pcks = pcks
   def run(self):
   	print 'inicia ping desde ',self.src.IP()
   	print '******.......................******'
   	print self.src.cmd('ping -c ',self.pcks,' ',self.dest.IP(),' &')
      
class myHPing3  (threading.Thread):
   def __init__(self,src,dest,pcks,data):
      threading.Thread.__init__(self)
      self.src = src
      self.dest = dest
      self.pcks = pcks
      self.data = data
   def run(self):
   	print 'inicia hping desde ',self.src.IP()
   	print '**********************************************'
   	print self.src.cmd('hping3 -V --rand-source --flood ',self.dest.IP(),' &')

net = Mininet(host=CPULimitedHost,link=TCLink)

c0=net.addController()
h1 = net.addHost( 'h1' )
h2 = net.addHost( 'h2' )
h3 = net.addHost( 'h3' )
h4 = net.addHost( 'h4' )
h5 = net.addHost( 'h5' )
h6 = net.addHost( 'h6' )
h7 = net.addHost( 'h7' )
h8 = net.addHost( 'h8' )
h9 = net.addHost( 'h9' )
h0 = net.addHost( 'h0' )
hClient = net.addHost( 'hClient' )
hServer = net.addHost( 'hServer' )

s1 = net.addSwitch ('s1' )
s2 = net.addSwitch ( 's2' )

bw=1

net.addLink( s1, h1 , bw=bw)
net.addLink( s1, h2 , bw=bw)
net.addLink( s1, h3 , bw=bw)
net.addLink( s1, h7 , bw=bw)
net.addLink( s1, h9 , bw=bw)
net.addLink( s1, hClient , bw=bw)
net.addLink( s1, s2, bw=1, max_queue_size=50)
net.addLink( s2, h4 , bw=bw)
net.addLink( s2, h5 , bw=bw)
net.addLink( s2, h6 , bw=bw)
net.addLink( s1, h8 , bw=bw)
net.addLink( s1, h0 , bw=bw)
net.addLink( s2, hServer, bw=bw )
#delay, loss

net.start()

net.iperf ((hClient, hServer))


print "-----------------------------------------------------------------------"

thread1 = myPing(h1,h4,10)
thread2 = myHPing3(h3,h5,100,1400)
thread3 = myHPing3(h2,h5,100,1400)
thread4 = myHPing3(h7,h8,100,1400)
thread5 = myHPing3(h9,h0,100,1400)

thread1.start()
print "-----------------------1 hping---------------------------"
net.iperf((hClient,hServer))

thread2.start()
print "-----------------------2 hping---------------------------"
net.iperf((hClient,hServer))

thread3.start()
print "-----------------------3 hping---------------------------"
net.iperf((hClient,hServer))

thread4.start()
print "-----------------------4 hping---------------------------"
net.iperf((hClient,hServer))

thread5.start()
print "-----------------------5 hping---------------------------"
net.iperf((hClient,hServer))
#net.pingAll()
#print h3.cmd('ping -c 5 %s' % h4.IP())
#print h1.cmd( 'ping localhost' )
#h2.cmd('hping3 -V -1 -d 1400 --faster %s' % h5.IP())
net.stop()
