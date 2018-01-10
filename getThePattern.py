#!/usr/bin/env python
import os, sys, re, shutil, time


class GetThePattern():
    lookInFiles = set()
    lookForKey = ''
    groupNum = 0

    outDir = ''
    outResultSet = set()


    def __init__(self, baseFileAbsPath, regularExpression, extractGroupNumber, outDirectoryAbsPath):
        if os.path.exists(baseFileAbsPath):
            with open(baseFileAbsPath, 'r') as in_file:
                for line in in_file:
                    line = line.strip()
                    if line and os.path.exists(line):
                        self.lookInFiles.add(line)

        self.lookForKey = regularExpression
        self.groupNum = extractGroupNumber
        self.outDir = outDirectoryAbsPath
        self.findNow()


    def createFile(self, path, filename):
        if not os.path.exists(path):
            os.makedirs(path)
        fileObj = open(os.path.join(path, filename), 'w+')
        fileObj.close

        return open(os.path.join(path, filename), 'a')


    def findNow(self):
        outputRegExMatch = self.createFile(self.outDir, 'outputOfYourRegExIsHere'+time.strftime("-%Y%m%d-%H%M%S")+'.txt')

        for filepath in self.lookInFiles:
            try:
                with open(filepath, 'r') as in_file:
                    print('Reading : ' + filepath)
                    for line in in_file:
                        matchedString = re.match(self.lookForKey, line, re.I)
                        if matchedString:
                            self.outResultSet.add(matchedString.group(self.groupNum).strip())
            except:
                print('Error in : ' + filepath)

        outputRegExMatch.write('Results for your regex "' + self.lookForKey + '":\n\n')
        for item in sorted(self.outResultSet):
            outputRegExMatch.write(item + '\n')


# print("--------------" + sys.argv[1])
# GetThePattern(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
obj = GetThePattern('D:\\2018\\python\\code\\OUTPUT\\keywordFoundHere-20180103-165616.txt', '(.*?@RequestMapping.*?")(.*?)(".*?)', 2, 'D:\\2018\\python\\code\\OUTPUT')