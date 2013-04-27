from fileParser import *
import math

probOfC = { "DT": [], "DR": [], "L": [] }

def naiveBayesBase( trainData ):
    '''
    Base training for naive bayes. Returns rating of top words for each doc class
    '''
    probOfW = {"DT": {}, "DR": {}, "L": {}}
    topWords = { "DT": [], "DR": [], "L": [] }
    uniqueWords = [];
    uniqueWordCt = 0;
    totalDocs = 0;
    classDocs = { "DT": 0, "DR": 0, "L": 0 }

    for fileType in trainData:
        totalWords = 0;
        dataWords = {};
        for fileName in trainData[fileType]:
            totalDocs += 1;
            classDocs[fileType] += 1;
            cleanData = cleanFile(fileName)
            fileWords = cleanData.split(" ");
            found = []
            for word in fileWords: #[word for word in fileWords if word not in commonWords]:
                if word not in uniqueWords:
                    uniqueWords += [word];
                    uniqueWordCt += 1;
                if word in dataWords and word not in found:
                    found += [word]
                    dataWords[word] += 1
                elif word not in found:
                    if (ignoreSelectWords == True and word not in selectWords) or (ignoreSelectWords == False):
                        found += [word]
                        dataWords[word] = 1

        topWords[fileType] = sorted( dataWords.items(), key=operator.itemgetter(1) )[-20:]
        
    totalDocs = float( totalDocs );
    for fileType in classDocs:
        probOfC[fileType] = classDocs[fileType] / totalDocs
    
    for fileType in topWords:
        '''fileType = DT, DR, L'''
        denom = len( topWords[fileType] ) + uniqueWordCt;
        for wordTuple in topWords[fileType]:
            ''''("butterfly", 15)'''
            numerator = float(wordTuple[1]) + 1; #Amount of documents with word
            probOfW[fileType][wordTuple[0]] = ( numerator / denom  );
            
    return probOfW

def testNaiveImproved( probOfW, testData ):
    '''
    Improved naive bayes based on more contribution from amount of words, as well as presence
    '''
    fileResults = []
    allFileLen = float( len( testData ) );
    fileLens = []
    
    for fileName in testData:
        cleanData = cleanFile(fileName )
        fileWords = cleanData.split(" ")
        fileLens.append( len(fileWords) );
        
    for fileName in testData:
        cleanData = cleanFile(fileName )
        fileWords = cleanData.split(" ")
        fileWordLen = len(fileWords);
        totalN = float(fileWordLen); #int / float = float DUH!
        
        result = {
            "L": 0,
            "DR": 0,
            "DT": 0
        }
        
        for fileType in probOfW:
            result[fileType] += math.log( probOfC[fileType] );
            for word in probOfW[fileType]:
                nik = fileWords.count( word )#amount of times word in fileWords
                inner = probOfW[fileType][word];
		if inner == 1:
                    result[fileType] += 0;
                else:
                    result[fileType] += ( nik * math.log( inner , 10) ); #log(xy) == log(x) + log(y)
                
            if result[fileType] == 0:
                #print "Just had an underflow problem in testNaiveBayes!"
                
        #Using min since values are reversed
        maxAttr = min( result.items(), key=operator.itemgetter(1) )[0]
        fileResults += [ ( fileName, maxAttr ) ]

    #Calculate our results against actual
    actualResults = file(testResultsFile).read();
    actualResults = actualResults.split('\n');
    dictResults = {};
    for fileName in actualResults:
        if ',' in fileName:
            lineList = fileName.split(',');
            dictResults[ lineList[0] ] =  lineList[1];

    totalResults = len( testData );
    totalCorrect = 0.0;
    for fileTuple in fileResults:
        print "naiveBayes, " + fileTuple[0] + ", ",fileTuple[1];
        if dictResults[path.basename(fileTuple[0])] == fileTuple[1]:
            totalCorrect += 1

    #print "Naive Bayes correctness:", totalCorrect / totalResults
    return fileResults

def testNaiveBase( probOfW, testData ):
    '''
    Base Naive Bayes with boolean bag option
    '''
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
        #Using min since values are reversed
        maxAttr = min( result.items(), key=operator.itemgetter(1) )[0]
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

    #print "Naive Bayes correctness:", totalCorrect / totalResults
    return fileResults
