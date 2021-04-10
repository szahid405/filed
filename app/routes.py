from app import app,db
from flask import jsonify ,request
from app.model import Song,Podcast,AudioBookFile
from sqlalchemy.exc import SQLAlchemyError

audioFileTypes = ["1", "2", "3"]
@app.route('/')
@app.route('/index')
def index():
	db.drop_all()
	db.create_all()
	
	return jsonify("App is up and running")





@app.route('/get/<audioFileType>',methods=["GET"])
def get_audio_files(audioFileType):
	'''This method gies the list of audio file by their types'''
	if audioFileType not in audioFileTypes:
		return jsonify(msg ="Inavlid file format"),400
	else:
		try :
			if audioFileType =="1":
				return jsonify(songs = Song.songs_lists())

			elif audioFileType == "2":
				return jsonify(podcasts = Podcast.podcast_lists())

			elif audioFileType == "3" :
				return jsonify(audiobooks= AudioBookFile.audioBook_lists())
		except:
				return jsonify(msg ="Invalid request"), 400



@app.route('/get/<audioFileType>/<int:audioFileID>',methods=["GET"])
def get_induvidual_audio_file(audioFileType,audioFileID):
	'''This method gies the audio file by its type and it'''

	if audioFileType not in audioFileTypes:
		return jsonify(msg ="Inavlid file format"),400
	else:
		try :

			if audioFileType =="1":
				flag , songs = Song.song(audioFileID)
				if flag :
					return jsonify(song = songs)
				else :
					return jsonify(msg ="No record found"), 400

			elif audioFileType == "2":
				flag,podcasts = Podcast.podcast(audioFileID)
				if flag :
					return jsonify(podcast = podcasts)
				else:
					return jsonify(msg ="No record found"), 400


			elif  audioFileType == "3":
				flag ,audioBooks=  AudioBookFile.audioBook(audioFileID)
				if flag :
					return jsonify(audioBooks = audioBooks)
				else:
					return jsonify(msg ="No record found"), 400

			return jsonify(msg ="Invalid request"), 400
		except:
			return jsonify(msg ="Invalid request"), 400





@app.route('/audio/create/', methods =["GET","POST"])
def create_audio():
	if request.method != 'POST':
		return  jsonify(msg ="Invalid request"), 400
	data = request.json
	try :
		audioFileType = data["audioFileType"]
		audioFileMetaData = data["audioFileMetaData"]
		if audioFileType == 1:
			try:
				song = Song()
				song.initial_validation(audioFileMetaData)
				song.validate_name(audioFileMetaData["name"])
				song.validate_duration(audioFileMetaData["duration"])
				db.session.add(song)
				db.session.commit()
				return jsonify(msg ="Song successfully added"), 200


			except :
  				db.session.rollback()
  				return jsonify(msg ="Internal server error"), 500
			
			
			
		elif audioFileType ==2 :
			try :
				podcast = Podcast()
				podcast.initial_validation(audioFileMetaData)
				podcast.validate_name(audioFileMetaData["name"])
				podcast.validate_duration(audioFileMetaData["duration"])
				podcast.validate_host(audioFileMetaData["host"])
				if "participants" in audioFileMetaData:
					podcast.validate_participants(audioFileMetaData["participants"])

				db.session.add(podcast)
				db.session.commit()
				return jsonify(msg ="Podcast successfully added"), 200
			except :
  				db.session.rollback()
  				return jsonify(msg ="Internal server error"), 500


			
		elif audioFileType==3 :
			try :
				audioBookFile = AudioBookFile()
				audioBookFile.initial_validation(audioFileMetaData)
				audioBookFile.validate_title(audioFileMetaData["title"])
				audioBookFile.validate_author(audioFileMetaData["author"])
				audioBookFile.validate_narrator(audioFileMetaData["narrator"])
				audioBookFile.validate_duration(audioFileMetaData["duration"])
				db.session.add(audioBookFile)
				db.session.commit()
				return jsonify(msg ="Audio Book File successfully added"), 200
			except :
  				db.session.rollback()
  				return jsonify(msg ="Internal server error"), 500

	except : 
		return jsonify(msg='Please check your data'), 400








