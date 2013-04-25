from fileParser import *

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
