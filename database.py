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

Student:
 id     | integer                  | not null
 name   | character varying(100)   | not null
 gpa    | numeric(10,2)            |
 birth  | timestamp with time zone |

Course:
 id     | integer                  | not null
 name   | character varying(100)   | not null
'''

import psycopg2 as psgre
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psgre.connect(
	dbname='postgres', 
	user='postgres',
	password='docker',
	host='localhost')

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

#cursor.execute('CREATE DATABASE test')

#cursor.execute("CREATE table student (code char(5) constraint firstkey primary key, student_name char(35), birth date)")
#DROP DATABASE [ IF EXISTS ] name
#cursor.execute('DROP DATABASE test')
cursor.close()
conn.close()