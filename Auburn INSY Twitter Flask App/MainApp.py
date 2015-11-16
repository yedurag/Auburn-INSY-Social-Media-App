from flask import *

from twython import Twython
from twython import TwythonStreamer
from collections import Iterable
import jinja2.ext
import json
import webbrowser
import sqlite3
import datetime
import re
import threading
from textblob import TextBlob
import ssl
import sys
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

reload(sys)  
sys.setdefaultencoding('utf8')


Windowmarker = 1


Beginning = datetime.datetime.now()
Beginning2 = datetime.datetime.now()

ws = []
Number_tweets = 0






############### Intial db setup ###########################


conn1 = sqlite3.connect('C:\Auburn INSY Twitter App Access Folder\AuburnINSYTwitterApp.db')

with conn1:
	print datetime.datetime.now().isoformat(' ')
	cur1 = conn1.cursor()
	
	cur1.execute("CREATE TABLE IF NOT EXISTS Tweet_tableprimary(Tweet TEXT, [Timestamp] timestamp,Timestamp_second TEXT, Timestamp_minute TEXT, Timestamp_hour TEXT, Created_at TEXT, Screen_name TEXT, Sentiment REAL, Latitude REAL, Longitude REAL, Place TEXT, Id_string TEXT)")
	cur1.execute("CREATE TABLE IF NOT EXISTS Tweet_tablesecondary(Tweet TEXT, [Timestamp] timestamp,Timestamp_second TEXT, Timestamp_minute TEXT, Timestamp_hour TEXT, Created_at TEXT, Screen_name TEXT, Sentiment REAL, Latitude REAL, Longitude REAL, Place TEXT, Id_string TEXT, Track_1 INTEGER, Track_2 INTEGER, Track_3 INTEGER, Track_4 INTEGER, Track_5 INTEGER, Track_6 INTEGER)")
	
	cur1.execute("CREATE TABLE IF NOT EXISTS Tweet_tracks(Track_1 TEXT, Track_2 TEXT, Track_3 TEXT, Track_4 TEXT, Track_5 TEXT, Track_6 TEXT, Track_name1 TEXT, Track_name2 TEXT, Track_name3 TEXT, Track_name4 TEXT, Track_name5 TEXT, Track_name6 TEXT)")
	cur1.execute("CREATE TABLE IF NOT EXISTS Tweet_minutestats(Timestamp_minute TEXT, Track_1_count INTEGER, Track_2_count INTEGER, Track_3_count INTEGER, Track_4_count INTEGER, Track_5_count INTEGER, Track_6_count INTEGER, Track_1_sentiment REAL, Track_2_sentiment REAL, Track_3_sentiment REAL, Track_4_sentiment REAL, Track_5_sentiment REAL, Track_6_sentiment REAL)")
	cur1.execute("CREATE TABLE IF NOT EXISTS Tweet_hourstats(Timestamp_hours TEXT, Track_1_count INTEGER, Track_2_count INTEGER, Track_3_count INTEGER, Track_4_count INTEGER, Track_5_count INTEGER, Track_6_count INTEGER, Track_1_sentiment REAL, Track_2_sentiment REAL, Track_3_sentiment REAL, Track_4_sentiment REAL, Track_5_sentiment REAL, Track_6_sentiment REAL)")
	cur1.execute("CREATE TABLE IF NOT EXISTS Tweet_secondstats(Timestamp_second TEXT, Track_1_count INTEGER, Track_2_count INTEGER, Track_3_count INTEGER, Track_4_count INTEGER, Track_5_count INTEGER, Track_6_count INTEGER, Track_1_sentiment REAL, Track_2_sentiment REAL, Track_3_sentiment REAL, Track_4_sentiment REAL, Track_5_sentiment REAL, Track_6_sentiment REAL)")
	cur1.execute("CREATE TABLE IF NOT EXISTS Tweet_Spacial_Track1(Tweet TEXT,Timestamp_second TEXT, Screen_name TEXT, Sentiment REAL, Latitude REAL, Longitude REAL, Place TEXT,Track_1 INTEGER)")
	cur1.execute("CREATE TABLE IF NOT EXISTS Tweet_Spacial_Track2(Tweet TEXT,Timestamp_second TEXT, Screen_name TEXT, Sentiment REAL, Latitude REAL, Longitude REAL, Place TEXT,Track_2 INTEGER)")
	cur1.execute("CREATE TABLE IF NOT EXISTS Tweet_Spacial_Track3(Tweet TEXT,Timestamp_second TEXT, Screen_name TEXT, Sentiment REAL, Latitude REAL, Longitude REAL, Place TEXT,Track_3 INTEGER)")
	cur1.execute("CREATE TABLE IF NOT EXISTS Tweet_Spacial_Track4(Tweet TEXT,Timestamp_second TEXT, Screen_name TEXT, Sentiment REAL, Latitude REAL, Longitude REAL, Place TEXT,Track_4 INTEGER)")
	cur1.execute("CREATE TABLE IF NOT EXISTS Tweet_Spacial_Track5(Tweet TEXT,Timestamp_second TEXT, Screen_name TEXT, Sentiment REAL, Latitude REAL, Longitude REAL, Place TEXT,Track_5 INTEGER)")
	cur1.execute("CREATE TABLE IF NOT EXISTS Tweet_Spacial_Track6(Tweet TEXT,Timestamp_second TEXT, Screen_name TEXT, Sentiment REAL, Latitude REAL, Longitude REAL, Place TEXT,Track_6 INTEGER)")
	cur1.close
	conn1.close
	print datetime.datetime.now().isoformat(' ')
	print "Setting up db done"

