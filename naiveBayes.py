from fileParser import *

def naiveBayesBase( trainData ):
    probOfW = {"DT": {}, "DR": {}, "L": {}}
    topWords = getAttributeSets(trainData)

    for fileType in topWords:
        for wordTuple in topWords[fileType]:
            numerator = float(wordTuple[1])
            denom = len( trainData[fileType] ) or 1.0
            probOfW[fileType][wordTuple[0]] = ( numerator / denom  ) or ( 1.0 / denom )
        #print probOfW[fileType]

    return probOfW

def naiveBayesImproved( trainData ):
    probOfW = {"DT": {}, "DR": {}, "L": {}}
    topWords = getAttributeSets(trainData)

    for fileType in topWords:
        for wordTuple in topWords[fileType]:
            numerator = float(wordTuple[1])
            denom = len( trainData[fileType] ) or 1.0
            probOfW[fileType][wordTuple[0]] = ( numerator / denom  ) or ( 1.0 / denom )
        #print probOfW[fileType]

    return probOfW

# No where close to done
#def trainMultinomialBayes( trainData ):
    #topWords = getAttributeSets(trainData)
    #N = 0
    #for type in trainData:
        #N += len(trainData[type])
    #print N

def TestNaiveBayes( probOfW, testData ):
    fileResults = []
    for fileName in testData:
        cleanData = cleanFile(fileName )
        fileWords = cleanData.split(" ")
        if useBooleanBag == False:
            totalN = float(len(fileWords))

        result = {
            "DT": 1.0,
            "DR": 1.0,
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
                        print "Just had an underflow problem in testNaiveBayes!"


        maxAttr = max( result.items(), key=operator.itemgetter(1) )[0]
        fileResults += [ ( fileName, maxAttr ) ]

    #Calculate our results against actual
    actualResults = file(testResultsFile).read()
    actualResults = actualResults.split('\n')
    dictResults = {}
    for fileName in actualResults:
        if ',' in fileName:
            lineList = fileName.split(',')
            dictResults[ lineList[0] ] =  lineList[1]

    totalResults = len( testData )
    totalCorrect = 0.0
    for fileTuple in fileResults:
        print "naiveBayes, " + fileTuple[0] + ", ",fileTuple[1]
        if dictResults[path.basename(fileTuple[0])] == fileTuple[1]:
            totalCorrect += 1

    print "Naive Bayes correctness:", totalCorrect / totalResults
    return fileResults