@app.route('/delete/<audioFileType>/<int:audioFileID>',methods=["POST"])
def  delete_induvidual_file_by_type_and_id(audioFileType,audioFileID):
	if audioFileType not in audioFileTypes:
		return jsonify(msg ="Inavlid file format"),400
	else:
		try :

			if audioFileType =="1":
				print(audioFileType,audioFileID)
				flag , songs = Song.deleteSong(audioFileID)
				if flag :
					return jsonify(songs = songs)
				else :
					return jsonify(msg ="No song found"), 400

			elif audioFileType == "2":
				flag,podcasts = Podcast.deletePodcast(audioFileID)
				if flag :
					return jsonify(podcasts = podcasts)
				else:
					return jsonify(msg ="No podcast found"), 400


			elif  audioFileType == "3":
				flag ,audioBooks=  AudioBookFile.deleteAudioBook(audioFileID)
				if flag :
					return jsonify(audioBooks = audioBooks)
				else:
					return jsonify(msg ="No AudioBookFile Found"), 400

			return jsonify(msg ="Invalid request"), 400
		except:
			return jsonify(msg ="Invalid request"), 400








@app.route('/update/<int:audioFileType>/<int:audioFileID>',methods=["POST"])
def  update_induvidual_file_by_type_and_id(audioFileType,audioFileID):

	if request.method != 'POST':
		return  jsonify(msg ="Invalid request"), 400
	data = request.json
	try :
		audioFileMetaData = data["audioFileMetaData"]
		print(audioFileMetaData)
		if audioFileType == 1:
			print(audioFileType)
			try:
				flag,song = Song.getSong(audioFileID)
				
				if song :


					song.initial_validation(audioFileMetaData)
					song.validate_name(audioFileMetaData["name"])
					song.validate_duration(audioFileMetaData["duration"])
					db.session.commit()
					return jsonify(msg ="Song successfully updated"), 200
				else:
					return jsonify(msg ="Validation error"), 400



			except :
  				db.session.rollback()
  				return jsonify(msg ="Internal server error"), 500
			
			
			
		elif audioFileType ==2 :
			try :
				flag,podcast = Podcast.getPodcast(audioFileID)
				if flag:
					podcast.initial_validation(audioFileMetaData)
					podcast.validate_name(audioFileMetaData["name"])
					podcast.validate_duration(audioFileMetaData["duration"])
					podcast.validate_host(audioFileMetaData["host"])
					if "participants" in audioFileMetaData:
						print("len")
						print(len(audioFileMetaData["participants"][0]))
						podcast.validate_participants(audioFileMetaData["participants"])

					db.session.commit()
					return jsonify(msg ="Podcast successfully updated"), 200
				else:
					return jsonify(msg ="Internal server error"), 500
			except :
  				db.session.rollback()
  				return jsonify(msg ="Internal server error"), 500


			
		elif audioFileType==3 :
			try :
				flag,audioBookFile = AudioBookFile.getAudioBook(audioFileID)
				if flag:
					audioBookFile.initial_validation(audioFileMetaData)
					audioBookFile.validate_title(audioFileMetaData["title"])
					audioBookFile.validate_author(audioFileMetaData["author"])
					audioBookFile.validate_narrator(audioFileMetaData["narrator"])
					db.session.commit()
					return jsonify(msg ="Audio Book File successfully updated"), 200
				else:
					return jsonify(msg ="Internal server error"), 500
			except :
  				db.session.rollback()
  				return jsonify(msg ="Internal server error"), 500

	except : 
		return jsonify(msg='Please check your data'), 400
	return jsonify(msg='Please check your data'), 400
	





