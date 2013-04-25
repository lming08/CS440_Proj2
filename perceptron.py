from fileParser import *

specMode = True

def getRelativeFrequencies(topWords, currentFile, fileType):
	relaFreqs = {"DR":{}, "DT":{}, "L":{}}
	cleanData = cleanFile(currentFile )
        fileWords = cleanData.split(" ");
        totalN = float(len(fileWords))

	for eachType in topWords:
		for eachWord in topWords[eachType]:
			relaFreqs[eachType][eachWord[0]] = fileWords.count(eachWord[0])/totalN or 1/totalN
	return relaFreqs
	
def inputSum(relaFreqs, weights, type):
	runningTotal = float(0)
	#print relaFreqs
	#print weights[type]
	for eachWord in weights[type]:
		runningTotal += relaFreqs[eachWord]*weights[type][eachWord]
	return runningTotal

def getFileVectors(trainData, topWords):
	fileVectorsComplete = {}
	for eachType in trainData:
		fileVectors = {}
		for eachFile in trainData[eachType]:
			cleanData = cleanFile(eachFile)
        		fileWords = cleanData.split(" ");
			totalN = float(len(fileWords))
			currentVector = {}
			for eachTypeAgain in topWords:
				for eachWord in topWords[eachTypeAgain]:
					currentFreq = fileWords.count(eachWord[0])/totalN or 1/totalN 
					currentVector.update({eachWord[0]:currentFreq})
			fileVectors.update({eachFile:currentVector})
		fileVectorsComplete.update({eachType:fileVectors})
	return fileVectorsComplete

def getTestVectors(testData, topWords):
	fileVectors = {}
	for eachFile in testData:
		cleanData = cleanFile(eachFile)
                fileWords = cleanData.split(" ");
		totalN = float(len(fileWords))
		currentVector = {}
		for eachType in topWords:
			for eachWord in topWords[eachType]:
				currentFreq = fileWords.count(eachWord[0])/totalN or 1/totalN
				currentVector.update({eachWord[0]:currentFreq})
		fileVectors.update({eachFile:currentVector})
	return fileVectors

def perceptronStrat(trainData):
	if specMode == False:
		print "Starting Preproc"
	if useBooleanBag == False:
		topWordsDT = getNcommonishWords(cleanClass(trainData, "DT"), 20)
		topWordsDR = getNcommonishWords(cleanClass(trainData, "DR"), 20)
		topWordsL = getNcommonishWords(cleanClass(trainData, "L"), 20)
		topWords = {"DT":topWordsDT, "DR":topWordsDR, "L":topWordsL}
	else:
		topWords = getAttributeSets(trainData)

	fileVectors = getFileVectors(trainData, topWords)
	if specMode == False:
		print "Preproc complete"
	
	weights = {"DR":{}, "DT":{}, "L":{}}
	alpha = initialAlpha
	bias = 0
	for eachType in topWords:
		for eachWord in topWords[eachType]:
			weights[eachType][eachWord[0]] = initialWeight

	if specMode == False:
		print "Beginning training"
	for i in range(101):
                if specMode == False:
			print "Starting Iteration #" + str(i)
                for eachType in fileVectors:
                	for eachFile in fileVectors[eachType]:
				for eachPercept in weights:
                        		error = 0
                                	input = inputSum(fileVectors[eachType][eachFile], weights, eachPercept)
                                        if input >= perceptronThreshold and eachPercept != eachType:
                                                error = -1
					if input < perceptronThreshold and eachPercept == eachType:
						error = 1
                                        for eachWord in weights[eachPercept]:
                                                weights[eachPercept][eachWord] += alpha*error*fileVectors[eachType][eachFile][eachWord]
                alpha *= alphaDecay
	if specMode == False:
		print "Training Complete"
	#print "Resulting Weights"
	#for eachType in weights:
		#print eachType
		#for eachWeight in weights[eachType]:
			#print eachWeight + ", " + str(weights[eachType][eachWeight])
		#print "\n"
	
	return (weights, topWords)

def testPerceptrons(perceptrons, testData, topWords):
	if specMode == False:
		print "Preprocessing test data"
	fileResults = [];
	fileVectors = getTestVectors(testData, topWords)
	if specMode == False:
		print "Preproc complete"
		print "Beginning perceptron voting"

	for eachFile in fileVectors:
		results = castVotes(perceptrons, fileVectors[eachFile], topWords)
		fileResults.append((path.basename(eachFile), random.choice(results)))
        #for f in fileResults:
                #print fileResults.index(f), f

        #Calculate our results against actual
	if specMode == False:
		print "Perceptron voting complete"
		print "Calculating number of correct result"

        actualResults = file(testResultsFile).read()
        actualResults = actualResults.split('\n');
        dictResults = {}
        for fileName in actualResults:
                if ',' in fileName:
                        lineList = fileName.split(',');
                        dictResults[ lineList[0] ] =  lineList[1]

        totalResults = len( testData );
        totalCorrect = 0.0;
        for fileTuple in fileResults:
                if dictResults[fileTuple[0]] == fileTuple[1]:
                        totalCorrect += 1;
		#else:
		#	print str(fileTuple) + str(dictResults[fileTuple[0]])

        if specMode == False:
		print "Percent accurate = " + str(totalCorrect / totalResults)
	elif specMode == True:	
		for eachTuple in fileResults:
			print "Perceptron, " + str(eachTuple[0]) + ", " + str(eachTuple[1])
        return fileResults;

def castVotes(perceptrons, fileVector, topWords):
	result = []
	#print str(perceptrons) + "\n"
	#print str(topWords) + "\n"
	#print str(fileVector) + "\n"
	for eachType in topWords:
		runningTotal = float(0)
		for eachWord in topWords[eachType]:
			runningTotal += perceptrons[eachType][eachWord[0]]*fileVector[eachWord[0]]
		if runningTotal > perceptronThreshold:
			result += [eachType]
	if result == []:
		result = ["DT", "DR", "L"]
	return result
	
