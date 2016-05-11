'''
Use Python and SQLite to write a simple table into .sqlite file
and execute a command
Created on May 9, 2016
@author: course
@author: dinh
'''

import sqlite3

conn = sqlite3.connect('assignmentWeek2A.sqlite')
cur = conn.cursor()

# Make new table using execute()
cur.execute('drop table if exists Ages')
cur.execute('CREATE table Ages (name varchar(128), age integer)')
cur.execute('DELETE from Ages')
cur.execute('insert into Ages (name, age) values (?,?)', ('Glenn', 24))
cur.execute('insert into Ages (name, age) values (?,?)', ('Dustin', 37))
cur.execute('insert into Ages (name, age) values (?,?)', ('Corran', 28))
cur.execute('insert into Ages (name, age) values (?,?)', ('Nikiya', 13))
conn.commit()

# execute SQLite select command and print result
l = 'select hex(name || age) AS X from Ages ORDER BY X'
for row in cur.execute(l):
    print row

# results:
# 1 | 436F7272616E3238
# 2 | 44757374696E3337
# 3 | 476C656E6E3234
# 4 | 4E696B6979613133

conn.close()