###########################################################
###########################################################


########### App config for flask ##########################



app = Flask(__name__)
app.secret_key='8oFrGj9au99UNu7sJbK1WQ7VLKhu5Nto'




########### Helper Functions ##############################

#db connector#

def Dbconnector():
	Conn = sqlite3.connect('C:\Auburn INSY Twitter App Access Folder\AuburnINSYTwitterApp.db')
	Conn.text_factory = str
	Cursor = Conn.cursor()
	return (Cursor, Conn)
	
	
##############To clear the db's and to take necessary stats ######


def Querying_clearing():
	global Windowmarker
	cursor, conn = Dbconnector()
	cursor.execute("select Track_1, Track_2, Track_3, Track_4, Track_5, Track_6 from Tweet_tracks")
	
	tracklist = [dict(Track_1 = row[0], Track_2 = row[1], Track_3 = row[2], Track_4 = row[3], Track_5 = row[4], Track_6 = row[5]) for row in cursor.fetchall()]
	Track_1 = ""
	Track_2 = ""
	Track_3 = ""
	Track_4 = ""
	Track_5 = ""
	Track_6 = ""
	
		
		
	for trackdict in tracklist:
		Track_1 = trackdict["Track_1"]
		Track_2 = trackdict["Track_2"]
		Track_3 = trackdict["Track_3"]
		Track_4 = trackdict["Track_4"]
		Track_5 = trackdict["Track_5"]
		Track_6 = trackdict["Track_6"]
	
	Tracklist1 = [x.strip() for x in Track_1.split(',')]
	Tracklist2 = [x.strip() for x in Track_2.split(',')]
	Tracklist3 = [x.strip() for x in Track_3.split(',')]
	Tracklist4 = [x.strip() for x in Track_4.split(',')]
	Tracklist5 = [x.strip() for x in Track_5.split(',')]
	Tracklist6 = [x.strip() for x in Track_6.split(',')]
	
	Windowbreak = datetime.datetime.now() - datetime.timedelta(minutes=Windowmarker)
	Windowbreak2 = datetime.datetime.now() - datetime.timedelta(minutes=(Windowmarker+5))
	Windowbreak3 = datetime.datetime.now() - datetime.timedelta(minutes=(Windowmarker+1440))
	Windowbreak4 = datetime.datetime.now() - datetime.timedelta(minutes=(Windowmarker+1440))
	Windowbreak5 = datetime.datetime.now() - datetime.timedelta(minutes=(Windowmarker+60))
	
	Window = Windowbreak.isoformat(' ')
	Window2 = Windowbreak2.isoformat(' ')
	Window3 = Windowbreak3.strftime('%Y-%m-%d %H:%M')
	Window4 = Windowbreak4.strftime('%Y-%m-%d %H')
	Window5 = Windowbreak5.strftime('%Y-%m-%d %H:%M:%S')
	Window6 = Windowbreak2.strftime('%Y-%m-%d %H:%M:%S')
	cursor.execute("SELECT * FROM Tweet_tableprimary WHERE [Timestamp]<?", (Window,))
	
	tweetlistfromprimary = [[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]] for row in cursor.fetchall()]
	
	cursor.execute("DELETE FROM Tweet_tableprimary WHERE [Timestamp]<?", (Window,))
	
	conn.commit()
	if tweetlistfromprimary != []:
		if Tracklist1 == ['']:
			for k in tweetlistfromprimary:
				k.append(0)
		
		
		else:
			for k in tweetlistfromprimary:
				if any(word.lower() in k[0].lower() for word in Tracklist1):
					k.append(1)
				else:
					k.append(0)
	
		if Tracklist2 == ['']:
			for k in tweetlistfromprimary:
				k.append(0)
		
		
		else:
			for k in tweetlistfromprimary:
				if any(word.lower() in k[0].lower() for word in Tracklist2):
					k.append(1)
				else:
					k.append(0)
				
		if Tracklist3 == ['']:
			for k in tweetlistfromprimary:
				k.append(0)
		
		
		else:
			for k in tweetlistfromprimary:
				if any(word.lower() in k[0].lower() for word in Tracklist3):
					k.append(1)
				else:
					k.append(0)
				
		if Tracklist4 == ['']:
			for k in tweetlistfromprimary:
				k.append(0)
		
		
		else:
			for k in tweetlistfromprimary:
				if any(word.lower() in k[0].lower() for word in Tracklist4):
					k.append(1)
				else:
					k.append(0)
				
		if Tracklist5 == ['']:
			for k in tweetlistfromprimary:
				k.append(0)
		
		
		else:
			for k in tweetlistfromprimary:
				if any(word.lower() in k[0].lower() for word in Tracklist5):
					k.append(1)
				else:
					k.append(0)
		if Tracklist6 == ['']:
			for k in tweetlistfromprimary:
				k.append(0)
		
		
		else:
			for k in tweetlistfromprimary:
				if any(word.lower() in k[0].lower() for word in Tracklist6):
					k.append(1)
				else:
					k.append(0)
	
	if 	tweetlistfromprimary != []:		
		
		cursor.executemany('insert into Tweet_tablesecondary values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', tweetlistfromprimary)
		conn.commit()
	cursor.execute("SELECT Timestamp_minute, sum(Track_1), sum(Track_2), sum(Track_3), sum(Track_4), sum(Track_5), sum(Track_6), sum(Track_1*Sentiment)/sum(Track_1), sum(Track_2*Sentiment)/sum(Track_2), sum(Track_3*Sentiment)/sum(Track_3),sum(Track_4*Sentiment)/sum(Track_4),sum(Track_5*Sentiment)/sum(Track_5),sum(Track_6*Sentiment)/sum(Track_6) FROM Tweet_tablesecondary WHERE [Timestamp]<? GROUP BY Timestamp_minute", (Window2,))
	
	tweetminstatsfromsecondary = [[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]] for row in cursor.fetchall()]
	cursor.execute("SELECT Timestamp_hour, sum(Track_1), sum(Track_2), sum(Track_3), sum(Track_4), sum(Track_5), sum(Track_6), sum(Track_1*Sentiment)/sum(Track_1), sum(Track_2*Sentiment)/sum(Track_2), sum(Track_3*Sentiment)/sum(Track_3),sum(Track_4*Sentiment)/sum(Track_4),sum(Track_5*Sentiment)/sum(Track_5),sum(Track_6*Sentiment)/sum(Track_6)  FROM Tweet_tablesecondary WHERE [Timestamp]<? GROUP BY Timestamp_hour", (Window2,))
	tweethourstatsfromsecondary = [[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]] for row in cursor.fetchall()]
	cursor.execute("SELECT Timestamp_second, sum(Track_1), sum(Track_2), sum(Track_3), sum(Track_4), sum(Track_5), sum(Track_6), sum(Track_1*Sentiment)/sum(Track_1), sum(Track_2*Sentiment)/sum(Track_2), sum(Track_3*Sentiment)/sum(Track_3),sum(Track_4*Sentiment)/sum(Track_4),sum(Track_5*Sentiment)/sum(Track_5),sum(Track_6*Sentiment)/sum(Track_6) FROM Tweet_tablesecondary WHERE [Timestamp]<? GROUP BY Timestamp_second", (Window2,))
	tweetsecstatsfromsecondary = [[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]] for row in cursor.fetchall()]
	
	cursor.execute("SELECT Timestamp_minute, sum(Track_1), sum(Track_2), sum(Track_3), sum(Track_4), sum(Track_5), sum(Track_6), sum(Track_1*Sentiment)/sum(Track_1), sum(Track_2*Sentiment)/sum(Track_2), sum(Track_3*Sentiment)/sum(Track_3),sum(Track_4*Sentiment)/sum(Track_4),sum(Track_5*Sentiment)/sum(Track_5),sum(Track_6*Sentiment)/sum(Track_6) FROM Tweet_tablesecondary WHERE [Timestamp]<? GROUP BY Timestamp_minute", (Window2,))
	tweetminstatsfromsecondary = [[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]] for row in cursor.fetchall()]
	
	cursor.execute("SELECT Tweet,Timestamp_second, Screen_name, Sentiment, Latitude, Longitude, Place,Track_1 FROM Tweet_tablesecondary WHERE Latitude != 0 AND [Place] IS NOT NULL AND Track_1 = 1 AND [Timestamp]<?", (Window2,))
	tweetspatialstatstrack1 = [[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]] for row in cursor.fetchall()]
	
	cursor.execute("SELECT Tweet,Timestamp_second, Screen_name, Sentiment, Latitude, Longitude, Place,Track_2 FROM Tweet_tablesecondary WHERE Latitude != 0 AND [Place] IS NOT NULL AND Track_2 = 1 AND [Timestamp]<?", (Window2,))
	tweetspatialstatstrack2 = [[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]] for row in cursor.fetchall()]
	
	cursor.execute("SELECT Tweet,Timestamp_second, Screen_name, Sentiment, Latitude, Longitude, Place,Track_3 FROM Tweet_tablesecondary WHERE Latitude != 0 AND [Place] IS NOT NULL AND Track_3 = 1 AND [Timestamp]<?", (Window2,))
	tweetspatialstatstrack3 = [[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]] for row in cursor.fetchall()]
	
	cursor.execute("SELECT Tweet,Timestamp_second, Screen_name, Sentiment, Latitude, Longitude, Place,Track_4 FROM Tweet_tablesecondary WHERE Latitude != 0 AND [Place] IS NOT NULL AND Track_4 = 1 AND [Timestamp]<?", (Window2,))
	tweetspatialstatstrack4 = [[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]] for row in cursor.fetchall()]
	
	cursor.execute("SELECT Tweet,Timestamp_second, Screen_name, Sentiment, Latitude, Longitude, Place,Track_5 FROM Tweet_tablesecondary WHERE Latitude != 0 AND [Place] IS NOT NULL AND Track_5 = 1 AND [Timestamp]<?", (Window2,))
	tweetspatialstatstrack5 = [[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]] for row in cursor.fetchall()]
	
	cursor.execute("SELECT Tweet,Timestamp_second, Screen_name, Sentiment, Latitude, Longitude, Place,Track_6 FROM Tweet_tablesecondary WHERE Latitude != 0 AND [Place] IS NOT NULL AND Track_6 = 1 AND [Timestamp]<?", (Window2,))
	tweetspatialstatstrack6 = [[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]] for row in cursor.fetchall()]
	
	
	if 	tweetminstatsfromsecondary != []:
		cursor.executemany('insert into Tweet_minutestats  values (?,?,?,?,?,?,?,?,?,?,?,?,?)', tweetminstatsfromsecondary)
		conn.commit()
	if 	tweethourstatsfromsecondary != []:
		cursor.executemany('insert into Tweet_hourstats  values (?,?,?,?,?,?,?,?,?,?,?,?,?)', tweethourstatsfromsecondary)
		conn.commit()
		
	if 	tweetsecstatsfromsecondary != []:
		cursor.executemany('insert into Tweet_secondstats  values (?,?,?,?,?,?,?,?,?,?,?,?,?)', tweetsecstatsfromsecondary)
		conn.commit()
		
	if tweetspatialstatstrack1 != []:
		cursor.executemany('insert into Tweet_Spacial_Track1  values (?,?,?,?,?,?,?,?)', tweetspatialstatstrack1)
		conn.commit()
		
	if tweetspatialstatstrack2 != []:
		cursor.executemany('insert into Tweet_Spacial_Track2  values (?,?,?,?,?,?,?,?)', tweetspatialstatstrack2)
		conn.commit()
		
	if tweetspatialstatstrack3 != []:
		cursor.executemany('insert into Tweet_Spacial_Track3  values (?,?,?,?,?,?,?,?)', tweetspatialstatstrack3)
		conn.commit()
		
	if tweetspatialstatstrack4 != []:
		cursor.executemany('insert into Tweet_Spacial_Track4  values (?,?,?,?,?,?,?,?)', tweetspatialstatstrack4)
		conn.commit()
		
	if tweetspatialstatstrack5 != []:
		cursor.executemany('insert into Tweet_Spacial_Track5  values (?,?,?,?,?,?,?,?)', tweetspatialstatstrack5)
		conn.commit()
		
	if tweetspatialstatstrack6 != []:
		cursor.executemany('insert into Tweet_Spacial_Track6  values (?,?,?,?,?,?,?,?)', tweetspatialstatstrack6)
		conn.commit()
		
	
	cursor.execute("DELETE FROM Tweet_minutestats WHERE [Timestamp_minute]<?", (Window3,))
	conn.commit()
	cursor.execute("DELETE FROM Tweet_hourstats WHERE [Timestamp_hours]<?", (Window4,))
	conn.commit()
	cursor.execute("DELETE FROM Tweet_secondstats WHERE [Timestamp_second]<?", (Window5,))
	conn.commit()
	
	cursor.close()
	conn.close()
	print "Queries and cleaning done!"
	
	
