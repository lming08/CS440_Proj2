#!/usr/bin/env python

#from os import listdir
from os import walk
from os import path
import re
import operator
import random


selectWords = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h','i', 'j', 'k', 'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', '',
    'be', 'to', 'in', 'at', 'no', 'do', 'go','he','we', 'it', 'or', 'my', 'of', 'on', 'is', 'as', 'by', 'my',
    'the', 'she', 'him', 'her', 'you', 'and', 'new', 'was', 'how', 'why', 'all', 'for', 'any', 'not',
    'what', 'that','have', 'from', 'this', 'most', 'then', 'also',
    'qwerty'
]

testResultsFile = "data/test-results.txt"
ignoreSelectWords = False
useBooleanBag = True
useTenFoldCross = False
useExtraPreProc = True
ensureEqualRepresentation = True

initialAlpha = .1
alphaDecay = .99
initialWeight = 1.0
perceptronThreshold = 1.01

def cleanFile(filename):
    '''
    Gets rid of anything that is not an alphabetic character or a
    single space
    '''
    contents = file(filename).read()
    contents = re.sub(r'[^a-zA-Z]', ' ', contents)
    if useExtraPreProc == True:
	contents = re.sub(r'[ii+]', ' ', contents)
    	contents = re.sub(r'[ll+]', ' ', contents)
    contents = contents.lower()
    contents = re.sub("\s+", " ", contents)

    return contents


def grep(filecontents, strToFind):
    if re.search(strToFind, filecontents):
        return True

def percentCorrect( total, fileResults ):
    #Calculate our results against actual
    actualResults = file(testResultsFile).read()
    actualResults = actualResults.split('\n');
    dictResults = {}
    for fileName in actualResults:
        if ',' in fileName:
            lineList = fileName.split(',');
            dictResults[lineList[0]] =  lineList[1]

    #for f in dictResults:
    #   print f, dictResults[f]

    totalCorrect = 0.0
    for fileTuple in fileResults:
        if dictResults[fileTuple[0]] == fileTuple[1]:
            totalCorrect += 1;

    return totalCorrect / total;

def intelliGrepStrat( files ):
    drNum = 0
    dtNum = 0
    lNum = 0
    drFileNum = 0
    dtFileNum = 0
    lFileNum = 0
    trainStrings = {
        "DR": "deed of reconveyance",
        "DT": "deed of trust",
        "L": "lien"
    }
    trainDataCount = {
        "DR": 0,
        "DT": 0,
        "L": 0
    }
    trainActualCount = {
        "DR": 0,
        "DT": 0,
        "L": 0
    }
    fileResults = [];
    for fileName in files:
        cleanData = cleanFile(fileName )
        trainStringCount = {
            "DR": 0,
            "DT": 0,
            "L": 0
        }
        for key,string in trainStrings.items():
            trainStringCount[key] = len( re.findall(string, cleanData) )
            #TODO: make more random than max (Max = first item with max value )
            maxVal = max( trainStringCount.items(), key=operator.itemgetter(1) )[0]
	
        fileResults += [ (path.basename(fileName), maxVal) ]

    #total = reduce( lambda p,n: p+n, [len(trainData[x]) for x in trainData] )
    total = len(files)
    correctNess = percentCorrect( total, fileResults );
    print "IntelliGrep Correctness: " , correctNess;
    return correctNess;
	
def getAttributeSets(trainData):
	topWords = {
        "DR": [],
        "DT": [],
        "L": []
    }

	for fileType in trainData:
                totalWords = 0;
                dataWords = {};
                for fileName in trainData[fileType]:
                        cleanData = cleanFile(fileName)
                        fileWords = cleanData.split(" ");
                        found = []
                        for word in fileWords: #[word for word in fileWords if word not in commonWords]:
                                if word in dataWords and word not in found:
                                        found += [word]
                                        dataWords[word] += 1
                                elif word not in found:
					if (ignoreSelectWords == True and word not in selectWords) or (ignoreSelectWords == False):
                                        	found += [word]
                                        	dataWords[word] = 1

                topWords[fileType] = sorted( dataWords.items(), key=operator.itemgetter(1) )[-20:];

	return topWords
	
