#!/usr/bin/env python

#from os import listdir
from os import walk
from os import path
import re
import operator
import random
from intelliGrep import *
from naiveBayes import *
from perceptron import *

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
   
    for i in range(len(trainDirTypes)):
	for(root, subFolders, files) in walk(trainDir[i]):
	    for eachFile in files:
		trainData[trainDirTypes[i]] += [trainDir[i]+ "/" + eachFile]
    testData = []
    for(root, subFolders, files) in walk(args.testDir):
	for eachFile in files:
	    testData += [args.testDir + "/" + eachFile]

    if args.stratName == 'intelliGrep':
		intelliGrepBase(testData);
		intelliGrepImproved(testData);
    elif args.stratName == 'naiveBayes':
        #naiveProbOfW  = naiveBayesBase( trainData )
        naiveProbOfW  = naiveBayesImproved( trainData )
        TestNaiveBayes( naiveProbOfW, testData );
    elif args.stratName == 'perceptron':
	usePerceptrons(trainDir, args.testDir, trainData, testData)
