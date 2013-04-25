#!/usr/bin/env python

#from os import listdir
from os import walk
from os import path
import re
import operator
import random


selectWords = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h','i', 'j', 'k', 'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', '',
    'be', 'to', 'in', 'at', 'no', 'do', 'go','he','we', 'it', 'or', 'my',' on', 'is', 'as', 'by', 'my',
    'the', 'she', 'him', 'her', 'you', 'and', 'new', 'was', 'how', 'why', 'all', 'for', 'any', 'not',
    'what', 'that','have', 'from', 'this', 'most', 'then', 'also',
    'qwerty'
]

testResultsFile = "data/test-results.txt"
ignoreSelectWords = True
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
        contents = re.sub(r'i{2,}', ' ', contents)
        contents = re.sub(r'l{3,}', ' ', contents)
    contents = contents.lower()
    contents = re.sub("\s+", " ", contents)
    return contents


def getAttributeSets(trainData):
    topWords = {
        "DT": [],
        "DR": [],
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


def cleanClass(trainingData, fileType):
    contents = " "
    for eachFile in trainingData[fileType]:
        contents += " " + file(eachFile).read()
        contents = re.sub(r'[^a-zA-Z]', ' ', contents)
    if useExtraPreProc == True:
        contents = re.sub(r'i{2,}', ' ', contents)
        contents = re.sub(r'i{2,}', ' ', contents)
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
    #   print (word)# + ", " + str(dataWords[word]))
    #print commonishWords
    return commonishWords


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

    if ensureEqualRepresentation == False:
        numInGroup = len(testFiles)/10
        for i in range(10):
            dividedTests[i] = random.sample(testFiles, numInGroup)
            for eachValue in dividedTests[i]:
                testFiles.remove(eachValue)
        for eachLeftOver in testFiles:
            dividedTests[random.randint(0, 9)].append(eachLeftOver)


    for i in range(10):
        random.shuffle(dividedTests[i])

    for eachGroup in dividedTests:
        currentGroupIndexes = [0, 0, 0]
        print eachGroup
        for eachTestFile in dividedTests[eachGroup]:
            currentGroupIndexes[trainDirTypes.index(results[path.basename(eachTestFile)])] += 1
            print eachTestFile + ", " + results[path.basename(eachTestFile)]
        print currentGroupIndexes
    #for eachFile in results:
    #   print eachFile + ", " + results[eachFile]
    return  [testFiles, results]

def subDivideTests(testFiles, testResults):
    dividedTests = {}
    numInGroup = len(testFileResults)/10

    if ensureEqualRepresentation == True:
        random.shuffle(testResults)
        fileTypes = ["DT", "DR", "L"]


    for i in range(10):
        results[i] = random.sample(testFiles, numInGroup)


