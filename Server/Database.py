import sqlite3
from datetime import date

class Database:
	def __init__(self):
		self.Connect()
		self.checkTableExists('video')
		self.conn.commit()
		self.conn.close()

	def checkTableExists(self,name):
		self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(name))
		tables = len(self.cursor.fetchall())
		if tables == 0: #if table not exist, create one
			self.cursor.execute("""CREATE TABLE video(
				id integer,
				Video text,
				name text,
				publisher text,
				view int,
				likee int,  
				dislike int, 
				datee text,
				image text)""")

	def Connect(self):
		self.conn = sqlite3.connect('DB/DataBase.db')
		self.cursor = self.conn.cursor()

	def GetCurrVideoId(self):
		self.Connect()
		self.cursor.execute("SELECT * FROM video")
		results = self.cursor.fetchall()
		currId = len(results)
		return currId

	def GetViews(self,VideoId):
		self.cursor.execute("SELECT view FROM video WHERE id == {}".format(VideoId))
		return self.cursor.fetchone()


	def GetVideo(self,VideoId): #add one to the watched before sending data
		self.Connect()
		self.cursor.execute(f"UPDATE video SET view = {self.GetViews(VideoId)[0]+1} WHERE id = {VideoId}")
		self.conn.commit()
		try:
			self.cursor.execute("SELECT * FROM video WHERE id == {}".format(VideoId))
		except:
			return 'ERROR'

		returnValue = self.cursor.fetchone()
		self.conn.close()
		return returnValue

	def GetDataBase(self):
		self.Connect()
		self.cursor.execute("SELECT * FROM video")
		return self.cursor.fetchall()

	def AddLines(self,data):
		self.Connect()
		self.cursor.executemany("INSERT INTO video VALUES (?,?,?,?,?,?,?,?,?)",data)
		self.conn.commit()
		self.conn.close()

	def GetLike(self,vidId):
		self.cursor.execute("SELECT likee FROM video WHERE id == {}".format(vidId))
		return self.cursor.fetchone()

	def GetDislikes(self,vidId):
		self.cursor.execute("SELECT dislike FROM video WHERE id == {}".format(vidId))
		return self.cursor.fetchone()

	def Like(self,vidId):
		self.Connect()
		print (self.GetLike(vidId)[0])
		self.cursor.execute(f"UPDATE video SET likee = {self.GetLike(vidId)[0]+1} WHERE id = {vidId}")
		self.conn.commit()
		print (self.GetLike(vidId)[0])
		self.conn.close()

	def Dislike(self,vidId):
		self.Connect()
		self.cursor.execute(f"UPDATE video SET dislike = {self.GetDislikes(vidId)[0]+1} WHERE id = {vidId}")
		self.conn.commit()
		self.conn.close()

