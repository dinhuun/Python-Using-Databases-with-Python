'''
Use XML to parse a roster .json file of users and courses and
use SQLite to write their tables plus a junction (many-to-many) table in an .sqlite file
Created on May 10, 2016
@author: course
@author: dinh
'''

import json
import sqlite3

conn = sqlite3.connect('assignmentWeek4.sqlite')
cur = conn.cursor()

# Make new tables using executescript()
cur.executescript('''
drop table if exists User;
drop table if exists Member;
drop table if exists Course;

create table User (
    id     integer not null primary key autoincrement unique,
    name   text unique
);

create table Course (
    id     integer not null primary key autoincrement unique,
    title  text unique
);

create table Member (
    user_id     integer,
    course_id   integer,
    role        integer,
    primary key (user_id, course_id)
)
''')

filename = raw_input('Enter file name: ')
if (len(filename) < 1): filename = 'roster.json'

# use JSON to gather all data as list
# [
#   ["Charley", "si110", 1],
#   ["Mea", "si110", 0],
dataStrings = open(filename).read()
data = json.loads(dataStrings)

for entry in data:
    
    name = entry[0];
    title = entry[1];
    role = entry[2];
    print name, title, role

    # write into User table
    cur.execute('''insert or ignore into User (name) values (?)''', (name, ))
    cur.execute('select id from User where name = ?', (name, ))
    user_id = cur.fetchone()[0]

    # write into Course table
    cur.execute('''insert or ignore into Course (title) values (?)''', (title, ))
    cur.execute('select id from Course where title = ?', (title, ))
    course_id = cur.fetchone()[0]

    # write into Member table
    cur.execute('''insert or replace into Member
                (user_id, course_id, role) values (?, ?, ?)''', (user_id, course_id, role))

    # write immediately
    conn.commit()

topTen = '''SELECT hex(User.name || Course.title || Member.role ) AS X
            FROM User JOIN Member JOIN Course 
            ON User.id = Member.user_id AND Member.course_id = Course.id
            ORDER BY X LIMIT 5'''
print
print 'Results:'
for row in cur.execute(topTen):
    print row
# results
# 1 | 416261696765616C736933333430
# 2 | 416264697261686D616E736933333430
# 3 | 416272696C736933363430
# 4 | 416465656E61736933303130
# 5 | 4164696C736931303630
    
conn.close()