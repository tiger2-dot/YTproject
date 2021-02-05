from Client import Network
import time
import cv2
from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import sys


class MainGUI(QMainWindow):
	def __init__(self,network):
		super(MainGUI,self).__init__()
		self.network = network
		self.MainUI(0)
		self.SideBarUI()


	def SideBarUI(self):
		self.borderLabel = QLabel(self)
		self.borderLabel.setStyleSheet("border: 1px solid black;") 
		self.borderLabel.move(1600,0)
		self.borderLabel.resize(220,920)
		self.borderLabel.setStyleSheet("border-image : url(imgs/back.png);")

		self.logoButt = QtWidgets.QPushButton(self)
		self.logoButt.setGeometry(1595,10,220,150)
		self.logoButt.setStyleSheet("border-image : url(imgs/logo.png);")

		self.uploadButt = QtWidgets.QPushButton(self)
		self.uploadButt.setText("     Upload a Video")
		self.uploadButt.clicked.connect(lambda: self.ClickSideButt('upload'))
		self.uploadButt.setGeometry(1600,425,220,50)
		self.uploadButt.setFont(QFont('Times',12))
		self.uploadButt.setStyleSheet("background-color : white") 
		self.uploadButt.setIcon(QIcon('imgs/icon.png'))
		self.uploadButt.setIconSize(QtCore.QSize(50,50))

		self.ManageButt = QtWidgets.QPushButton(self)
		self.ManageButt.setText("    Manage Account")
		self.ManageButt.clicked.connect(lambda: self.ClickSideButt('manageAcc'))
		self.ManageButt.setGeometry(1600,350,220,50)
		self.ManageButt.setFont(QFont('Times',12))
		self.ManageButt.setStyleSheet("background-color : white") 
		self.ManageButt.setIcon(QIcon('imgs/mngAcc.png'))
		self.ManageButt.setIconSize(QtCore.QSize(50,50))

		self.DisLiked = QtWidgets.QPushButton(self)
		self.DisLiked.setText("   Disliked Videos")
		self.DisLiked.clicked.connect(lambda: self.ClickSideButt('disliked'))
		self.DisLiked.setGeometry(1600,275,220,50)
		self.DisLiked.setFont(QFont('Times',12))
		self.DisLiked.setStyleSheet("background-color : white") 
		self.DisLiked.setIcon(QIcon('imgs/dislike.png'))
		self.DisLiked.setIconSize(QtCore.QSize(50,50))

		self.liked = QtWidgets.QPushButton(self)
		self.liked.setText("   Liked Videos")
		self.liked.clicked.connect(lambda: self.ClickSideButt('liked'))
		self.liked.setGeometry(1600,200,220,50)
		self.liked.setFont(QFont('Times',12))
		self.liked.setStyleSheet("background-color : white") 
		self.liked.setIcon(QIcon('imgs/like.png'))
		self.liked.setIconSize(QtCore.QSize(50,50))

		self.about = QtWidgets.QPushButton(self)
		self.about.setText("About The Creator")
		self.about.clicked.connect(lambda: self.ClickSideButt('about'))
		self.about.setGeometry(1600,650,220,50)
		self.about.setFont(QFont("Times",12, weight = QtGui.QFont.Bold))
		self.about.setStyleSheet("background-color : white") 


	def MainUI(self,videoCounter):
		#videoCounter = 0
		self.IDs = []

		back = QLabel(self)
		back.setStyleSheet("border: 1px solid black;") 
		back.move(0,0)
		back.resize(1600,920)
		back.setStyleSheet("border-image : url(imgs/back2.png);")


		for y in range(0,2):
			for x in range(0,5):
				data = self.network.Recommended(videoCounter)
				videoCounter += 1

				if data == 'ERROR':
					break

				name,publisher,views,date,vidId,img = data[0],data[1],data[2],data[3],data[4],data[5]

				self.IDs.append(vidId)

				date = str(date).split('-')
				date = "{}/{}/{}".format(date[2],date[1],date[0])

				newImg = open('GuiCache/{}.png'.format(videoCounter),'wb') #saving the image in order to show it latter
				newImg.write(img)
				newImg.close()

				self.vid = QLabel(self) #Showing the preview img
				self.vid.setGeometry(45 + (290 * x),115 + (320 * y),210,170)
				self.vid.setStyleSheet("border-image : url(GuiCache/{}.png);".format(videoCounter))

				self.name = QLabel(self) #The name of the video
				self.name.setText(name)
				self.name.setGeometry(45 + (290 * x),297 + (320 * y),210,50)
				self.name.setFont(QFont("Times",11,weight = QtGui.QFont.Bold))
				self.name.setWordWrap(True)

				self.publisher = QLabel(self) #The name of the publisher
				self.publisher.setText(publisher)
				self.publisher.setGeometry(45 + (290 * x),339 + (320 * y),180,20)
				self.publisher.setFont(QFont("Times",11))

				self.viewsNdate = QLabel(self) #The number of views and the publish date
				self.viewsNdate.setText("{} views ~ {}".format(views,date))
				self.viewsNdate.setGeometry(45 + (290 * x),375 + (320 * y),180,20)


	def mousePressEvent(self,event): #when presing the vid than understanding what is the id of the current vid and calling it
		xPos = event.x()
		yPos = event.y()
		counter = 0

		if xPos >= 45 and xPos <=1360 and yPos >= 115 and yPos <= 720: #checking if clicking in the button areas
			X = int((xPos - 45)/290)
			Y = int((yPos - 115)/320)
			isBrake = False
			for y in range(0,2):
				for x in range(0,5):
					if x >= X and y >= Y:
						isBrake = True
						break
					else:
						counter += 1
				if isBrake == True:
					break

			self.vidId = self.IDs[counter]
			moreGui = MoreGUI("show,{}".format(self.vidId), self.network)
			widget.addWidget(moreGui)
			widget.setCurrentIndex(widget.currentIndex() + 1)


	def ClickSideButt(self,arg):
		moreGui = MoreGUI(arg,self.network)
		widget.addWidget(moreGui)
		widget.setCurrentIndex(widget.currentIndex() + 1)
	