def naiveBayesStrat( trainData ):
	probOfW = {"DR": {}, "DT": {}, "L": {}}
    	topWords = getAttributeSets(trainData)

	for fileType in topWords:
		for wordTuple in topWords[fileType]:
				numerator = float(wordTuple[1])
				denom = len( trainData[fileType] ) or 1.0
				probOfW[fileType][wordTuple[0]] = ( numerator / denom  ) or ( 1.0 / denom )
		#print probOfW[fileType]	
			
	return probOfW;	
	
def TestNaiveBayes( probOfW, testData ):
	fileResults = [];
	for fileName in testData:
		cleanData = cleanFile(fileName )
		fileWords = cleanData.split(" ");
		if useBooleanBag == False:
			totalN = float(len(fileWords))
		result = {
			"DR": 1.0,
		    "DT": 1.0,
		    "L": 1.0
		}
		for fileType in probOfW:
			for word in probOfW[fileType]:
				if useBooleanBag == True:
					if word in fileWords:
						result[fileType] *= probOfW[fileType][word]
					else:
						result[fileType] *= (1 - probOfW[fileType][word])
				else:
					multiplier = fileWords.count(word)/totalN or (1/totalN)
					result[fileType] *= multiplier*probOfW[fileType][word]
					if result[fileType] == 0:
						print "just had an underflow problem in testNaiveBayes!"
					
					
		maxAttr = max( result.items(), key=operator.itemgetter(1) )[0]
		fileResults += [ ( fileName, maxAttr ) ]
		
	#for f in fileResults:
		#print fileResults.index(f), f
	
	#Calculate our results against actual
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
		if dictResults[path.basename(fileTuple[0])] == fileTuple[1]:
			totalCorrect += 1;
			
	print totalCorrect / totalResults;
	return fileResults;

def cleanClass(trainingData, fileType):
	contents = " "
	for eachFile in trainingData[fileType]:
		contents += " " + file(eachFile).read()
    	contents = re.sub(r'[^a-zA-Z]', ' ', contents)
	if useExtraPreProc == True:
		contents = re.sub(r'[ii+]', ' ', contents)
		contents = re.sub(r'[ll+]', ' ', contents)
    	contents = contents.lower()
    	contents = re.sub("\s+", " ", contents)
	#print "test"
	#print contents
	return contents

def getNcommonishWords(someString, N):
	dataWords = {};
	tokens = someString.split(" ")
        for word in tokens:
        	if word in dataWords:
                	dataWords[word] += 1
        	elif (ignoreSelectWords == True and word not in selectWords) or ignoreSelectWords == False:
       			dataWords[word] = 1

       	commonishWords = sorted(dataWords.items(), key=operator.itemgetter(1))[-N:];
	#print "test"
	#for word in commonishWords:
	#	print (word)# + ", " + str(dataWords[word]))
	#print commonishWords
	return commonishWords

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
	print "Starting Preproc"
	if useBooleanBag == False:
		topWordsDT = getNcommonishWords(cleanClass(trainData, "DT"), 20)
		topWordsDR = getNcommonishWords(cleanClass(trainData, "DR"), 20)
		topWordsL = getNcommonishWords(cleanClass(trainData, "L"), 20)
		topWords = {"DT":topWordsDT, "DR":topWordsDR, "L":topWordsL}
	else:
		topWords = getAttributeSets(trainData)

	fileVectors = getFileVectors(trainData, topWords)
	print "Preproc complete"
	
	weights = {"DR":{}, "DT":{}, "L":{}}
	alpha = initialAlpha
	bias = 0
	for eachType in topWords:
		for eachWord in topWords[eachType]:
			weights[eachType][eachWord[0]] = initialWeight

	print "Beginning training"
	for i in range(101):
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
	print "Training Complete"
	#print "Resulting Weights"
	#for eachType in weights:
		#print eachType
		#for eachWeight in weights[eachType]:
			#print eachWeight + ", " + str(weights[eachType][eachWeight])
		#print "\n"
	
	return (weights, topWords)

def testPerceptrons(perceptrons, testData, topWords):
	print "Preprocessing test data"
	fileResults = [];
	fileVectors = getTestVectors(testData, topWords)
	print "Preproc complete"

	print "Beginning perceptron voting"
	for eachFile in fileVectors:
		results = castVotes(perceptrons, fileVectors[eachFile], topWords)
		fileResults.append((path.basename(eachFile), random.choice(results)))
        #for f in fileResults:
                #print fileResults.index(f), f

        #Calculate our results against actual
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

        print "Percent accurate = " + str(totalCorrect / totalResults)
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
	
