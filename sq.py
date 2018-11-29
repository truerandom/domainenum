import sqlite3

def getDBConnection(dbname):
	try:
		bd = sqlite3.connect(dbname)
		print("Base de datos abierta")
		cursor = bd.cursor()
		return bd
	except Exception as e:
		print("Problem openning the database")

def getDBCursor(bd):
	try:
		return bd.cursor()
	except Exception as e:
		print("Problem returning cursor")

def initTables(cursor):
	tables = ["CREATE TABLE IF NOT EXISTS ips(ip varchar(18) PRIMARY KEY ASC);",
		"CREATE TABLE IF NOT EXISTS sites(site varchar(200),ip,FOREIGN KEY(ip) REFERENCES ips(ip));"]
	for table in tables:
		try:
			cursor.execute(table);
		except Exception as e:
			print("Error in initTables")
			print(e)
	print("Tablas creadas correctamente")

def insertInfo(cursor,ip,site):
	queries =["INSERT OR IGNORE INTO ips VALUES('%s');" % ip,
		"INSERT INTO sites VALUES('%s','%s');" % (ip,site)]
	for q in queries:
		print(q)
		try:
			cursor.execute(q)
		except Exception as e:
			print("Error @insertInfo")
			print(e)

def closeDB(db):
	try:
		bd.commit()
	except Exception as e:
		print("Problem closing db")

ip = '132.248.124.180'
sites = ['acceso.seguridad.unam.mx','correo.seguridad.unam.mx','vpn.seguridad.unam.mx']

bd = getDBConnection('pocpoc.db')
cursor = getDBCursor(bd)
initTables(cursor)
for site in sites:
	insertInfo(cursor,ip,site)
closeDB(bd)
