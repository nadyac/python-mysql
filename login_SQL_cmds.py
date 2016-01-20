# loginPythonSQL.py

#import the connector module and print function and errorcode
from __future__ import print_function
from mysql.connector import errorcode
import mysql.connector

DB_NAME = 'USERS'
#create database
def create_database(cursor):
	try:
		cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
	except mysql.connector.Error as err:
		print("Failed creating database: {}".format(err))
        exit(1)
def create_tables():
	print("Creating tables.")
	TABLES = {}
	TABLES['login'] = (
						"CREATE TABLE `login` (" 
						"`username` varchar(14) NOT NULL,"
						"`password` varchar(14) NOT NULL,"
						"PRIMARY KEY(`username`)"
						")	ENGINE=InnoDB")
	#iterate through the tables in the tables dictionary
	for tableName, ddlStatements in TABLES.iteritems():
		try:
			print("Creating table " + tableName.format(tableName), end='')
			cursor.execute(ddlStatements) #cursor interprets and executes ddl SQL statements
		except mysql.connector.Error as Err:
			if Err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
				print("Table " + tableName + " already exists.")
			else:
				print(Err.msg)
		else:
			print(" OK.")
def insert_record(username, password, tableName, cursor):
	#if the user doesn't exist, add them to the table
	addUser = (
				"	INSERT INTO " + tableName +
				"	(username,password)"
				"	VALUES (%s, %s)"
			  )
	newUser = (username, password)

	cursor.execute(addUser, newUser)
	print("Inserted new record.")

#connect to the database using username, password, host, database.
try:
	cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='USERS')
	cursor = cnx.cursor()
	print("Made connection.")

#if there is an error connecting to the database, throw an error
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Could not connect to database with the given credentials.")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("It seems that database does not exist. Will create it.")
		cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1')
		cursor = cnx.cursor()
		create_database(cursor)
	else:
		# if not error with credentials or db existence, then print out err
		print(err)

#create tables dictionary and add tables to DB if they don't exist.
create_tables()
insert_record('Nadya','password123','login',cursor)

#commit changes and close the connection.
cnx.commit()
cursor.close()
cnx.close()