class MoreGUI(QWidget):
	def __init__(self,func,network):
		super(MoreGUI,self).__init__()
		self.network = network

		self.HHoleBox = QHBoxLayout()
		self.VSideBar = QVBoxLayout()

		self.func = func.split(',')

		if self.func[0] == "upload":
			self.Upload()
		if self.func[0] == 'show':
			self.ShowVid(self.func[1])

		self.SideBarUI()

		self.setLayout(self.HHoleBox)
		

	def ShowVid(self, vidId): #BUILD THE WINDOW THAT SHOWS VIDEO
		data = self.network.GetVideo(vidId) #[name,publisher,view,like,dislike,date,vidData]
		video = data[6]

		newVid = open('GuiCache/{}.mp4'.format(vidId),'wb')
		newVid.write(video)
		newVid.close()

		#CREATE MEDIA PLAYER AND VIDEO WIDGETS
		self.mediaPlayer = QMediaPlayer(None,QMediaPlayer.StreamPlayback)

		self.videoWidget = QVideoWidget()

		self.playButt = QtWidgets.QPushButton(self)
		self.playButt.setEnabled(True)
		self.playButt.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay)) #CHANGE ICON WHEN PLAY AND STOP, AND DIRECTORY
		self.playButt.clicked.connect(self.play)

		self.slider = QtWidgets.QSlider(Qt.Horizontal)
		self.slider.setRange(0,0)
		self.slider.sliderMoved.connect(self.setPosition)

		self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile('GuiCache/{}.mp4'.format(vidId))))
		self.mediaPlayer.setVideoOutput(self.videoWidget)

		#CREATING INFO LABELS
		nameL = QLabel(self)
		nameL.setText(data[0])
		nameL.setFont(QFont('Times',15))

		self.like = QtWidgets.QPushButton(self)
		self.like.setText(data[3])
		self.like.clicked.connect(lambda: self.addLike(vidId))
		self.like.setIcon(QIcon('imgs/like.png'))
		self.like.setIconSize(QtCore.QSize(50,50))

		self.dislike = QtWidgets.QPushButton(self)
		self.dislike.setText(data[4])
		self.like.clicked.connect(lambda: self.addDislike(vidId))
		self.dislike.setIcon(QIcon('imgs/dislike.png'))
		self.dislike.setIconSize(QtCore.QSize(50,50))

		self.date = QLabel(self)
		self.date.setText(f"Date of upload: {data[5]}")
		self.date.setFont(QFont('Times',15))

		self.publisher = QLabel(self)
		self.publisher.setText(f"Uploaded by: {data[1]}")
		self.publisher.setFont(QFont('Times',15))

		self.views = QLabel(self)
		self.views.setText(f"{data[2]} views")
		self.views.setFont(QFont('Times',15))


		#CREATING LAYOUTS AND PLACING EVERYTHING
		hboxLayout = QHBoxLayout()
		hboxLayout.addWidget(self.playButt)
		hboxLayout.addWidget(self.slider)

		nameBoxLayout = QHBoxLayout()
		nameBoxLayout.addWidget(nameL) 

		infoBoxLayout = QHBoxLayout()
		infoBoxLayout.addWidget(self.like) 
		infoBoxLayout.addWidget(self.dislike) 
		infoBoxLayout.addSpacing(950)
		infoBoxLayout.addWidget(self.date) 
		infoBoxLayout.addSpacing(50)
		infoBoxLayout.addWidget(self.views) 

		publisherBox = QHBoxLayout()
		publisherBox.addStretch(1)
		publisherBox.addWidget(self.publisher)

		vboxLayout = QVBoxLayout()
		vboxLayout.addWidget(self.videoWidget,17)
		vboxLayout.addLayout(hboxLayout,1)
		vboxLayout.addLayout(nameBoxLayout,1)
		vboxLayout.addLayout(infoBoxLayout,1)
		vboxLayout.addLayout(publisherBox,1)

		self.HHoleBox.addLayout(vboxLayout)
		self.HHoleBox.addSpacing(235)

		self.mediaPlayer.positionChanged.connect(self.positionChanged)
		self.mediaPlayer.durationChanged.connect(self.durationChanged)


	def positionChanged(self,position):
		self.slider.setValue(position)

	def durationChanged(self,duration):
		self.slider.setRange(0, duration)

	def setPosition(self,position):
		self.mediaPlayer.setPosition(position)

	def play(self):
		if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
			self.mediaPlayer.pause()
		else:
			self.mediaPlayer.play()


	def addLike(self,vidId):
		self.network.addLike(vidId)

	def addDislike(self,vidId):
		self.network.addDislike(vidId)

	def Logo(self):
		try:
			if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
				self.mediaPlayer.pause()
		except:
			pass

		mainWindow = MainGUI(self.network)
		widget.addWidget(mainWindow)
		widget.setCurrentIndex(widget.currentIndex() + 1)

	def Upload(self):
		self.nameL = QLabel(self)
		self.nameL.setText('Please enter the name of the video: ')
		self.nameL.move(600,100)
		self.nameL.resize(200,50)

		self.enterName = QLineEdit(self)
		self.enterName.setGeometry(800,115,150,20)

		self.publL = QLabel(self)
		self.publL.setText('Please enter the name of the publisher: ')
		self.publL.move(600,200)
		self.publL.resize(200,50)

		self.enterPublisher = QLineEdit(self)
		self.enterPublisher.setGeometry(800,215,150,20)

		self.vidData = b''
		self.uplVid = QtWidgets.QPushButton(self)
		self.uplVid.setGeometry(700,300,150,50)
		self.uplVid.setText('Click to upload the vid')
		self.uplVid.clicked.connect(self.uploadVid)

		self.imgData = b''
		self.uplImg = QtWidgets.QPushButton(self)
		self.uplImg.setGeometry(650,400,300,50) 
		self.uplImg.setText('Click to upload the img / ABLE TO UPLOAD ONLY PNG')
		self.uplImg.clicked.connect(self.uploadImg)

		self.sendData = QtWidgets.QPushButton(self)
		self.sendData.setGeometry(700,500,150,50)
		self.sendData.setText('Upload')
		self.sendData.clicked.connect(self.senddata)
		

	def senddata(self):
		self.network.Upload([self.vidData,self.enterName.text(),self.enterPublisher.text(),self.imgData])


	def uploadImg(self):
		filePath, K = QFileDialog.getOpenFileName(self, 'Open Video File', 'C:\\Users\\natal\\Desktop\\Daniel\\SchooldProjects\\py\\YTproject', 'Video files (*.png)')
		try:
			file = open(filePath, 'rb')
		except:
			return
		self.imgData = file.read()

	def uploadVid(self):
		filePath, K = QFileDialog.getOpenFileName(self, 'Open Video File', 'C:\\Users\\natal\\Desktop\\Daniel\\SchooldProjects\\py\\YTproject', 'Video files (*.mp4)')
		try:
			file = open(filePath, 'rb')
		except:
			return
		self.vidData = file.read()
	

	def SideBarUI(self):
		self.borderLabel = QLabel(self)
		self.borderLabel.setStyleSheet("border: 1px solid black;") 
		self.borderLabel.move(1600,0)
		self.borderLabel.resize(220,920)
		self.borderLabel.setStyleSheet("border-image : url(imgs/back.png);")
		
		self.logoButt = QtWidgets.QPushButton(self)
		self.logoButt.clicked.connect(self.Logo)
		self.logoButt.setGeometry(1595,10,220,150)
		self.logoButt.setStyleSheet("border-image : url(imgs/logo.png);")

		self.uploadButt = QtWidgets.QPushButton(self)
		self.uploadButt.setText("     Upload a Video")
		self.uploadButt.clicked.connect(lambda: self.ClickSideButt('upload'))
		self.uploadButt.setGeometry(1600,425,220,50)
		self.uploadButt.setFont(QFont('Times',12))
		self.uploadButt.setStyleSheet("background-color : white") 
		self.uploadButt.setIcon(QIcon('imgs/icon.png'))
		self.uploadButt.setIconSize(QtCore.QSize(50,50))

		self.ManageButt = QtWidgets.QPushButton(self)
		self.ManageButt.setText("    Manage Account")
		self.ManageButt.clicked.connect(lambda: self.ClickSideButt('manageAcc'))
		self.ManageButt.setGeometry(1600,350,220,50)
		self.ManageButt.setFont(QFont('Times',12))
		self.ManageButt.setStyleSheet("background-color : white") 
		self.ManageButt.setIcon(QIcon('imgs/mngAcc.png'))
		self.ManageButt.setIconSize(QtCore.QSize(50,50))

		self.DisLiked = QtWidgets.QPushButton(self)
		self.DisLiked.setText("   Disliked Videos")
		self.DisLiked.clicked.connect(lambda: self.ClickSideButt('disliked'))
		self.DisLiked.setGeometry(1600,275,220,50)
		self.DisLiked.setFont(QFont('Times',12))
		self.DisLiked.setStyleSheet("background-color : white") 
		self.DisLiked.setIcon(QIcon('imgs/dislike.png'))
		self.DisLiked.setIconSize(QtCore.QSize(50,50))

		self.liked = QtWidgets.QPushButton(self)
		self.liked.setText("   Liked Videos")
		self.liked.clicked.connect(lambda: self.ClickSideButt('liked'))
		self.liked.setGeometry(1600,200,220,50)
		self.liked.setFont(QFont('Times',12))
		self.liked.setStyleSheet("background-color : white") 
		self.liked.setIcon(QIcon('imgs/like.png'))
		self.liked.setIconSize(QtCore.QSize(50,50))

		self.about = QtWidgets.QPushButton(self)
		self.about.setText("About The Creator")
		self.about.clicked.connect(lambda: self.ClickSideButt('about'))
		self.about.setGeometry(1600,650,220,50)
		self.about.setFont(QFont("Times",12, weight = QtGui.QFont.Bold))
		self.about.setStyleSheet("background-color : white")





network = Network()
app = QApplication(sys.argv)
mainWindow = MainGUI(network)

widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedWidth(1820)
widget.setFixedHeight(920)
widget.show()


sys.exit(app.exec_())



