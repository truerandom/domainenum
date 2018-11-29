import requests
import time
from stem import Signal
from stem.control import Controller

"""
SocksPort 9050 # Default: Bind to localhost:9050 for local connections.
SocksPort 127.0.0.1:9100 # Bind to this address:port too.
"""
class DomainEnum:
	def __init__(self):
		print 'en init'
		self.session = self.get_tor_session()
		# Tor uses the 9050 port as the default socks port

	"""
	Gets a new tor session
	"""
	def get_tor_session(self):
		session = requests.session()
		session.proxies = {'http':  'socks5://127.0.0.1:9050','https': 'socks5://127.0.0.1:9050'}
		return session 

	"""
	Renew ip of the domainenum object
	"""
	def renewIP(self):
		self.session = self.get_tor_session()
		try:
			with Controller.from_port(port = 9051) as controller:
				controller.authenticate()
				controller.signal(Signal.NEWNYM)
		except Exception as e:
			print e
		time.sleep(2)
		
	"""
	Get current ip
	"""
	def getIP(self):
		myip = self.session.get("http://httpbin.org/ip").text
		myip = myip.replace('\n','').replace('\r\n','').replace('{','').replace('}','').split(':')[1]
		return myip

	"""
	Get ip's domains from hacker target
	"""
	def getIPDomains(self,ip):
		try:
			content = self.session.get('https://api.hackertarget.com/reverseiplookup/?q=%s' % ip)
			return content.text
		except Exception as e:
			print "Couldn't get the domain info for ip %s" % ip
			return None
	"""
	Returns True if the quota is exceeded or an error ocurred
	"""
	def quotaExceeded(self,content):
		if content is not None and len(content) > 0:
			if 'API count exceeded' in content:
				return True
			return False
		return True
	
	"""
	Requests ip's domains until obtained
	"""
	def getDomains(self,ip):
		continue_requests = True
		while continue_requests:
			ht_response = domenum.getIPDomains(ip)
			if not domenum.quotaExceeded(ht_response):
				return ht_response.split('\n')
			else:
				domenum.renewIP()
				print '[i] ip changed to %s ' % domenum.getIP()

	def domainsFound(self,ht_response):
		if ht_response is not None and len(ht_response) >0:
			if 'No DNS A records found for' in ht_response:
				return False
			return True
		return False

# Make a request through the Tor connection
# IP visible through Tor
domenum = DomainEnum()
print 'Requesting info with ip %s ' % domenum.getIP()
for i in range(0,255):
	cur_ip = '132.248.124.%s' % i
	dominfo = domenum.getDomains(cur_ip) 
	print cur_ip
	if domenum.domainsFound(dominfo):
		print '\n'.join(dominfo)

