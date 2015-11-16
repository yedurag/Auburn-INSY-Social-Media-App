from flask import Flask
import sqlite3
import datetime
from flask import *
from flask import Response, jsonify
import json
import re
from itertools import groupby
from operator import itemgetter
import webbrowser

Windowmarker = 1


app = Flask(__name__)
app.secret_key='8oFrGj9au99UNu7sJbK1WQ7VLKhu5Nto12333'

@app.route("/datastream1")
def datastream1():
  global Windowmarker
  
  Conn = sqlite3.connect('C:\Auburn INSY Twitter App Access Folder\AuburnINSYTwitterApp.db')
  Conn.text_factory = str
  cursor = Conn.cursor()
  Windowbreak = datetime.datetime.now() - datetime.timedelta(minutes=Windowmarker)
  Window = Windowbreak.strftime('%Y-%m-%d %H:%M:%S')
  cursor.execute("SELECT * FROM Tweet_tablesecondary")
  tweetlistfromsecondary = [[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17]] for row in cursor.fetchall()]
  
  
		
		
  
  cursor.execute("Select * FROM Tweet_tracks")
  tracklist = [dict(Track_1 = row[0], Track_2 = row[1], Track_3 = row[2], Track_4 = row[3], Track_5 = row[4], Track_6 = row[5], Track_name1 = row[6],  Track_name2 = row[7],  Track_name3 = row[8], Track_name4 = row[9], Track_name5 = row[10], Track_name6 = row[11]) for row in cursor.fetchall()]
  cursor.close()
  Conn.close()
  Track_1 = ""
  Track_2 = ""
  Track_3 = ""
  Track_4 = ""
  Track_5 = ""
  Track_6 = ""
  Track_name1 = ""
  Track_name2 = ""
  Track_name3 = ""
  Track_name4 = ""
  Track_name5 = ""
  Track_name6 = ""
  
  
  for trackdict in tracklist:
	Track_1 = trackdict["Track_1"]
	Track_2 = trackdict["Track_2"]
	Track_3 = trackdict["Track_3"]
	Track_4 = trackdict["Track_4"]
	Track_5 = trackdict["Track_5"]
	Track_6 = trackdict["Track_6"]
	if trackdict["Track_name1"] != "":
		Track_name1 = trackdict["Track_name1"]
	if trackdict["Track_name2"] != "":
		Track_name2 = trackdict["Track_name2"]
		
	if trackdict["Track_name3"] != "":
		Track_name3 = trackdict["Track_name3"]
		
	if trackdict["Track_name4"] != "":
		Track_name4 = trackdict["Track_name4"]
		
	if trackdict["Track_name5"] != "":
		Track_name5 = trackdict["Track_name5"]
		
	if trackdict["Track_name6"] != "":
		Track_name6 = trackdict["Track_name6"]
		
		
	
		
	
  Tracklist1 = [x.strip() for x in Track_1.split(',')]
  Tracklist2 = [x.strip() for x in Track_2.split(',')]
  Tracklist3 = [x.strip() for x in Track_3.split(',')]
  Tracklist4 = [x.strip() for x in Track_4.split(',')]
  Tracklist5 = [x.strip() for x in Track_5.split(',')]
  Tracklist6 = [x.strip() for x in Track_6.split(',')]
  Trackhashlist1 = ["#" + i.lower() for i in Tracklist1]
  Trackhashlist2 = ["#" + i.lower() for i in Tracklist2]
  Trackhashlist3 = ["#" + i.lower() for i in Tracklist3]
  Trackhashlist4 = ["#" + i.lower() for i in Tracklist4]
  Trackhashlist5 = ["#" + i.lower() for i in Tracklist5]
  Trackhashlist6 = ["#" + i.lower() for i in Tracklist6]
  
  
  all_tweets = []
  
  
   
  
  tweetlistforhashtag1 = []
  tweetlistforhashtag2 = []
  tweetlistforhashtag3 = []
  tweetlistforhashtag4 = []
  tweetlistforhashtag5 = []
  tweetlistforhashtag6 = []
  
  
  tweetlist1forhashtag1 = []
  tweetlist2forhashtag2 = []
  tweetlist3forhashtag3 = []
  tweetlist4forhashtag4 = []
  tweetlist5forhashtag5 = []
  tweetlist6forhashtag6 = []
  
  
  for i in tweetlistfromsecondary:
	if i[12] == 1:
		tweetlistforhashtag1.append([i[3], i[0]])
		
  for i in tweetlistfromsecondary:
	if i[13] == 1:
		tweetlistforhashtag2.append([i[3], i[0]])
		
  for i in tweetlistfromsecondary:
	if i[14] == 1:
		tweetlistforhashtag3.append([i[3], i[0]])
  for i in tweetlistfromsecondary:
	if i[15] == 1:
		tweetlistforhashtag4.append([i[3], i[0]])
		
  for i in tweetlistfromsecondary:
	if i[16] == 1:
		tweetlistforhashtag5.append([i[3], i[0]])
		
  for i in tweetlistfromsecondary:
	if i[17] == 1:
		tweetlistforhashtag6.append([i[3], i[0]])
		
		
  if tweetlistforhashtag1 != []:
	data = sorted(tweetlistforhashtag1, key=itemgetter(0))
	for k, g in groupby(data, itemgetter(0)):
		g = list(g)
		x = [l[1] for l in g]
		stringx = " ".join(x)
		stringy = stringx.lower()
		hashtaglist = ["#" + part[1:] for part in stringy.split() if part.startswith('#')]
		hashtaglist2 = []
		
		for r in hashtaglist:
			if r not in Trackhashlist1:
				hashtaglist2.append(r)
		hashtaglistinner = [[g[0], len(list(g[1]))] for g in groupby(hashtaglist2)]
		hashtaglistinner = sorted(hashtaglistinner, key=itemgetter(1),reverse=True)
		if len(hashtaglistinner) > 0:
			hashtaglistinner1 = hashtaglistinner[0]
		else:
			hashtaglistinner1 = ["no hashtag",0]
			
			
		tweetlist1forhashtag1.append([k,hashtaglistinner1])
		
  if tweetlistforhashtag2 != []:
	data = sorted(tweetlistforhashtag2, key=itemgetter(0))
	for k, g in groupby(data, itemgetter(0)):
		g = list(g)
		x = [l[1] for l in g]
		stringx = " ".join(x)
		stringy = stringx.lower()
		hashtaglist = ["#" + part[1:] for part in stringy.split() if part.startswith('#')]
		hashtaglist2 = []
		
		for r in hashtaglist:
			if r not in Trackhashlist2:
				hashtaglist2.append(r)
		hashtaglistinner = [[g[0], len(list(g[1]))] for g in groupby(hashtaglist2)]
		hashtaglistinner = sorted(hashtaglistinner, key=itemgetter(1),reverse=True)
		if len(hashtaglistinner) > 0:
			hashtaglistinner1 = hashtaglistinner[0]
		else:
			hashtaglistinner1 = ["no hashtag",0]
			
			
		tweetlist2forhashtag2.append([k,hashtaglistinner1])
		
  if tweetlistforhashtag3 != []:
	data = sorted(tweetlistforhashtag3, key=itemgetter(0))
	for k, g in groupby(data, itemgetter(0)):
		g = list(g)
		x = [l[1] for l in g]
		stringx = " ".join(x)
		stringy = stringx.lower()
		hashtaglist = ["#" + part[1:] for part in stringy.split() if part.startswith('#')]
		hashtaglist2 = []
		
		for r in hashtaglist:
			if r not in Trackhashlist3:
				hashtaglist2.append(r)
		hashtaglistinner = [[g[0], len(list(g[1]))] for g in groupby(hashtaglist2)]
		hashtaglistinner = sorted(hashtaglistinner, key=itemgetter(1),reverse=True)
		if len(hashtaglistinner) > 0:
			hashtaglistinner1 = hashtaglistinner[0]
		else:
			hashtaglistinner1 = ["no hashtag",0]
			
			
		tweetlist3forhashtag3.append([k,hashtaglistinner1])
		
  if tweetlistforhashtag4 != []:
	data = sorted(tweetlistforhashtag4, key=itemgetter(0))
	for k, g in groupby(data, itemgetter(0)):
		g = list(g)
		x = [l[1] for l in g]
		stringx = " ".join(x)
		stringy = stringx.lower()
		hashtaglist = ["#" + part[1:] for part in stringy.split() if part.startswith('#')]
		hashtaglist2 = []
		
		for r in hashtaglist:
			if r not in Trackhashlist4:
				hashtaglist2.append(r)
		hashtaglistinner = [[g[0], len(list(g[1]))] for g in groupby(hashtaglist2)]
		hashtaglistinner = sorted(hashtaglistinner, key=itemgetter(1),reverse=True)
		if len(hashtaglistinner) > 0:
			hashtaglistinner1 = hashtaglistinner[0]
		else:
			hashtaglistinner1 = ["no hashtag",0]
			
			
		tweetlist4forhashtag4.append([k,hashtaglistinner1])
		
  if tweetlistforhashtag5 != []:
	data = sorted(tweetlistforhashtag5, key=itemgetter(0))
	for k, g in groupby(data, itemgetter(0)):
		g = list(g)
		x = [l[1] for l in g]
		stringx = " ".join(x)
		stringy = stringx.lower()
		hashtaglist = ["#" + part[1:] for part in stringy.split() if part.startswith('#')]
		hashtaglist2 = []
		
		for r in hashtaglist:
			if r not in Trackhashlist5:
				hashtaglist2.append(r)
		hashtaglistinner = [[g[0], len(list(g[1]))] for g in groupby(hashtaglist2)]
		hashtaglistinner = sorted(hashtaglistinner, key=itemgetter(1),reverse=True)
		if len(hashtaglistinner) > 0:
			hashtaglistinner1 = hashtaglistinner[0]
		else:
			hashtaglistinner1 = ["no hashtag",0]
			
			
		tweetlist5forhashtag5.append([k,hashtaglistinner1])
		
		
  if tweetlistforhashtag6 != []:
	data = sorted(tweetlistforhashtag6, key=itemgetter(0))
	for k, g in groupby(data, itemgetter(0)):
		g = list(g)
		x = [l[1] for l in g]
		stringx = " ".join(x)
		stringy = stringx.lower()
		hashtaglist = ["#" + part[1:] for part in stringy.split() if part.startswith('#')]
		hashtaglist2 = []
		
		for r in hashtaglist:
			if r not in Trackhashlist6:
				hashtaglist2.append(r)
		hashtaglistinner = [[g[0], len(list(g[1]))] for g in groupby(hashtaglist2)]
		hashtaglistinner = sorted(hashtaglistinner, key=itemgetter(1),reverse=True)
		if len(hashtaglistinner) > 0:
			hashtaglistinner1 = hashtaglistinner[0]
		else:
			hashtaglistinner1 = ["no hashtag",0]
			
			
		tweetlist6forhashtag6.append([k,hashtaglistinner1])
		
		
	
	
	
    
	
	
  
  
 
 
  
  
  
  for i in tweetlistfromsecondary:
	Tweetsfortrack1 = {}
	
	if i[12] == 1:
		Tweetsfortrack1["tweet"] = i[0]
		Tweetsfortrack1["timestamp"] = i[2]
		Tweetsfortrack1["created_at"] = i[5]
		Tweetsfortrack1["user_name"] = i[6]
		Tweetsfortrack1["sentiment"] = i[7]
		Tweetsfortrack1["id_str"] = i[11]
		Tweetsfortrack1["track"] = "Track1"
		Tweetsfortrack1["track_name"] = Track_name1
		
		Tweetsfortrack1["track1_count"] = 1
		Tweetsfortrack1["track2_count"] = 0
		Tweetsfortrack1["track3_count"] = 0
		Tweetsfortrack1["track4_count"] = 0
		Tweetsfortrack1["track5_count"] = 0
		Tweetsfortrack1["track6_count"] = 0
		
		Tweetsfortrack1["track1_sentiment"] = i[7]
		Tweetsfortrack1["track2_sentiment"] = 0
		Tweetsfortrack1["track3_sentiment"] = 0
		Tweetsfortrack1["track4_sentiment"] = 0
		Tweetsfortrack1["track5_sentiment"] = 0
		Tweetsfortrack1["track6_sentiment"] = 0
		
		
		if i[7] > 0.5:
			Tweetsfortrack1["sentibin"] = "very positive"
			
		elif i[7] <= 0.5 and i[7] > 0:
			Tweetsfortrack1["sentibin"] = "positive"
		elif i[7] == 0:
			Tweetsfortrack1["sentibin"] = "neutral"
		elif i[7] < 0 and i[7] >= -0.5:
			Tweetsfortrack1["sentibin"] = "negative"	
		else:
			Tweetsfortrack1["sentibin"] = "very negative"
		for t in tweetlist1forhashtag1:
			if t[0] == i[3]:
				Tweetsfortrack1["tophashtag"] = t[1][0]
				Tweetsfortrack1["tophashtagcount"] = t[1][1]
				
			
		if Tweetsfortrack1 != {}:
			all_tweets.append(Tweetsfortrack1)	
		
  for i in tweetlistfromsecondary:
	Tweetsfortrack2 = {}
	if i[13] == 1:
		Tweetsfortrack2["tweet"] = i[0]
		Tweetsfortrack2["timestamp"] = i[2]
		Tweetsfortrack2["created_at"] = i[5]
		Tweetsfortrack2["user_name"] = i[6]
		Tweetsfortrack2["sentiment"] = i[7]
		Tweetsfortrack2["id_str"] = i[11]
		Tweetsfortrack2["track"] = "Track2"
		Tweetsfortrack2["track_name"] = Track_name2
		
		Tweetsfortrack2["track1_count"] = 0
		Tweetsfortrack2["track2_count"] = 1
		Tweetsfortrack2["track3_count"] = 0
		Tweetsfortrack2["track4_count"] = 0
		Tweetsfortrack2["track5_count"] = 0
		Tweetsfortrack2["track6_count"] = 0
		
		Tweetsfortrack2["track1_sentiment"] = 0
		Tweetsfortrack2["track2_sentiment"] = i[7]
		Tweetsfortrack2["track3_sentiment"] = 0
		Tweetsfortrack2["track4_sentiment"] = 0
		Tweetsfortrack2["track5_sentiment"] = 0
		Tweetsfortrack2["track6_sentiment"] = 0
		if i[7] > 0.5:
			Tweetsfortrack2["sentibin"] = "very positive"
			
		elif i[7] <= 0.5 and i[7] > 0:
			Tweetsfortrack2["sentibin"] = "positive"
		elif i[7] == 0:
			Tweetsfortrack2["sentibin"] = "neutral"
		elif i[7] < 0 and i[7] >= -0.5:
			Tweetsfortrack2["sentibin"] = "negative"	
		else:
			Tweetsfortrack2["sentibin"] = "very negative"
		for t in tweetlist2forhashtag2:
			if t[0] == i[3]:
				Tweetsfortrack2["tophashtag"] = t[1][0]
				Tweetsfortrack2["tophashtagcount"] = t[1][1]
	
		if Tweetsfortrack2 != {}:
			all_tweets.append(Tweetsfortrack2)
		
  for i in tweetlistfromsecondary:
	Tweetsfortrack3 = {}
	if i[14] == 1:
		Tweetsfortrack3["tweet"] = i[0]
		Tweetsfortrack3["timestamp"] = i[2]
		Tweetsfortrack3["created_at"] = i[5]
		Tweetsfortrack3["user_name"] = i[6]
		Tweetsfortrack3["sentiment"] = i[7]
		Tweetsfortrack3["id_str"] = i[11]
		Tweetsfortrack3["track"] = "Track3"
		Tweetsfortrack3["track_name"] = Track_name3
		Tweetsfortrack3["track1_count"] = 0
		Tweetsfortrack3["track2_count"] = 0
		Tweetsfortrack3["track3_count"] = 1
		Tweetsfortrack3["track4_count"] = 0
		Tweetsfortrack3["track5_count"] = 0
		Tweetsfortrack3["track6_count"] = 0
		
		Tweetsfortrack3["track1_sentiment"] = 0
		Tweetsfortrack3["track2_sentiment"] = 0
		Tweetsfortrack3["track3_sentiment"] = i[7]
		Tweetsfortrack3["track4_sentiment"] = 0
		Tweetsfortrack3["track5_sentiment"] = 0
		Tweetsfortrack3["track6_sentiment"] = 0
		
		if i[7] > 0.5:
			Tweetsfortrack3["sentibin"] = "very positive"
			
		elif i[7] <= 0.5 and i[7] > 0:
			Tweetsfortrack3["sentibin"] = "positive"
		elif i[7] == 0:
			Tweetsfortrack3["sentibin"] = "neutral"
		elif i[7] < 0 and i[7] >= -0.5:
			Tweetsfortrack3["sentibin"] = "negative"	
		else:
			Tweetsfortrack3["sentibin"] = "very negative"
		for t in tweetlist3forhashtag3:
			if t[0] == i[3]:
				Tweetsfortrack3["tophashtag"] = t[1][0]
				Tweetsfortrack3["tophashtagcount"] = t[1][1]
		if Tweetsfortrack3 != {}:
			all_tweets.append(Tweetsfortrack2)
		
		
  for i in tweetlistfromsecondary:
	Tweetsfortrack4 = {}
	if i[15] == 1:
		Tweetsfortrack4["tweet"] = i[0]
		Tweetsfortrack4["timestamp"] = i[2]
		Tweetsfortrack4["created_at"] = i[5]
		Tweetsfortrack4["user_name"] = i[6]
		Tweetsfortrack4["sentiment"] = i[7]
		Tweetsfortrack4["id_str"] = i[11]
		Tweetsfortrack4["track"] = "Track4"
		Tweetsfortrack4["track_name"] = Track_name4
		
		Tweetsfortrack4["track1_count"] = 0
		Tweetsfortrack4["track2_count"] = 0
		Tweetsfortrack4["track3_count"] = 0
		Tweetsfortrack4["track4_count"] = 1
		Tweetsfortrack4["track5_count"] = 0
		Tweetsfortrack4["track6_count"] = 0
		
		Tweetsfortrack4["track1_sentiment"] = 0
		Tweetsfortrack4["track2_sentiment"] = 0
		Tweetsfortrack4["track3_sentiment"] = 0
		Tweetsfortrack4["track4_sentiment"] = i[7]
		Tweetsfortrack4["track5_sentiment"] = 0
		Tweetsfortrack4["track6_sentiment"] = 0
		
		
		if i[7] > 0.5:
			Tweetsfortrack4["sentibin"] = "very positive"
			
		elif i[7] <= 0.5 and i[7] > 0:
			Tweetsfortrack4["sentibin"] = "positive"
		elif i[7] == 0:
			Tweetsfortrack4["sentibin"] = "neutral"
		elif i[7] < 0 and i[7] >= -0.5:
			Tweetsfortrack4["sentibin"] = "negative"	
		else:
			Tweetsfortrack4["sentibin"] = "very negative"
		for t in tweetlist4forhashtag4:
			if t[0] == i[3]:
				Tweetsfortrack4["tophashtag"] = t[1][0]
				Tweetsfortrack4["tophashtagcount"] = t[1][1]
		if Tweetsfortrack4 != {}:
			all_tweets.append(Tweetsfortrack4)
			
  for i in tweetlistfromsecondary:
	Tweetsfortrack5 = {}
	if i[16] == 1:
		Tweetsfortrack5["tweet"] = i[0]
		Tweetsfortrack5["timestamp"] = i[2]
		Tweetsfortrack5["created_at"] = i[5]
		Tweetsfortrack5["user_name"] = i[6]
		Tweetsfortrack5["sentiment"] = i[7]
		Tweetsfortrack5["id_str"] = i[11]
		Tweetsfortrack5["track"] = "Track5"
		Tweetsfortrack5["track_name"] = Track_name5
		Tweetsfortrack5["track1_count"] = 0
		Tweetsfortrack5["track2_count"] = 0
		Tweetsfortrack5["track3_count"] = 0
		Tweetsfortrack5["track4_count"] = 0
		Tweetsfortrack5["track5_count"] = 1
		Tweetsfortrack5["track6_count"] = 0
		
		Tweetsfortrack5["track1_sentiment"] = 0
		Tweetsfortrack5["track2_sentiment"] = 0
		Tweetsfortrack5["track3_sentiment"] = 0
		Tweetsfortrack5["track4_sentiment"] = 0
		Tweetsfortrack5["track5_sentiment"] = i[7]
		Tweetsfortrack5["track6_sentiment"] = 0
		
		if i[7] > 0.5:
			Tweetsfortrack5["sentibin"] = "very positive"
			
		elif i[7] <= 0.5 and i[7] > 0:
			Tweetsfortrack5["sentibin"] = "positive"
		elif i[7] == 0:
			Tweetsfortrack5["sentibin"] = "neutral"
		elif i[7] < 0 and i[7] >= -0.5:
			Tweetsfortrack5["sentibin"] = "negative"	
		else:
			Tweetsfortrack5["sentibin"] = "very negative"
		for t in tweetlist5forhashtag5:
			if t[0] == i[3]:
				Tweetsfortrack5["tophashtag"] = t[1][0]
				Tweetsfortrack5["tophashtagcount"] = t[1][1]
		if Tweetsfortrack5 != {}:
			all_tweets.append(Tweetsfortrack5)
			
  for i in tweetlistfromsecondary:
	Tweetsfortrack6 = {}
	if i[17] == 1:
		Tweetsfortrack6["tweet"] = i[0]
		Tweetsfortrack6["timestamp"] = i[2]
		Tweetsfortrack6["created_at"] = i[5]
		Tweetsfortrack6["user_name"] = i[6]
		Tweetsfortrack6["sentiment"] = i[7]
		Tweetsfortrack6["id_str"] = i[11]
		Tweetsfortrack6["track"] = "Track6"
		Tweetsfortrack6["track_name"] = Track_name6
		
		Tweetsfortrack6["track1_count"] = 0
		Tweetsfortrack6["track2_count"] = 0
		Tweetsfortrack6["track3_count"] = 0
		Tweetsfortrack6["track4_count"] = 0
		Tweetsfortrack6["track5_count"] = 0
		Tweetsfortrack6["track6_count"] = 1
		
		Tweetsfortrack6["track1_sentiment"] = 0
		Tweetsfortrack6["track2_sentiment"] = 0
		Tweetsfortrack6["track3_sentiment"] = 0
		Tweetsfortrack6["track4_sentiment"] = 0
		Tweetsfortrack6["track5_sentiment"] = 0
		Tweetsfortrack6["track6_sentiment"] = i[7]
		
		if i[7] > 0.5:
			Tweetsfortrack6["sentibin"] = "very positive"
			
		elif i[7] <= 0.5 and i[7] > 0:
			Tweetsfortrack6["sentibin"] = "positive"
		elif i[7] == 0:
			Tweetsfortrack6["sentibin"] = "neutral"
		elif i[7] < 0 and i[7] >= -0.5:
			Tweetsfortrack6["sentibin"] = "negative"	
		else:
			Tweetsfortrack6["sentibin"] = "very negative"
			
		for t in tweetlist6forhashtag6:
			if t[0] == i[3]:
				Tweetsfortrack6["tophashtag"] = t[1][0]
				Tweetsfortrack6["tophashtagcount"] = t[1][1]
		if Tweetsfortrack6 != {}:
			all_tweets.append(Tweetsfortrack6)
  all_tweets1 = []
  for k in all_tweets:
    if k != {}:
		all_tweets1.append(k)
		
  
  js = json.dumps(all_tweets1)
  resp = Response(js, status=200, mimetype='application/json')
  resp.headers.add('Access-Control-Allow-Origin', "*")
  return resp
  
