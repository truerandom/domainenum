import requests
import time
from stem import Signal
from stem.control import Controller
import sqlite3

"""
SocksPort 9050 # Default: Bind to localhost:9050 for local connections.
SocksPort 127.0.0.1:9100 # Bind to this address:port too.
"""
class DomainEnum:
	def __init__(self,dbname):
		self.dbman = DBManager(dbname)
		self.dbman.initTables()
		self.session = self.get_tor_session()

	"""
	Gets a new tor session
	"""
	def get_tor_session(self):
		session = requests.session()
		# Tor uses the 9050 port as the default socks port
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
			if 'No DNS A records' in ht_response[0]:
				return False
			return True
		return False

class DBManager:
	def __init__(self,dbname):
		self.db = self.getDBConnection(dbname)
		self.cursor = self.getDBCursor()

	def getDBConnection(self,dbname):
		try:
			bd = sqlite3.connect(dbname)
			return bd
		except Exception as e:
			print("Problem openning the database")
			print(e)

	def getDBCursor(self):
		try:
			return self.db.cursor()
		except Exception as e:
			print("Problem returning cursor")
			print(e)

	def initTables(self):
		tables = ["CREATE TABLE IF NOT EXISTS ips(ip varchar(18) PRIMARY KEY ASC);",
			"CREATE TABLE IF NOT EXISTS sites(site varchar(200) PRIMARY KEY ASC ,ip,FOREIGN KEY(ip) REFERENCES ips(ip));"]
		for table in tables:
			try:
				self.cursor.execute(table);
			except Exception as e:
				print("Error in initTables")
				print(e)

	def insertInfo(self,ip,site):
		if len(site) > 0:
			queries =["INSERT OR IGNORE INTO ips VALUES('%s');" % ip,
				"INSERT INTO sites VALUES('%s','%s');" % (ip,site)]
			for q in queries:
				#print(q)
				try:
					self.cursor.execute(q)
				except Exception as e:
					print("Error @insertInfo")
					print(e)

	def closeDB(self):
		try:
			self.db.commit()
		except Exception as e:
			print("Problem closing db")
			print(e)
			
			
# Make a request through the Tor connection
# IP visible through Tor
domenum = DomainEnum('unamsites.db')
print 'Requesting info with ip %s ' % domenum.getIP()
for i in range(90,100):
	cur_ip = '132.248.124.%s' % i
	domains = domenum.getDomains(cur_ip) 
	print cur_ip
	print '\n'.join(domains)
	if domenum.domainsFound(domains):
		for dom in domains:
			domenum.dbman.insertInfo(cur_ip,dom)
domenum.dbman.closeDB()
