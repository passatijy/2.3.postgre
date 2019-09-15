'''
def create_db(): # создает таблицы
	pass

def get_students(course_id): # возвращает студентов определенного курса
	pass

def add_students(course_id, students): # создает студентов и 
									   # записывает их на курс
	pass


def add_student(student): # просто создает студента
	pass

def get_student(student_id):
	pass


'''
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

def get_student(student_id):
	pass

def add_students(connstr):
	print("input students as list of dicts [{'name':'Ivan Petrov','gpa':'5.1','birthdate':'2016-06-22 22:10:25-04','course':'1'},{}]")
	stud = input('Enter there: ')
	try:
		studlist = ast.literal_eval(stud)
	except Exception as error:
		print('Something goes wrong,', error)
	#print('Studlist: ', studlist, 'type:', type(studlist))
	for k in studlist:
		execstring = execstring = 'INSERT INTO student(name, gpa, birth) VALUES ' + "('" + studdict['name'] +"','" + studdict['gpa'] + "','" + studdict['birthdate'] + "');" 
		some_sql_action(connstr, execstring)


def add_student(connstr):
	''' Input student name, gpa, birth date with timezone as dict 
	{'name':'Ivan Petrov','gpa':'5.1','birthdate':'2016-06-22 22:10:25-04'}
	'''
	print("input student as dict {'name':'Ivan Petrov','gpa':'5.1','birthdate':'2016-06-22 22:10:25-04','course':'1'}")
	stud = input('Enter there: ')
	try:
		studdict = ast.literal_eval(stud)
	except Exception as error:
		print('Something goes wrong,', error)
	execstring = 'INSERT INTO student(name, gpa, birth) VALUES ' + "('" + studdict['name'] +"','" + studdict['gpa'] + "','" + studdict['birthdate'] + "');" 
	some_sql_action(connstr, execstring)

def listdb(connstr):
	execstring = 'SELECT * from pg_catalog.pg_database ;'
	result = some_sql_action(connstr, execstring)
	return result

def main_repeater(conn, dbname):
	operate_spec = {
	'database':dbname, 
	'user':'postgres',
	'password':'docker',
	'host':'localhost'}

	repeat = True
	while repeat:
		command = input('  Введите команду (n-newdb,d-deldb,l-listdb,s-showone stud,a-addonestud;p - add list of studs; h - помощь; q - выход) ')
		if command == 'q' :
			repeat = False
			break
		elif command == 'h' :
			print('no help')
		elif command == 'n':
			print('making new db with name:', dbname)
			print('conn: ', conn)
			print('operate_spec:', operate_spec)
			createdb(conn, dbname)
			spec2 = '(id serial PRIMARY KEY, name varchar(100) NOT NULL)'
			print('Create table course')
			createtable(operate_spec,"course",spec2)
			spec = '(id serial PRIMARY KEY, name varchar(100) NOT NULL, gpa numeric(10,2),birth timestamp, course_id integer )'
			print('Create table student')
			createtable(operate_spec,"student",spec)
			spec3 = "INSERT into course (name) values ('math'),('physics'),('biology');"
			some_sql_action(operate_spec,spec3)
			spec4 = 'ALTER table public.student ADD CONSTRAINT course_constr_id FOREIGN KEY (course_id) REFERENCES course (id);'
			some_sql_action(operate_spec,spec4)
		elif command == 'd':
			dbname = input('Db to remove: ')
			print('removing db', dbname)
			dropdb(conn, dbname)
		elif command == 's':
			k = get_all_students(operate_spec)
			for st in k:
				print('Student name:', st)
		elif command == 'l':
			listdb_list = listdb(conn)
			for k in listdb_list:
				print('Database name:', k[0])
		elif command == 'a':
			add_student(operate_spec)
		elif command == 'p':
			add_students(operate_spec)
		else:
			print('  Нет такой команды. Попробуйте еще.')

'''
Student:
 id     | integer                  | not null
 name   | character varying(100)   | not null
 gpa    | numeric(10,2)            |
 birth  | timestamp with time zone |

Course:
 id     | integer                  | not null
 name   | character varying(100)   | not null'''

if __name__ == '__main__':
	init_spec = {
	'database':'postgres', 
	'user':'postgres',
	'password':'docker',
	'host':'localhost'}

	tmpdbname = databasename(suffixes, prefixes)
	main_repeater(init_spec, tmpdbname)
