'''
Use XML to parse an iTunes .xml file of songs and
use SQLite to write their attributes into corresponding tables in an .sqlite file
Created on May 9, 2016
@author: course
@author: dinh
'''

import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('assignmentWeek3.sqlite')
cur = conn.cursor()

# Make new tables using executescript()
cur.executescript('''
drop table if exists Artist;
drop table if exists Genre;
drop table if exists Album;
drop table if exists Track;

create table Artist (
    id    integer not null primary key autoincrement unique,
    name  text unique
);

create table Genre (
    id    integer not null primary key autoincrement unique,
    name  text unique
);

create table Album (
    id            integer not null primary key autoincrement unique,
    artist_id     integer,
    title text    unique
);

create table Track (
    id        integer not null primary key autoincrement unique,
    title     text unique,
    album_id  integer,
    genre_id  integer,
    len       integer,
    rating    integer,
    count     integer
);
''')

filename = raw_input('Enter filename: ')
if (len(filename) < 1): filename = 'tracks.xml'

# sample data
# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>

# helper function looks up and returns text of node with tag == 'key' and text == key
def lookup(d, key):
    found = False
    for child in d:
        if found: return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None

# use ET to gather all data as tree
data = ET.parse(filename)
songs = data.findall('dict/dict/dict')
print 'Number of songs', len(songs)
for song in songs: 
    if(lookup(song, 'Track ID') is None): continue
    
    artist = lookup(song, 'Artist')
    genre = lookup(song, 'Genre')
    album = lookup(song, 'Album')
    name = lookup(song, 'Name')
    length = lookup(song, 'Total Time')
    rating = lookup(song, 'Rating')
    count = lookup(song, 'Play Count')
    
    # if informatio is missing, discard
    if name is None or artist is None or album is None or genre is None: continue
    
    print name, artist, album, length, rating, count
    
    # write into Artist table
    cur.execute('''insert or ignore into Artist (name) values (?)''', (artist, ))
    cur.execute('select id from Artist where name = ?', (artist, ))
    artist_id = cur.fetchone()[0]
    
    # write into Genre table
    cur.execute('''insert or ignore into Genre (name) values (?)''', (genre, ))
    cur.execute('select id from Genre where name = ?', (genre, ))
    genre_id = cur.fetchone()[0]
    
    # write into Album table
    cur.execute('''insert or ignore into Album (title, artist_id)
                values (?, ?)''', (album, artist_id))
    cur.execute('select id from Album where title = ?', (album, ))
    album_id = cur.fetchone()[0]
    
    # write into Track table
    cur.execute('''insert or replace into Track (title, album_id, genre_id, len, rating, count)
                values (?, ?, ?, ?, ?, ?)''', (name, album_id, genre_id, length, rating, count))
    
    # write immediately
    conn.commit()

conn.close()