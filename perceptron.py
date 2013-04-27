from fileParser import *

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
	#print weights
	#print type
	#print "\n"
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
			currentVector = {}
			for eachTypeAgain in topWords:
				totalN = float(0)
				for eachWord in topWords[eachTypeAgain]:
					currentFreq = fileWords.count(eachWord[0]) or 1
					currentVector.update({eachWord[0]:currentFreq})
					totalN += currentFreq
                        	for eachWord in topWords[eachTypeAgain]:
                                	currentFreq = currentVector[eachWord[0]]/totalN
                                	currentVector.update({eachWord[0]:currentFreq})
			fileVectors.update({eachFile:currentVector})
		fileVectorsComplete.update({eachType:fileVectors})
	return fileVectorsComplete

def getFileVectors10(trainingFiles, topWords, results):
	fileVectorsComplete = {"DT":{}, "DR":{}, "L":{}}
	fileVectors = {}
        for eachFile in trainingFiles:
       		cleanData = cleanFile(eachFile)
                fileWords = cleanData.split(" ");
                currentVector = {}
		for eachType in topWords:
			totalN = float(0)
                	for eachWord in topWords[eachType]:
                		currentFreq = fileWords.count(eachWord[0])or 1
				totalN += currentFreq
                        	currentVector.update({eachWord[0]:currentFreq})
			for eachWord in topWords[eachType]:
				currentFreq = currentVector[eachWord[0]]/totalN
				currentVector.update({eachWord[0]:currentFreq})
		fileVectors = fileVectorsComplete[results[path.basename(eachFile)]]
		fileVectors.update({path.basename(eachFile):currentVector})
                fileVectorsComplete.update({results[path.basename(eachFile)]:fileVectors})
        return fileVectorsComplete

def getTestVectors(testData, topWords):
	fileVectors = {}
	for eachFile in testData:
		cleanData = cleanFile(eachFile)
                fileWords = cleanData.split(" ");
		currentVector = {}
		for eachType in topWords:
			totalN = float(0)
			for eachWord in topWords[eachType]:
				currentFreq = fileWords.count(eachWord[0]) or 1
				currentVector.update({eachWord[0]:currentFreq})
				totalN += currentFreq
			for eachWord in topWords[eachType]:
                                currentFreq = currentVector[eachWord[0]]/totalN
                                currentVector.update({eachWord[0]:currentFreq})
		fileVectors.update({eachFile:currentVector})
	return fileVectors

def perceptronStrat(trainData):
	if specMode == False:
		print "Starting Preproc"
	topWords = getAttributeSets(trainData)
	longestType = trainData.items()[0][0]
	for eachType in trainData:
		if len(trainData[eachType]) >= len(trainData[longestType]):
			longestType = eachType

	fileVectors = getFileVectors(trainData, topWords)
	if specMode == False:
		print "Preproc complete"
	
	types = ["DR", "DR", "L"]
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
			
		#for i in range(len(trainData[longestType])):
		#	for eachType in types:
		#		if i <= len(trainData[eachType]):
		#			currentVector = fileVectors[eachType].items()[i][1]
		#			#print currentVector
		#			#raw_input()
		#			for eachPercept in weights:
		#				error = 0;
		#				input = inputSum(currentVector, weights, eachPercept)
		#				if input >= perceptronThreshold and eachPercept != eachType:
		#					error = -1
		#				if input < perceptronThreshold and eachPercept == eachType:
		#					error = 1
		#				for eachWord in weights[eachPercept]:
		#					weights[eachPercept][eachWord] += alpha*error*currentVector[eachWord]
		#	
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