def createTestPool(trainDir, testDir, trainDirTypes):
	testFiles = []
	results = {}

	testFileStuff = file(testResultsFile).read()
        testFileStuff = testFileStuff.split('\n');
        results = {}
	dividedTests = {}
	for i in range(10):
		dividedTests[i] = []
	currentGroupIndexes = [0, 0, 0]
        for eachLine in testFileStuff:
                if ',' in eachLine:
                        splitCurrentLine = eachLine.split(',');
			testFiles += [testDir + "/" + splitCurrentLine[0]]
                        results[splitCurrentLine[0]] = splitCurrentLine[1]
			
			if ensureEqualRepresentation == True:
				myGroup = trainDirTypes.index(splitCurrentLine[1])
				myGroupIndex = currentGroupIndexes[myGroup] % 10
				dividedTests[myGroupIndex] += [testDir + "/" + splitCurrentLine[0]]
				currentGroupIndexes[myGroup] += 1
		

	for i in range(len(trainDirTypes)):
        	for(root, subFolders, files) in walk(trainDir[i]):
            		for eachFile in files:
				testFiles += [trainDir[i] + "/" + eachFile]
				results.update({eachFile:trainDirTypes[i]})
				
				if ensureEqualRepresentation == True:
                                	myGroup = i
                                	myGroupIndex = currentGroupIndexes[myGroup] % 10
                                	dividedTests[myGroupIndex] += [trainDir[i] + "/" + eachFile]
                                	currentGroupIndexes[myGroup] += 1

	#for eachGroup in dividedTests:
	#	currentGroupIndexes = [0, 0, 0]
	#	print eachGroup
	#	for eachTestFile in dividedTests[eachGroup]:
	#		currentGroupIndexes[trainDirTypes.index(results[path.basename(eachTestFile)])] += 1
	#		print eachTestFile + ", " + results[path.basename(eachTestFile)]
	#	print currentGroupIndexes
	#for eachFile in results:
	#	print eachFile + ", " + results[eachFile]
	return	[testFiles, results]

def subDivideTests(testFiles, testResults):
	dividedTests = {}
	numInGroup = len(testFileResults)/10

	if ensureEqualRepresentation == True:
		random.shuffle(testResults)
		fileTypes = ["DT", "DR", "L"]
					
				
	for i in range(10):
		results[i] = random.sample(testFiles, numInGroup)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('stratName' , choices=('intelliGrep', 'naiveBayes' , 'perceptron') , default='intelliGrep' , help="Select the desired strategy: 'intelliGrep' , 'naiveBayes' , 'perceptron'")
    parser.add_argument('dtDir'     , help="Select the desired dtDir to train on")
    parser.add_argument('drDir'     , help="Select the desired drDir to train on")
    parser.add_argument('lDir'      , help="Select the desired lDir to train on")
    parser.add_argument('testDir'   , help="Select the desired testDir to test on")
    args = parser.parse_args()

    trainDirTypes = ["DT", "DR", "L"]
    trainDir = [args.dtDir, args.drDir, args.lDir]

    trainData = {
        "DT": [],
        "DR": [],
        "L": []
    }
    if useTenFoldCross == True:
	createTestPool(trainDir, args.testDir, trainDirTypes)
    else:
    	for i in range(len(trainDirTypes)):
            for(root, subFolders, files) in walk(trainDir[i]):
	    	for eachFile in files:
            	    trainData[trainDirTypes[i]] += [trainDir[i]+ "/" + eachFile]
  	testData = []
    	for(root, subFolders, files) in walk(args.testDir):
            for eachFile in files:
               	testData += [args.testDir + "/" + eachFile]

    intelliGrepStrat(testData)
    #naiveProbOfW  = naiveBayesStrat( trainData )
    #TestNaiveBayes( naiveProbOfW, testData );
    #perceptStuff = perceptronStrat(trainData)
    #perceptrons = perceptStuff[0]
    #topWords = perceptStuff[1]
    #testPerceptrons(perceptrons, testData, topWords)
    
	
    
    
