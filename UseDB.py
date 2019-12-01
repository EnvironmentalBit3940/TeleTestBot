import postgresql
import sqlite3
import psycopg2
from datetime import datetime
#from logging import debug, info, DEBUG

class opendb:
	def del_usr(self,message):
		self.cur.execute('delete from users where id=%s;', [int(message.chat.id)])
		self.con.commit()
		self.con.close()

	def ins_user(self, message):
#		debug(f'{message.chat.id} created account')
		self.cur.execute('insert into users (id, name) values (%s);', [message.chat.id, message.text])
		self.con.commit()
		self.con.close()

	def find_name(self, message):
		self.cur.execute('select name from users where id=%s;', [message.chat.id])
		name = self.cur.fetchone()[0]
		self.con.close()
		return name

	def add_result(self, message, test, result):
		self.cur.execute('insert into users (%s) values(%s) where id=%s;', [test, result, message.chat.id])

	def __init__(self):
		self.con = psycopg2.connect("dbname=userdb")
		self.cur = self.con.cursor()
		self.cur.execute('CREATE TABLE IF NOT EXISTS Users( id Integer, name char(20), test1 Integer, test2 Integer, test3 Integer);')
		print('init')

class tests_db:
    def take_test(self, test_name, answr_id):
        if test_name == 't1':
            self.cur.execute('SELECT * FROM Test1 WHERE id=?', [answr_id])
        elif test_name == 't2':
            self.cur.execute('SELECT * FROM Test2 WHERE id=?', [answr_id])
        elif test_name == 't3':
            self.cur.execute('SELECT * FROM Test3 WHERE id=?', [answr_id])

        return self.cur.fetchone()


    def __init__(self):
        self.con = sqlite3.connect('tests.db')
        self.cur = self.con.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS Test2(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, question char(100), cor_answ char(100), answrs char(100));')
        self.cur.execute('CREATE TABLE IF NOT EXISTS Test3(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, question char(100), cor_answ char(100), answrs char(100));')
        self.cur.execute('CREATE TABLE IF NOT EXISTS Test1(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, question char(100), cor_answ char(100), answrs char(100));')

if __name__ == "__main__":

	print(opendb())