def perceptronStrat10(trainingFiles, results, topWords):
	if specMode == False:
		print "Starting Preproc"

	fileVectors = getFileVectors10(trainingFiles, topWords, results)
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
                	for eachFile in trainingFiles:
				justName = path.basename(eachFile)
				fileType = results[justName]
				fileVector = fileVectors[fileType][justName]
				for eachPercept in weights:
					input = inputSum(fileVector, weights, eachPercept)
					error = 0
					if input >= perceptronThreshold and eachPercept != fileType:
                                                error = -1
                                        if input < perceptronThreshold and eachPercept == fileType:
                                                error = 1 
					for eachWord in weights[eachPercept]:
                                                weights[eachPercept][eachWord] += alpha*error*fileVector[eachWord]
		
		alpha *= alphaDecay

	if specMode == False:
		print "Training Complete"
	#print "Resulting Weights"
	#for eachType in weights:
	#	print eachType
	#	for eachWeight in weights[eachType]:
	#		print eachWeight + ", " + str(weights[eachType][eachWeight])
	#	print "\n"
	
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
			else:
				print str(fileTuple) + str(dictResults[fileTuple[0]])

		print "Percent accurate = " + str(totalCorrect / totalResults)
	elif specMode == True:	
		for eachTuple in fileResults:
			print "Perceptron, " + str(eachTuple[0]) + ", " + str(eachTuple[1])
        return fileResults;

def testPerceptrons10(perceptrons, testData, topWords, actualResults):
	fileResults = []
        fileVectors = getTestVectors(testData, topWords)
	totalGuess = 0
        if specMode == False:
                print "Preproc complete"
                print "Beginning perceptron voting"

        for eachFile in fileVectors:
                results = castVotes(perceptrons, fileVectors[eachFile], topWords)
                fileResults.append((path.basename(eachFile), random.choice(results)))
		if results == ["DT", "DR", "L"]:
			totalGuess += 1

	print "totalGuesses = " + str(totalGuess)
        #Calculate our results against actual
        if specMode == False:
                print "Perceptron voting complete"
                print "Calculating number of correct result"

        totalResults = len( testData );
        totalCorrect = 0.0;
        for fileTuple in fileResults:
                if actualResults[fileTuple[0]] == fileTuple[1]:
                        totalCorrect += 1;
		else:
			print str(fileTuple) + str(actualResults[fileTuple[0]])

        if specMode == False:
                print "Percent accurate = " + str(totalCorrect / totalResults)
        elif specMode == True:
                for eachTuple in fileResults:
                        print "Perceptron, " + str(eachTuple[0]) + ", " + str(eachTuple[1])
        return totalCorrect/totalResults;

def castVotes(perceptrons, fileVector, topWords):
	result = []
	for eachType in topWords:
		runningTotal = float(0)
		for eachWord in topWords[eachType]:
			runningTotal += perceptrons[eachType][eachWord[0]]*fileVector[eachWord[0]]
		if runningTotal > perceptronThreshold:
			result += [eachType]
	if result == []:
		result = ["DT", "DR", "L"]
	return result

def usePerceptrons(trainDirs, testDir, trainData, testData):

	if useTenFoldCross == True:
		trainDirTypes = ["DT", "DR", "L"]
        	testPool = createTestPool(trainDirs, trainDirTypes)
        	dividedTests = testPool[0]
        	results = testPool[1]
		averageAccuracy = 0;
		attributeTests = []
            	for i in range(10):
                	attributeTests += dividedTests[i]
            	
		attributes = getAttributeSets10(attributeTests, results)
		if specMode == True:
			perceptStuff = perceptronStrat10(attributeTests, results, attributes)
			perceptrons = perceptStuff[0]
			testPerceptrons(perceptrons, testData, attributes)
		else:
            		for i in range(10):
                		trainingTests = []
                		for j in range(10):
                   			if j != i:
						trainingTests += dividedTests[j]
                		perceptStuff = perceptronStrat10(trainingTests, results, attributes)
                		perceptrons = perceptStuff[0]
                		averageAccuracy += testPerceptrons10(perceptrons, dividedTests[i], attributes, results)
            		averageAccuracy *= .1
            		print "avg = " + str(averageAccuracy)
        else:
		for eachType in trainData:
			random.shuffle(trainData[eachType])
			random.shuffle(trainData[eachType])
            	perceptStuff = perceptronStrat(trainData)
            	perceptrons = perceptStuff[0]
            	topWords = perceptStuff[1]
            	testPerceptrons(perceptrons, testData, topWords)	