@app.route("/datastream2")
def datastream2():
  Conn = sqlite3.connect('C:\Auburn INSY Twitter App Access Folder\AuburnINSYTwitterApp.db')
  Conn.text_factory = str
  cursor = Conn.cursor()
  cursor.execute("SELECT Timestamp_second, sum(Track_1_count), sum(Track_2_count), sum(Track_3_count), sum(Track_4_count), sum(Track_5_count), sum(Track_6_count), sum(Track_1_count*Track_1_sentiment)/sum(Track_1_count), sum(Track_2_count*Track_2_sentiment)/sum(Track_2_sentiment), sum(Track_3_count*Track_3_sentiment)/sum(Track_3_count),sum(Track_4_count*Track_4_sentiment)/sum(Track_4_count),sum(Track_5_count*Track_5_sentiment)/sum(Track_5_count),sum(Track_6_count*Track_6_sentiment)/sum(Track_6_count) FROM Tweet_secondstats GROUP BY Timestamp_second")
  
  tweetsecstats = [{"time_stamp_second": row[0], "track1_count": row[1],"track2_count": row[2],"track3_count": row[3],"track4_count": row[4],"track5_count": row[5],"track6_count": row[6], "track1_sentiment" : row[7],"track2_sentiment" : row[8],"track3_sentiment" : row[9],"track4_sentiment" : row[10],"track5_sentiment" : row[11],"track6_sentiment" : row[12]} for row in cursor.fetchall()]
  js = json.dumps(tweetsecstats)
  resp = Response(js, status=200, mimetype='application/json')
  resp.headers.add('Access-Control-Allow-Origin', "*")
  return resp
 
 

