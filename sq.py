import sqlite3
def getDBCursor(dbname):
	try:
		bd = sqlite3.connect(dbname)
		print("Base de datos abierta")
		cursor = bd.cursor()
		return cursor
	except Exception as e:
		print("Problem openning the database")

def initTables(cursor):
	tables = ["CREATE TABLE IF NOT EXISTS ips(ip varchar(18));","CREATE TABLE IF NOT EXISTS sites(site varchar(200));"]
	for table in tables:
		try:
			cursor.execute(tabla);
		except Exception as e:
			print("Error in initTables")
	print("Tablas creadas correctamente")

def insertInfo(cursor,ip,site):
	q = 'INSERT INTO 
ip = '132.248.124.180'
sites = ['acceso.seguridad.unam.mx','correo.seguridad.unam.mx','vpn.seguridad.unam.mx']

cursor = getDBCursor('pocpoc.db')
initTables(cursor)


