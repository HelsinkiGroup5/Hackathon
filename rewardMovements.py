import numpy as np
import time
import rto

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import re
matplotlib.rcParams['figure.figsize'] = (18.0, 10.0)

rto = reload(rto)
N = 1000
class ProccessSkeletonJoint:
	def __init__(self):
		self.bufferSize = 18
		self.reset()
		self.mexp = rto.MotionExplorer(inputdim = 2, order = 4, number_of_stdev = 4)

	def addData(self, ms, d):
		if self.currentInputSize <  self.bufferSize:
			self.sumT = self.sumT + ms*1000
			self.sumX = self.sumX +d[0]
			self.sumY = self.sumY +d[1]
			self.currentInputSize = self.currentInputSize +1
		else:
			score, added = self.mexp.new_sample(int(self.sumT/self.bufferSize), (self.sumX/self.bufferSize, self.sumY/self.bufferSize))
			self.reset()
			return (score, added)
		return None

	def getObservations(self):
		return self.mexp.observations

	def reset(self):
		self.currentInputSize = 0
		self.sumX = 0
		self.sumY = 0
		self.sumT = 0


def processFile(filename):
	data = []
	with open(filename) as f:
		content = f.readlines()
	for c in content:
		d = re.findall(r"[-+]?\d*\.\d+|\d+",c)
		data.append(( float(d[0]), float(d[1]), float(d[2]), float(d[3]) ))	
	return data



if __name__ == '__main__':
	data = processFile("log.txt")
	lData = []
	rData = []


	psjLH = ProccessSkeletonJoint()
	psjRH = ProccessSkeletonJoint()

	# rSamplesT = np.cumsum(np.random.uniform(11,500, len(rData)).astype(int)) 
	# lSamplesT = np.cumsum(np.random.uniform(11,500, len(lData)).astype(int)) 

	rSamplesT = lSamplesT = []

	for d in data:
		t,h,x,y = d
		if h == 11:
			rData.append([x,y])
			rSamplesT.append(t)
		elif h == 7:
			lData.append([x,y])
			lSamplesT.append(t)
	# rSamplesT = np.cumsum(np.random.uniform(11,500, len(rData)).astype(int)) 
	# lSamplesT = np.cumsum(np.random.uniform(11,500, len(lData)).astype(int)) 
	# print "processing rigt hand"
	count  = 0
	for d in rData:
		r = psjRH.addData(rSamplesT[count],d)
		if r :
			score, added = r
			if added:
				print rSamplesT[count], d, score,added
		count = count +1
	print len(psjRH.getObservations())


	# print "processing left hand"
	count  = 0
	for d in lData:
		r = psjLH.addData(lSamplesT[count],d)
		if r :
			score, added = r
			if added:
				print lSamplesT[count], d, score,added
		count = count +1
	print len(psjLH.getObservations())

	# nsamples = 200
	# samples_t = np.cumsum(np.random.uniform(11,500, nsamples).astype(int))
	# samples = 100 * np.random.random((nsamples,2))
	# count = 0
	# for s in samples:
	# 	newms = int(round(time.time() * 1000))

	# 	score, added = psj.addData(samples_t[count],s)
	# 	if added:
	# 		print newms, s, score,added
	# 	count = count +1
	# print len(psj.getObservations())