@app.route("/datastream3")
def datastream3():
  Conn = sqlite3.connect('C:\Auburn INSY Twitter App Access Folder\AuburnINSYTwitterApp.db')
  Conn.text_factory = str
  cursor = Conn.cursor()
  cursor.execute("SELECT Timestamp_minute, sum(Track_1_count), sum(Track_2_count), sum(Track_3_count), sum(Track_4_count), sum(Track_5_count), sum(Track_6_count), sum(Track_1_count*Track_1_sentiment)/sum(Track_1_count), sum(Track_2_count*Track_2_sentiment)/sum(Track_2_sentiment), sum(Track_3_count*Track_3_sentiment)/sum(Track_3_count),sum(Track_4_count*Track_4_sentiment)/sum(Track_4_count),sum(Track_5_count*Track_5_sentiment)/sum(Track_5_count),sum(Track_6_count*Track_6_sentiment)/sum(Track_6_count) FROM Tweet_minutestats GROUP BY Timestamp_minute")
  
  tweetsecstats = [{"time_stamp_minute": row[0], "track1_count": row[1],"track2_count": row[2],"track3_count": row[3],"track4_count": row[4],"track5_count": row[5],"track6_count": row[6], "track1_sentiment" : row[7],"track2_sentiment" : row[8],"track3_sentiment" : row[9],"track4_sentiment" : row[10],"track5_sentiment" : row[11],"track6_sentiment" : row[12]} for row in cursor.fetchall()]
  js = json.dumps(tweetsecstats)
  resp = Response(js, status=200, mimetype='application/json')
  resp.headers.add('Access-Control-Allow-Origin', "*")
  return resp
 			
