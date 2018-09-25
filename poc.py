import requests
import time
from stem import Signal
from stem.control import Controller

"""
SocksPort 9050 # Default: Bind to localhost:9050 for local connections.
SocksPort 127.0.0.1:9100 # Bind to this address:port too.
"""
def get_tor_session():
	session = requests.session()
	# Tor uses the 9050 port as the default socks port
	session.proxies = {'http':  'socks5://127.0.0.1:9050','https': 'socks5://127.0.0.1:9050'}
	return session

def renewIP():
	print 'entre a renew ip'
	try:
		with Controller.from_port(port = 9051) as controller:
			controller.authenticate()
			controller.signal(Signal.NEWNYM)
	except Exception as e:
		print 'Oie no '
		print e
	print 'sali de renew ip'

# Make a request through the Tor connection
# IP visible through Tor
session = get_tor_session()
print(session.get("http://httpbin.org/ip").text)
# Above should print an IP different than your public IP

# Following prints your normal public IP
print(requests.get("http://httpbin.org/ip").text)


renewIP()
session = get_tor_session()
time.sleep(4)
print(session.get("http://httpbin.org/ip").text)
