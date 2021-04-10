
from sqlalchemy import  ARRAY,Column,JSON
from app import db
from datetime import datetime

class Song(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	duration = db.Column(db.Integer, nullable=False)
	uploaded_time = db.Column(db.String, default = datetime.utcnow(), nullable=False)

	def   __repr__(self):
		return f"name :{self.name}, duration :{self.duration}  , uploaded_time:{self.uploaded_time}"


	def initial_validation(self,data):
		if not ("name" in data and "duration" in data):
			raise  AssertionError('Data is invalid')

	def validate_name(self, name):
		if len(name) >100:
			raise AssertionError('Song name is too long')
		else:
			self.name =name


	def validate_duration(self,duration):
		if not (duration and duration>=0):
			raise AssertionError('Duration should be positive')
		else :
			self.duration = duration

	

	@staticmethod
	def  songs_lists():
		songsData = []
		songs = Song.query.all()
		for song in songs :
			songsData.append({"name":song.name, "duration":song.duration ,"uploaded_time":song.uploaded_time, "id":song.id })
		return songsData

	@staticmethod
	def song(id):
		try :
			song = Song.query.filter_by(id=id).first()
			

			return True,{"name":song.name, "duration":song.duration ,"uploaded_time":song.uploaded_time, "id":song.id }
		except :
			return False,"No song found"

	@staticmethod
	def deleteSong(id):
		try :
			song = Song.query.filter_by(id=id).delete()
			print(song)
			db.session.commit()
			

			return True,{"msg": f"Song  has been deleted" }
		except :
			return False,"No song found"

	@staticmethod
	def getSong(id):
		try :
			song = Song.query.filter_by(id=id).first()
			print(song)
	
			
			return True,song
		except :
			return False,"No song found"






class Podcast(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	duration = db.Column(db.Integer, nullable=False)
	uploaded_time = db.Column(db.String, default = datetime.utcnow(),nullable=False)
	host = db.Column(db.String(100), nullable=False)
	participants =  db.Column(JSON, nullable=True)


	def initial_validation(self,data):

		if not ("name" in data  and "host" in data and "duration" in data):
			raise  AssertionError('Data is invalid')
		
		





	def validate_name(self, name):
		if len(name) >100:
			raise AssertionError('Song name is too long')
		else:
			self.name =name
	def validate_host(self, host):
		if len(host) >100:
			raise AssertionError('Host length is too long')
		else:
			self.host  = host 
	def validate_participants(self,participants):
		if   isinstance(participants, str) or    (isinstance(participants, list) and len(participants))>10:
			raise AssertionError('Participants are too many')
		elif isinstance(participants, list) and len(participants)<10:
			
			for participant in participants :

				if  not isinstance(participant, str) and len(participant)>100 :
					raise  AssertionError('Song name is too long')
		
			self.participants =  participants

	def validate_duration(self,duration):
		if not (duration and duration>=0):
			raise AssertionError('Duration should be positive')
		else :
			self.duration = duration


	


	@staticmethod
	def  podcast_lists():
		podcastsData = []
		podcasts= Podcast.query.all()
		for podcast in podcasts :
			if podcast.participants:
				podcastsData.append({"name":podcast.name, "duration":podcast.duration ,"uploaded_time":podcast.uploaded_time, "id":podcast.id,"participants" :podcast.participants })
			else:
				podcastsData.append({"name":podcast.name, "duration":podcast.duration ,"uploaded_time":podcast.uploaded_time, "id":podcast.id})
		return podcastsData

	@staticmethod
	def podcast(id):
		try :
			podcast = 	Podcast.query.filter_by(id=id).first()
			if podcast.participants:
				return True,{"name":podcast.name, "duration":podcast.duration ,"uploaded_time":podcast.uploaded_time, "id":podcast.id,"participants" :podcast.participants }
			
			return True,{"name":podcast.name, "duration":podcast.duration ,"uploaded_time":podcast.uploaded_time, "id":podcast.id}
			
		except :
			return False,"No Podcast found"

	@staticmethod
	def deletePodcast(id):
		try :
			podcast = Podcast.query.filter_by(id=id).delete()
			db.session.commit()
			

			return True,{"msg": f"Podcast  has been deleted" }
		except :
			return False,"No podcast found"


	@staticmethod
	def getPodcast(id):
		try :
			podcast = Podcast.query.filter_by(id=id).first()
	
			

			return True,podcast
		except :
			return False,"No song found"





class 	AudioBookFile(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	author = db.Column(db.String(100), nullable=False) 
	narrator = db.Column(db.String(100), nullable=False)
	uploaded_time = db.Column(db.String, default = datetime.utcnow() ,nullable=False)
	duration = db.Column(db.Integer, nullable=False)


	def initial_validation(self,data):
		if not ( "title" in data and "author" in data and "narrator" in data) :
			raise  AssertionError('Data is invalid')
	def validate_title(self, title):
		if len(title) >100:
			raise AssertionError('Title is too long')
		else:
			self.title =title
	def validate_author(self, author):
		if len(author) >100:
			raise AssertionError('Author name is too long')
		else:
			self.author =author
	def validate_narrator(self, narrator):
		if narrator and len(narrator) >100:
			raise AssertionError('Narrator name is too long')
		elif narrator:
			self.narrator =narrator
	def validate_duration(self,duration):
		if not (duration and duration>=0):
			raise AssertionError('Duration should be positive')
		else :
			self.duration = duration
	


	@staticmethod
	def  audioBook_lists():
		audioBookData = []
		audioBooks = AudioBookFile.query.all()
		for audioBook in audioBooks :
			audioBookData.append({"title":audioBook.title, "author":audioBook.author , "narrator" :audioBook.narrator,"uploaded_time":audioBook.uploaded_time, "id":audioBook.id ,"duration":audioBook.duration })
		return audioBookData

	@staticmethod
	def audioBook(id):
		try :
			audioBookFile = AudioBookFile.query.filter_by(id=id).first()

			

			return True,{"title":audioBookFile.title, "author":audioBookFile.author , "narrator" :audioBookFile.narrator,"uploaded_time":audioBookFile.uploaded_time, "id":audioBookFile.id, "duration":audioBookFile.duration }
		except :
			return False,"No Audio Book found"

	@staticmethod
	def deleteAudioBook(id):
		try :
			audioBook = AudioBookFile.query.filter_by(id=id).delete()
			db.session.commit()
			

			return True,{"msg": f"AudioBookFile  has been deleted" }
		except :
			return False,"No audioBook found"

	@staticmethod
	def getAudioBook(id):
		try :
			audioBook = AudioBookFile.query.filter_by(id=id).first()
	
			

			return True,audioBook
		except :
			return False,"No song found"

	



	