@app.route("/datastream4")
def datastream4():
  Conn = sqlite3.connect('C:\Auburn INSY Twitter App Access Folder\AuburnINSYTwitterApp.db')
  Conn.text_factory = str
  cursor = Conn.cursor()
  cursor.execute("SELECT Timestamp_hours, sum(Track_1_count), sum(Track_2_count), sum(Track_3_count), sum(Track_4_count), sum(Track_5_count), sum(Track_6_count), sum(Track_1_count*Track_1_sentiment)/sum(Track_1_count), sum(Track_2_count*Track_2_sentiment)/sum(Track_2_sentiment), sum(Track_3_count*Track_3_sentiment)/sum(Track_3_count),sum(Track_4_count*Track_4_sentiment)/sum(Track_4_count),sum(Track_5_count*Track_5_sentiment)/sum(Track_5_count),sum(Track_6_count*Track_6_sentiment)/sum(Track_6_count) FROM Tweet_hourstats GROUP BY Timestamp_hours")
  
  tweetsecstats = [{"time_stamp_hour": row[0], "track1_count": row[1],"track2_count": row[2],"track3_count": row[3],"track4_count": row[4],"track5_count": row[5],"track6_count": row[6], "track1_sentiment" : row[7],"track2_sentiment" : row[8],"track3_sentiment" : row[9],"track4_sentiment" : row[10],"track5_sentiment" : row[11],"track6_sentiment" : row[12]} for row in cursor.fetchall()]
  js = json.dumps(tweetsecstats)
  resp = Response(js, status=200, mimetype='application/json')
  resp.headers.add('Access-Control-Allow-Origin', "*")
  return resp	
			
