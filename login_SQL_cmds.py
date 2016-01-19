# loginPythonSQL.py

#import the connector module and print function and errorcode
from __future__ import print_function
from mysql.connector import errorcode
import mysql.connector

DB_NAME = 'users_db'
#create database
def create_database(cursor):
	try:
		cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
	except mysql.connector.Error as err:
		print("Failed creating database: {}".format(err))
        exit(1)

#connect to the database using username, password, host, database.
try:
	cnx = mysql.connector.connect(user='[username]', password='[password]', host='127.0.0.1', database='[db_name]')
	cursor = cnx.cursor()
	print("Made connection.")

#if there is an error connecting to the database, throw an error
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Could not connect to database with the given credentials.")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("It seems that database does not exist. Will create it.")
		cnx = mysql.connector.connect(user='[user]', password='[password]', host='127.0.0.1')
		cursor = cnx.cursor()
		create_database(cursor)
	else:
		# if not error with credentials or db existence, then print out err
		print(err)

#create tables dictionary

#create tables if they don't exist.

#close the connection.
cursor.close()
cnx.close()
