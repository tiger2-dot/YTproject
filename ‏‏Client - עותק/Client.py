import socket
import pickle

class Network:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.HOST = socket.gethostname()
		self.PORT = 5520
		self.Connect()

	def Connect(self):
		self.client.connect((self.HOST,self.PORT))

	def GetBigData(self,size):
		RUN = True

		data = b''
		while RUN:
			packet = self.client.recv(size)
			howManyPacketWillBeSent = packet[0:2]
			currentPacketIndex = packet[2:4]
			actualData = packet[4:]

			data += actualData

			#currentPacketIndex = int.from_bytes(currentPacketIndex,byteorder = 'big')
			#howManyPacketWillBeSent = int.from_bytes(howManyPacketWillBeSent,byteorder = 'big')

			if howManyPacketWillBeSent <= currentPacketIndex:
				RUN = False

			self.client.send(str('a').encode()) # just sending something to let the server know we are ready for another packet

		return data


	def CreatePacketList(self,data,amountOfData = 8186):

		numOfPackets = int(len(data)/amountOfData) 
		listOfPackets = []

		for index in range(0,numOfPackets+1):
			packet = b''

			packet += numOfPackets.to_bytes(2, byteorder = 'big') #how many packets will be sent until full image will be done
			packet += index.to_bytes(2, byteorder = 'big') #what is the number of the current packet
			
			packet += data[amountOfData*index:amountOfData*(index+1)]

			listOfPackets.append(packet)

		return listOfPackets
		
	def GetVideo(self,id): 
		self.client.send(str('Video,{}'.format(id)).encode())

		generalInfo = self.client.recv(2048).decode() #"name,publisher,view,like,dislike,date"

		if generalInfo != 'ERROR':
			generalInfo = generalInfo.split(',')
		else:
			return

		self.client.send(str('video').encode())

		vidData = self.GetBigData(8192)

		generalInfo.append(vidData) #name,publisher,view,like,dislike,date,vidData

		return generalInfo

	def Upload(self, info): #info suppose to be like: [b'VIDEO DATA', name, publisher, b'IMAGE DATA']
		self.client.send(str('Upload,').encode())
		video = info[0]
		img = info[3]
		if self.client.recv(1024).decode() == 'ready': #READY TO RECIEVE VIDEO NAME AND PUBLISHER
			name, publisher = info[1], info[2]
			names = "{},{}".format(name,publisher)
			self.client.send(names.encode())
		if self.client.recv(1024).decode() == 'sendVideo': #READY TO RECIEVE VIDEO
			packets = self.CreatePacketList(video)
			for p in packets:
				self.client.send(p)
				a = self.client.recv(16)
		if self.client.recv(1024).decode() == 'sendImg': #READY TO RECIEVE IMG
			packets = self.CreatePacketList(img)
			for p in packets:
				self.client.send(p)
				a = self.client.recv(16)


	def Recommended(self, vidIndex): #vidIndex is a number: 0,1,2 and so on
		self.client.send(str("Recommended,{}".format(vidIndex)).encode())
		info = self.client.recv(2048).decode() #recieveing data at the format of: name,publisher,views,date,vidId
		if info != 'ERROR':
			info = info.split(',')
		else:
			return ('ERROR')
		self.client.send(str("Img").encode())
		img = self.GetBigData(8192)
		info.append(img)
		return info #returning: [name,publisher,views,date,vidId,img]

	def Disconnect(self): #To Disconnect
		self.client.send(str('disconnect,').encode())

	def addLike(self,vidId):
		self.client.send(str("Like,{}".format(vidId)).encode())

	def addDislike(self,vidId):
		self.client.send(str("Dislike,{}".format(vidId)).encode())