@app.route("/datastream5")
def datastream5():
  Conn = sqlite3.connect('C:\Auburn INSY Twitter App Access Folder\AuburnINSYTwitterApp.db')
  Conn.text_factory = str
  cursor = Conn.cursor()
  cursor.execute("SELECT Tweet, Timestamp_second, Screen_name, Place FROM Tweet_Spacial_Track1")
  
  tweetspacialtrack1 = [[row[0],row[1],row[2],row[3]] for row in cursor.fetchall()]
  
  cursor.execute("SELECT Place, min(Latitude), min(Longitude), sum(Track_1), sum(Track_1*Sentiment)/sum(Track_1) FROM Tweet_Spacial_Track1 GROUP BY Place")
  tweetspacialtrack1stats = [{"place": row[0], "latitude": row[1], "longitude": row[2], "count": row[3], "sentiment": row[4], "tweets": []} for row in cursor.fetchall()]
  
  for i in tweetspacialtrack1stats:
	spatialinter = []
	for k in tweetspacialtrack1:
		if i["place"] == k[3]:
			spatialinter.append(["Tweet:" + "'" + k[0] + "' "+ "Time:" + k[1] + " User:" + "'" + k[2]+ "' "])
	i["tweets"] = spatialinter
  spatialall = []
  for r in tweetspacialtrack1stats:
	if r != {}:
		spatialall.append(r)
	
  
  js = json.dumps(spatialall)
  resp = Response(js, status=200, mimetype='application/json')
  resp.headers.add('Access-Control-Allow-Origin', "*")
  return resp	
  
