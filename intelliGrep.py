from fileParser import *

def cleanFileImproved(filename):
    '''
    Gets rid of anything that is not an alphabetic character or a
    single space
    '''
    contents = file(filename).read()
    contents = re.sub(r'[^a-zA-Z]', ' ', contents)
    if useExtraPreProc == True:
    	contents = re.sub(r'i{2,}', ' ', contents)
    	contents = re.sub(r'l{3,}', ' ', contents)
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

def intelliGrepBase( files ):
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


		maxTup = max( trainStringCount.items(), key=operator.itemgetter(1) );
		ansPossibilities = [x for x in trainStringCount if trainStringCount[x] == maxTup[1]];
		maxVal = random.choice( ansPossibilities );
		fileResults += [ (path.basename(fileName), maxVal) ]

	total = len(files)
	for (fName, result)  in fileResults:
		print "IntelliGrepBase, " + fName + ", " + result
	correctNess = percentCorrect( total, fileResults );
	print "IntelliGrep Base Correctness: " , correctNess;
	return correctNess;


def intelliGrepImproved( files ):
	drNum = 0
	dtNum = 0
	lNum = 0
	drFileNum = 0
	dtFileNum = 0
	lFileNum = 0
	trainStrings = {
		"DR": "DEED OF RECONVEYANCE",
		"DT": "DEED OF TRUST",
		"L": "LIEN"
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
		cleanData = cleanFileImproved(fileName )
		trainStringCount = {
			"DR": 0,
			"DT": 0,
			"L": 0
		}
		for key,string in trainStrings.items():
			trainStringCount[key] = len( re.findall(string, cleanData) )

		maxTup = max( trainStringCount.items(), key=operator.itemgetter(1) );
		ansPossibilities = [x for x in trainStringCount if trainStringCount[x] == maxTup[1]];
		maxVal = random.choice( ansPossibilities );
		fileResults += [ (path.basename(fileName), maxVal) ]

	total = len(files)
	for (fName, result)  in fileResults:
		print "IntelliGrepImproved, " + fName + ", " + result
	correctNess = percentCorrect( total, fileResults );
	print "IntelliGrep Improved Correctness: " , correctNess;
	return correctNess;