#######Add the hashtag stats also in future #####
	
	
	
	
	
	
####### For executing the main insert query and commiting it#######
	
def committing(ws):
	cursor, cnx = Dbconnector()
	cursor.executemany('insert into Tweet_tableprimary  values (?,?,?,?,?,?,?,?,?,?,?,?)', ws)
	
	cnx.commit()
	cursor.close()
	cnx.close()

###################################################################
def textminingtweets(tweet):
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)    
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet	
	
##########This function will be used later for mining#############################


##################################################################################

#####################App routing for home#########################################

@app.route('/')
def home():
	return render_template('home.html')
	

	
###########Routing for data flows to front end#################################################


	
	
	
	
	
	
	

#####################App routing for main page, the stream happens within this function#########################################
@app.route('/MainPage',methods=['GET','POST'])

def log():
	
	
	if request.method == 'POST':
		print datetime.datetime.now().isoformat(' ')
		conn2 = sqlite3.connect('C:\Auburn INSY Twitter App Access Folder\AuburnINSYTwitterApp.db')
		conn2.execute("DELETE FROM Tweet_tracks")
		conn2.execute("INSERT INTO Tweet_tracks(Track_1, Track_2, Track_3, Track_4, Track_5, Track_6, Track_name1, Track_name2, Track_name3, Track_name4, Track_name5, Track_name6) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (request.form['searchterms1'], request.form['searchterms2'], request.form['searchterms3'], request.form['searchterms4'], request.form['searchterms5'], request.form['searchterms6'], request.form['trackname1'], request.form['trackname2'], request.form['trackname3'], request.form['trackname4'], request.form['trackname5'], request.form['trackname6']))
		conn2.commit()
		conn2.close()
		print datetime.datetime.now().isoformat(' ')
		print "Tracks Tracked"
		emailid = request.form['emailid']
		
		
		apikey = request.form['twitterapikey']
		apisecret = request.form['twitterapisecret']
		oauthkey = request.form['twitteroauthkey']
		oauthsecret = request.form['twitteroauthsecret']
		
		searchterms1 = request.form['searchterms1']
		
		searchlist1 = [x.strip() for x in searchterms1.split(',')]
		trackname1 = request.form['trackname1']
		
		searchterms2 = request.form['searchterms2']
		searchlist2 = [x.strip() for x in searchterms2.split(',')]
		trackname2 = request.form['trackname2']
		
		
		searchterms3 = request.form['searchterms3']
		searchlist3 = [x.strip() for x in searchterms3.split(',')]
		trackname3 = request.form['trackname3']
		
		searchterms4 = request.form['searchterms4']
		searchlist4 = [x.strip() for x in searchterms4.split(',')]
		trackname4 = request.form['trackname4']
		
		
		searchterms5 = request.form['searchterms5']
		searchlist5 = [x.strip() for x in searchterms5.split(',')]
		trackname5 = request.form['trackname5']
		
		searchterms6 = request.form['searchterms6']
		searchlist6 = [x.strip() for x in searchterms6.split(',')]
		trackname6 = request.form['trackname6']
		
		
		
		
		
		giantlist = searchlist1 + searchlist2 + searchlist3 + searchlist4 + searchlist5 + searchlist6
		giantlist2 = filter(None, giantlist)
		bigsearch = ', '.join(giantlist2)
		
		print bigsearch
		stream(apikey, apisecret, oauthkey, oauthsecret, bigsearch)
		
	return render_template('MainPage.html')
	
##############################Streaming and Threading comes here#######################################

class MyStreamer(TwythonStreamer):
	def on_success(self, data):
		global Beginning
		global Beginning2
		global Number_tweets
		global ws
		
		if 'text' in data and data['lang'].encode('utf-8') == 'en':
			try:
				lat = 0
				lng = 0
				plc = None
				if isinstance(data['coordinates'], Iterable):
					if 'coordinates' in data['coordinates']:
						lat = data['coordinates']['coordinates'][0]
						lng = data['coordinates']['coordinates'][1]
				if data['place'] != None:
					plc = data['place']['full_name'].encode('utf8')  
				
				if 'text' in data and data['lang'].encode('utf-8') == 'en':
					text = textminingtweets(data['text'].encode('utf8'))
					analysis = vaderSentiment(text)['compound']
					text = data['text'].replace("\"", "'")
					text = text.replace("\\", "")
					created_at = data['created_at'].encode('utf8')
					id_str = data['id_str'].encode('utf8')
					screen_name = data['user']['screen_name'].encode('utf-8')
					
					
					if True:
						
						
						

						if Number_tweets > 0:
							ws.append([text, datetime.datetime.now().isoformat(' '), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), datetime.datetime.now().strftime('%Y-%m-%d %H'), created_at, screen_name, analysis, lat, lng, plc, id_str])
							
						
						
						print ws
						
						
						Number_tweets += 1
						
						
					if (datetime.datetime.now() - Beginning).total_seconds() > 10:
						commit = threading.Thread(target=committing, args=(ws,))
						commit.start()
						print "inserting new tweets!"
						
						querying_clearing = threading.Thread(target=Querying_clearing)
						querying_clearing.start()
						
						Beginning = datetime.datetime.now()
						Number_tweets = 0
						ws = []
			
			except Exception as e:
				print e
				
	def on_error(self, status_code, data):
		print status_code

#####################################################################################################################


		

def stream(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET,trackterms):
	while True:
			try:
					stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	
					stream.statuses.filter(track=trackterms)
			except:
					continue




			
if __name__=='__main__':
	webbrowser.open_new("http://localhost:5000/")
	
	app.run(debug=True)
	
		