@app.route("/datastream6")
def datastream6():
  Conn = sqlite3.connect('C:\Auburn INSY Twitter App Access Folder\AuburnINSYTwitterApp.db')
  Conn.text_factory = str
  cursor = Conn.cursor()
  cursor.execute("SELECT Tweet, Timestamp_second, Screen_name, Place FROM Tweet_Spacial_Track2")
  
  tweetspacialtrack2 = [[row[0],row[1],row[2],row[3]] for row in cursor.fetchall()]
  
  cursor.execute("SELECT Place, min(Latitude), min(Longitude), sum(Track_2), sum(Track_2*Sentiment)/sum(Track_2) FROM Tweet_Spacial_Track2 GROUP BY Place")
  tweetspacialtrack2stats = [{"place": row[0], "latitude": row[1], "longitude": row[2], "count": row[3], "sentiment": row[4]} for row in cursor.fetchall()]
  
  for i in tweetspacialtrack2stats:
	spatialinter = []
	for k in tweetspacialtrack2:
		if i["place"] == k[3]:
			spatialinter.append(["Tweet:" + "'" + k[0] + "' "+ "Time:" + k[1] + " User:" + "'" + k[2]+ "' "])
		i["tweets"] = spatialinter
  spatialall = []
  for r in tweetspacialtrack2stats:
	if r != {}:
		spatialall.append(r)
	
  
  js = json.dumps(spatialall)
  resp = Response(js, status=200, mimetype='application/json')
  resp.headers.add('Access-Control-Allow-Origin', "*")
  return resp	
  
