import csv
import datetime
import glob, os



class AnalyzeFile(object):
	TIME_THRESHOLD = 5 # in seconds

	LIDAR_VEH_DIST_THRESHOLD = 200
	LIDAR_CAR_SIZE_MIN_THRESHOLD = 3
	LIDAR_CAR_SIZE_MAX_THRESHOLD = 8
	LIDAR_TRK_SIZE_MAX_THRESHOLD = 13

	LIDAR_PED_DIST_THRESHOLD = 300
	LIDAR_PED_SIZE_MIN_THRESHOLD = 0
	LIDAR_PED_SIZE_MAX_THRESHOLD = 2

	def __init__(self):
		self.tripNo = 0


	def analyze(self):
		# Iterate over all the files in the data folder.
		# After processing, move data to a dataProcessing folder.

		#os.chdir("/mydir")
		for fileName in glob.glob("data_*.csv"):
			with open(fileName, 'r') as readFile:
				reader = csv.reader(readFile)

				self.resetTripVariables()
				self.iterateOverRows(reader)

	def iterateOverRows(self,reader):
		for row in reader:
			absTime = datetime.datetime.strptime(row[0],'%m-%d-%Y-%H-%M-%S')
			self.setReferenceTime(absTime)

			relTime = (absTime - self.refTime).total_seconds()
			
			if self.checkTripEnd(relTime): continue
			self.prevTime = relTime

			self.checkForCars(relTime,row[3],row[4])





			#print relTime, row[1:], self.tripNo

	def printSummary(self):
		print "\n Trip " + str(self.tripNo) + " Summary ************"
		print "Number of parked cars: " + str(self.carCount)
		print "Number of parked trucks:" + str(self.truckCount)

		print "Approx. number of pedestrians / other short obstacles: " + str(self.pedCount)


	def resetTripVariables(self):
		self.prevTime = 0
		self.refTime = 0
		self.firstPass = True
		self.resetAnalysisVariables()

	def setReferenceTime(self,absTime):
		if self.firstPass:
			self.tripNo += 1
			self.refTime = absTime
			self.firstPass = False

	def checkTripEnd(self,relTime): 
		if (relTime - self.prevTime) > AnalyzeFile.TIME_THRESHOLD:
			self.printSummary()
			self.resetTripVariables()
			return True
		return False

	def resetAnalysisVariables(self):
		self.vehicleDetect = 0
		self.carCount = 0
		self.truckCount = 0

		self.pedDetect = 0
		self.pedCount = 0

	def resetVehicleDetect(self):
		if (AnalyzeFile.LIDAR_CAR_SIZE_MIN_THRESHOLD<self.vehicleDetect<AnalyzeFile.LIDAR_CAR_SIZE_MAX_THRESHOLD):
			self.carCount += 1
		elif (AnalyzeFile.LIDAR_CAR_SIZE_MAX_THRESHOLD<self.vehicleDetect<AnalyzeFile.LIDAR_TRK_SIZE_MAX_THRESHOLD):
			self.truckCount += 1
		
		self.vehicleDetect = 0

	def resetPedDetect(self):
		if (AnalyzeFile.LIDAR_PED_SIZE_MIN_THRESHOLD<self.vehicleDetect<AnalyzeFile.LIDAR_PED_SIZE_MAX_THRESHOLD):
			self.pedCount += 1
		
		self.pedDetect = 0

	def checkForCars(self,relTime,lidar1,lidar2):
		#housekeeping
		try:
			lidar1, lidar2 = int(lidar1), int(lidar2)
		except ValueError:
			#skip this value.
			return

		if (lidar2 < AnalyzeFile.LIDAR_VEH_DIST_THRESHOLD):
			#maybe a vehicle if it persists.
			self.vehicleDetect += 1
		else:
			self.resetVehicleDetect()

		if (AnalyzeFile.LIDAR_VEH_DIST_THRESHOLD< lidar2 < AnalyzeFile.LIDAR_PED_DIST_THRESHOLD):
			#maybe a pedestrian or some lamp posts if it doesn't persist.
			self.pedDetect += 1
		else:
			self.resetPedDetect()		


if __name__ == "__main__":
    a = AnalyzeFile()
    a.analyze()