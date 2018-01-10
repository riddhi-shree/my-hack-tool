#!/usr/bin/env python
import os, sys, re, shutil, time


class findMyKeyword():
    lookInDir = ''
    lookForKey = ''
    outDir = ''

    includeExtensions = []
    outUniqueList = set()


    def __init__(self, baseDirectoryAbsPath, searchString, outDirectoryAbsPath, includeExtensions):
        self.lookInDir = baseDirectoryAbsPath
        self.lookForKey = searchString
        self.outDir = outDirectoryAbsPath
        self.includeExtensions = includeExtensions
        self.findNow()


    def createFile(self, path, filename):
        if not os.path.exists(path):
            os.makedirs(path)
        fileObj = open(os.path.join(path,filename), 'w+')
        fileObj.close

        return open(os.path.join(path,filename), 'a')


    def findNow(self):
        outputFileLocationMatch = self.createFile(self.outDir, 'keywordFoundHere'+time.strftime("-%Y%m%d-%H%M%S")+'.txt')
        outputFileLineMatch = self.createFile(self.outDir, 'keywordContainedInLines'+time.strftime("-%Y%m%d-%H%M%S")+'.txt')
        setFileLocationMatch = set()
        setFileLineMatch = set()

        for root, dirs, files in os.walk(self.lookInDir):
            for file in files:
                if os.path.splitext(file)[1] in self.includeExtensions:
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r') as in_file:
                            print('Reading : ' + filepath)
                            for line in in_file:
                                if line.find(self.lookForKey) != -1:
                                    setFileLocationMatch.add(filepath + '\n')
                                    setFileLineMatch.add(line.strip() + '\n')
                                    break
                    except UnicodeDecodeError:
                        print('Error in : ' + filepath)


        outputFileLocationMatch.write('Your keyword "' + self.lookForKey + '" is hiding here:\n\n')
        for item in sorted(setFileLocationMatch):
            outputFileLocationMatch.write(item + '\n')
            #print(item)

        outputFileLineMatch.write('Your keyword "' + self.lookForKey + '" is used here:\n\n')
        for item in sorted(setFileLineMatch):
            outputFileLineMatch.write(item + '\n')
            # print(item)

        outputFileLocationMatch.close()
        outputFileLineMatch.close()
        print('Done!')


#print("--------------" + sys.argv[1])
#findMyKeyword(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
findMyKeyword('D:\\2017\\Work\\Yes\\Docs\\SourceCode\\Phoenix-Web-master-432e0bc352409d44771b480ccc8af5bcc4cef5ec', '@RequestMapping', 'D:\\2018\\python\\code\\OUTPUT', ['.html','.java'])