@app.route("/datastream7")
def datastream7():
  Conn = sqlite3.connect('C:\Auburn INSY Twitter App Access Folder\AuburnINSYTwitterApp.db')
  Conn.text_factory = str
  cursor = Conn.cursor()
  cursor.execute("SELECT Tweet, Timestamp_second, Screen_name, Place FROM Tweet_Spacial_Track3")
  
  tweetspacialtrack3 = [[row[0],row[1],row[2],row[3]] for row in cursor.fetchall()]
  
  cursor.execute("SELECT Place, min(Latitude), min(Longitude), sum(Track_3), sum(Track_3*Sentiment)/sum(Track_3) FROM Tweet_Spacial_Track3 GROUP BY Place")
  tweetspacialtrack3stats = [{"place": row[0], "latitude": row[1], "longitude": row[2], "count": row[3], "sentiment": row[4]} for row in cursor.fetchall()]
  
  for i in tweetspacialtrack3stats:
	spatialinter = []
	for k in tweetspacialtrack3:
		if i["place"] == k[3]:
			spatialinter.append(["Tweet:" + "'" + k[0] + "' "+ "Time:" + k[1] + " User:" + "'" + k[2]+ "' "])
	i["tweets"] = spatialinter
  spatialall = []
  for r in tweetspacialtrack3stats:
	if r != {}:
		spatialall.append(r)
	
  
  js = json.dumps(spatialall)
  resp = Response(js, status=200, mimetype='application/json')
  resp.headers.add('Access-Control-Allow-Origin', "*")
  return resp

@app.route("/datastream8")
def datastream8():
  Conn = sqlite3.connect('C:\Auburn INSY Twitter App Access Folder\AuburnINSYTwitterApp.db')
  Conn.text_factory = str
  cursor = Conn.cursor()
  cursor.execute("SELECT Tweet, Timestamp_second, Screen_name, Place FROM Tweet_Spacial_Track4")
  
  tweetspacialtrack4 = [[row[0],row[1],row[2],row[3]] for row in cursor.fetchall()]
  
  cursor.execute("SELECT Place, min(Latitude), min(Longitude), sum(Track_4), sum(Track_4*Sentiment)/sum(Track_4) FROM Tweet_Spacial_Track4 GROUP BY Place")
  tweetspacialtrack4stats = [{"place": row[0], "latitude": row[1], "longitude": row[2], "count": row[3], "sentiment": row[4]} for row in cursor.fetchall()]
  
  for i in tweetspacialtrack4stats:
	spatialinter = []
	for k in tweetspacialtrack4:
		if i["place"] == k[3]:
			spatialinter.append(["Tweet:" + "'" + k[0] + "' "+ "Time:" + k[1] + " User:" + "'" + k[2]+ "' "])
	i["tweets"] = spatialinter
  spatialall = []
  for r in tweetspacialtrack4stats:
	if r != {}:
		spatialall.append(r)
	
  
  js = json.dumps(spatialall)
  resp = Response(js, status=200, mimetype='application/json')
  resp.headers.add('Access-Control-Allow-Origin', "*")
  return resp

