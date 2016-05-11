'''
Use Python and SQLite to gather the email addresses after 'From ' and
write the numbers of appearances of those organizations into an .sqlite file
Created on May 9, 2016
@author: course
@author: dinh
'''

import sqlite3

conn = sqlite3.connect('assignmentWeek2B.sqlite')
cur = conn.cursor()

cur.execute('''drop table if exists Counts''')
cur.execute('''create table Counts (org text, count integer)''')

filename = raw_input('Enter file name: ')
if ( len(filename) < 1 ) : filename = 'mbox.txt'
handle = open(filename)
for line in handle:
    if not line.startswith('From: ') : continue # if 'From ' not found, next line
    pieces = line.split()
    email = pieces[1] # get email address
    org = email.split('@')[1] # get organization
    
    cur.execute('select count from Counts where org = ? ', (org, ))
    row = cur.fetchone() # through the table and get that row with 'org'
    if row is None: # create new row and count 1
        cur.execute('''insert into Counts (org, count) 
                values (?, 1)''', (org, ))
    else : # find old row and increase count by 1
        cur.execute('update Counts set count = count + 1 where org = ?', 
            (org, ))
    # This statement commits outstanding changes to disk each 
    # time through the loop - the program can be made faster 
    # by moving the commit so it runs only after the loop completes
    conn.commit()

# https://www.sqlite.org/lang_select.html
# select and print 10 most frequent organizations
topTen = 'select org, count from Counts order by count desc limit 10'
print
print 'Counts:'
for row in cur.execute(topTen):
    print row[0], row[1]

conn.close()