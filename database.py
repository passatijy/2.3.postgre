from random import randrange,choice
import psycopg2 
import ast
from psycopg2.sql import SQL, Identifier
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
prefixes = ('apple','peach','grass','mellon','cucumber')
suffixes = ('green','blue','red','yellow','white','black','orange')

def some_sql_action(conspec, action):
	try:
		connection = psycopg2.connect(user=conspec['user'],
									password=conspec['password'],
									host=conspec['host'],
									database=conspec['database'])
		connection.autocommit = True
		cursor = connection.cursor()
		cursor.execute(action)
		if 'SELECT' in action:
			result = cursor.fetchall() 
		else:
			result = None
	except (Exception, psycopg2.Error) as error :
		print ("Error while fetching data from PostgreSQL", error)
		result = None
	finally:
	#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
	return result

def databasename(pref,suff):
	dbname = choice(pref) + choice(suff) + str(randrange(0,9)) + str(randrange(0,9))
	return dbname

def createdb(connstr,dbname):
	execstring = 'CREATE DATABASE' + ' ' + dbname + ';'
	some_sql_action(connstr, execstring)


def createtable(connstr, tablename, tablespec):
	execstring = 'CREATE TABLE ' + tablename + tablespec + ';'
	print('Creating table')
	some_sql_action(connstr, execstring)


def dropdb(connstr, dbname):
	execstring = 'DROP DATABASE' + ' ' + dbname + ';'
	some_sql_action(connstr, execstring)

def get_all_students(connstr):
	execstring = 'SELECT * from student;'
	result = some_sql_action(connstr, execstring)
	return result

def get_student(connstr, student_id):
	execstring = 'SELECT * from student WHERE id =' + student_id +';'
	result = some_sql_action(connstr, execstring)
	return result

def get_student_by_course(connstr, course_id):
	execstring = 'SELECT * from student WHERE course_id =' + course_id +';'
	result = some_sql_action(connstr, execstring)
	return result

def add_students(connstr, studs):
	print('studs_type:', type(studs))
	print('studs: ', studs)
	for k in studs:
		execstring = 'INSERT INTO student(name, gpa, birth, course_id) VALUES ' + "('" + k['name'] +"','" + k['gpa'] + "','" + k['birthdate'] + "','" + k['course'] + "');" 
		some_sql_action(connstr, execstring)

def add_student(connstr, stud):
	''' Input student name, gpa, birth date with timezone as dict 
	{'name':'Ivan Petrov','gpa':'5.1','birthdate':'2016-06-22 22:10:25-04'}
	'''
	execstring = 'INSERT INTO student(name, gpa, birth) VALUES ' + "('" + stud['name'] +"','" + stud['gpa'] + "','" + stud['birthdate'] + "');" 
	some_sql_action(connstr, execstring)

def listdb(connstr):
	execstring = 'SELECT * from pg_catalog.pg_database ;'
	result = some_sql_action(connstr, execstring)
	return result

def main_repeater(conn, dbname, onestud, studlistdict, searchstudid, searchcourseid):
	op_conn = {
	'database':dbname, 
	'user':'postgres',
	'password':'postgres',
	'host':'localhost'}

	print('-----Lets--start-----')
	print('main connector:', conn)
	print('opr. connector:', op_conn)
	print('making new db with name:', dbname)
	createdb(conn, dbname)

	print('-----Creating--tables-----')
	spec2 = '(id serial PRIMARY KEY, name varchar(100) NOT NULL)'
	print('Create table course')
	createtable(op_conn,"course",spec2)

	spec = '(id serial PRIMARY KEY, name varchar(100) NOT NULL, gpa numeric(10,2),birth timestamp, course_id integer )'
	print('Create table student')
	createtable(op_conn,"student",spec)

	spec3 = "INSERT into course (name) values ('math'),('physics'),('biology');"
	some_sql_action(op_conn,spec3)

	spec4 = 'ALTER table public.student ADD CONSTRAINT course_constr_id FOREIGN KEY (course_id) REFERENCES course (id);'
	some_sql_action(op_conn,spec4)
	input('press "enter" key to continue(you can verify db and tables from another window with psql)')

	print('-----List-of-databases-----')
	listdb_list = listdb(conn)
	for k in listdb_list:
		print('Database name:', k[0])

	print('-----Adding--one--student-----')
	add_student(op_conn, onestud)
	print('-----Adding--list--of--students-----')
	add_students(op_conn, studlistdict)
	print('-----All--students-----')
	k = get_all_students(op_conn)
	for st in k:
		print('Student name:', st)

	print('-----Find student with id=2-----')
	print('Found student:', get_student(op_conn, searchstudid))

	print('-----Find all students with course_id=2-----')
	print('Found students:', get_student_by_course(op_conn,searchcourseid))

	input('All done, after "enter" key pressing the database will be dropped')
	input('Shure? Press "enter" key to continue')

	print('removing db', dbname)
	dropdb(conn, dbname)



if __name__ == '__main__':
	init_spec = {
	'database':'postgres', 
	'user':'postgres',
	'password':'postgres',
	'host':'localhost'}
	o_stud = {'name':'Kons Uk','gpa':'3.1','birthdate':'199-03-13 22:10:25-04','course':2}
	m_stud = [
	{'name':'Ol Petr','gpa':'6.1','birthdate':'2005-07-22 22:10:25-04','course':'2'},
	{'name':'In Kols','gpa':'3.2','birthdate':'2002-03-10 23:10:25-04','course':'2'},
	{'name':'Serg Iv','gpa':'5.2','birthdate':'2009-06-22 22:10:25-04','course':'3'},
	{'name':'Sash Ol','gpa':'4.3','birthdate':'2001-06-24 22:10:25-04','course':'1'}]

	tmpdbname = databasename(suffixes, prefixes)
	main_repeater(init_spec, tmpdbname, o_stud, m_stud, '2', '2')