@app.route("/datastream9")
def datastream9():
  Conn = sqlite3.connect('C:\Auburn INSY Twitter App Access Folder\AuburnINSYTwitterApp.db')
  Conn.text_factory = str
  cursor = Conn.cursor()
  cursor.execute("SELECT Tweet, Timestamp_second, Screen_name, Place FROM Tweet_Spacial_Track5")
  
  tweetspacialtrack5 = [[row[0],row[1],row[2],row[3]] for row in cursor.fetchall()]
  
  cursor.execute("SELECT Place, min(Latitude), min(Longitude), sum(Track_5), sum(Track_5*Sentiment)/sum(Track_5) FROM Tweet_Spacial_Track5 GROUP BY Place")
  tweetspacialtrack5stats = [{"place": row[0], "latitude": row[1], "longitude": row[2], "count": row[3], "sentiment": row[4]} for row in cursor.fetchall()]
  
  for i in tweetspacialtrack5stats:
	spatialinter = []
	for k in tweetspacialtrack5:
		if i["place"] == k[3]:
			spatialinter.append(["Tweet:" + "'" + k[0] + "' "+ "Time:" + k[1] + " User:" + "'" + k[2]+ "' "])
	i["tweets"] = spatialinter
  spatialall = []
  for r in tweetspacialtrack5stats:
	if r != {}:
		spatialall.append(r)
	
  
  js = json.dumps(spatialall)
  resp = Response(js, status=200, mimetype='application/json')
  resp.headers.add('Access-Control-Allow-Origin', "*")
  return resp

@app.route("/datastream10")
def datastream10():
  Conn = sqlite3.connect('C:\Auburn INSY Twitter App Access Folder\AuburnINSYTwitterApp.db')
  Conn.text_factory = str
  cursor = Conn.cursor()
  cursor.execute("SELECT Tweet, Timestamp_second, Screen_name, Place FROM Tweet_Spacial_Track6")
  
  tweetspacialtrack6 = [[row[0],row[1],row[2],row[3]] for row in cursor.fetchall()]
  
  cursor.execute("SELECT Place, min(Latitude), min(Longitude), sum(Track_6), sum(Track_6*Sentiment)/sum(Track_6) FROM Tweet_Spacial_Track6 GROUP BY Place")
  tweetspacialtrack6stats = [{"place": row[0], "latitude": row[1], "longitude": row[2], "count": row[3], "sentiment": row[4]} for row in cursor.fetchall()]
  
  for i in tweetspacialtrack6stats:
	spatialinter = []
	for k in tweetspacialtrack6:
		if i["place"] == k[3]:
			spatialinter.append(["Tweet:" + "'" + k[0] + "' "+ "Time:" + k[1] + " User:" + "'" + k[2]+ "' "])
	i["tweets"] = spatialinter
  spatialall = []
  for r in tweetspacialtrack6stats:
	if r != {}:
		spatialall.append(r)
	
  
  js = json.dumps(spatialall)
  resp = Response(js, status=200, mimetype='application/json')
  resp.headers.add('Access-Control-Allow-Origin', "*")
  return resp    
			 
@app.route("/datastream11")
def datastream11():
  Conn = sqlite3.connect('C:\Auburn INSY Twitter App Access Folder\AuburnINSYTwitterApp.db')
  Conn.text_factory = str
  cursor = Conn.cursor()
  cursor.execute("select Track_1, Track_2, Track_3, Track_4, Track_5, Track_6, Track_name1, Track_name2, Track_name3, Track_name4, Track_name5, Track_name6 from Tweet_tracks")
  
  tweetsecstats = [{"Track_1": row[0], "Track_2": row[1],"Track_3": row[2],"Track_4": row[3],"Track_5": row[4],"Track_6": row[5],"Track_name1": row[6], "Track_name2" : row[7],"Track_name3" : row[8],"Track_name4" : row[9],"Track_name5" : row[10],"Track_name6" : row[11]} for row in cursor.fetchall()]
  js = json.dumps(tweetsecstats)
  resp = Response(js, status=200, mimetype='application/json')
  resp.headers.add('Access-Control-Allow-Origin', "*")
  return resp	
			 			
@app.route('/')
def Dashboard_MainPage():
	return render_template('Dashboard_MainPage.html')	
			
@app.route('/TemporalAnalysis_FlowingData')
def TemporalAnalysis_FlowingData():
	return render_template('TemporalAnalysis_FlowingData.html')		
		
@app.route('/TemporalAnalysis_PersistentData')
def TemporalAnalysis_PersistentData():
	return render_template('TemporalAnalysis_PersistentData.html')
		
@app.route('/SpatialAnalysis')
def SpatialAnalysis():
	return render_template('SpatialAnalysis.html')  
		
	
		
		
		
	
  
  
  
  
  
	
if __name__ == "__main__":
  webbrowser.open_new("http://localhost:5001/")
  app.run(debug=True, port=5001)
	
	
