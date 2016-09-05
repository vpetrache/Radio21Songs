import urllib2
import json
import MySQLdb
from datetime import datetime

def create_db():
    con = MySQLdb.connect("localhost", "root" , "")
    cur = con.cursor()
    cur.execute('CREATE database radio21;')
    print "schema created"
    con.close()

def create_table():
    con = MySQLdb.connect("localhost", "root", "", "radio21")
    cur = con.cursor()
    cur.execute('CREATE TABLE `songs` (\n  `idsongs` int(11) NOT NULL AUTO_INCREMENT,\n  `artist` mediumtext,\n  `song` mediumtext,\n  `time` mediumtext,\n  PRIMARY KEY (`idsongs`),\n  UNIQUE KEY `idsongs_UNIQUE` (`idsongs`)\n) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=latin1;')
    print "table created"
    con.close()

def insert(artist, song, rotime):
    db = MySQLdb.connect("localhost","root","", "radio21")
    cursor = db.cursor()
    sql = """INSERT INTO songs(artist, song, time)
             VALUES ('%s', '%s','%s')""" % \
          (artist, song, rotime)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()

def get_db_song():
    db = MySQLdb.connect("localhost","root","", "radio21")
    cursor = db.cursor()
    sql = "SELECT song from songs order by time desc limit 1"

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            dbsong = row[0]
            return dbsong
    except:
        print "Error: unable to fetch data"

    db.close()

def daily_songs(day):
    db = MySQLdb.connect("localhost","root","", "radio21")
    i= day + '%'
    cursor = db.cursor()
    sql = "SELECT artist, song, time from songs where time like ('%s') order by time desc" % \
          (i)

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except:
        print "Error: unable to fetch data"

    db.close()

def get_local_time():
    rotime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return rotime

def get_song(url):
    # try:
        response = urllib2.urlopen(url).read()
        return json.loads(response)
    # except Exception as a:
    #     print a