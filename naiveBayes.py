from fileParser import *

def naiveBayesStrat( trainData ):
    probOfW = {"DR": {}, "DT": {}, "L": {}}
    topWords = getAttributeSets(trainData)

    for fileType in topWords:
        for wordTuple in topWords[fileType]:
                numerator = float(wordTuple[1])
                denom = len( trainData[fileType] ) or 1.0
                probOfW[fileType][wordTuple[0]] = ( numerator / denom  ) or ( 1.0 / denom )
        #print probOfW[fileType]

    return probOfW

def TestNaiveBayes( probOfW, testData ):
    fileResults = []
    for fileName in testData:
        cleanData = cleanFile(fileName )
        fileWords = cleanData.split(" ")
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
                        print "Just had an underflow problem in testNaiveBayes!"


        maxAttr = max( result.items(), key=operator.itemgetter(1) )[0]
        fileResults += [ ( fileName, maxAttr ) ]

    #for f in fileResults:
        #print fileResults.index(f), f

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
        if dictResults[path.basename(fileTuple[0])] == fileTuple[1]:
            totalCorrect += 1

    print "Naive Bayes correctness:", totalCorrect / totalResults
    return fileResults
