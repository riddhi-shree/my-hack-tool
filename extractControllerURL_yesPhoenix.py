#!/usr/bin/env python
import os, sys, re, shutil


class getControllerLinks():
    directoryPath = ''
    absoluteOutFilename = ''
    absoluteOutFoldername = ''
    searchSubDirectory = ''


    def __init__(self, directoryPath, searchSubDirectory):
        self.directoryPath = directoryPath
        self.getLinks()
        self.searchSubDirectory = searchSubDirectory


    def createFile(self, filename):
        destAbsFolder = os.path.join(self.directoryPath,'OUTPUT')
        if not os.path.exists(destAbsFolder):
            os.makedirs(destAbsFolder)
        self.absoluteOutFilename = os.path.join(destAbsFolder,filename)
        f = open(self.absoluteOutFilename, 'w+')
        f.close()


    def getLinks(self):
        self.createFile('linkWasExtractedFromFile.txt')
        mappingOutfile = open(self.absoluteOutFilename, 'a')

        self.createFile('listOfParametersFoundInURL.txt')
        paramOutfile = open(self.absoluteOutFilename, 'a')

        self.createFile('listOfExtractedLinks.txt')
        outfile = open(self.absoluteOutFilename, 'a')
        self.searchAndCopyFoldersWithName(self.directoryPath, self.searchSubDirectory)

        setOfExtractedLinks = set()
        setOfExtractedParameters = set()
        for root, dirs, files in os.walk(self.absoluteOutFoldername):
            for file in files:
                if file.endswith('.java'):
                    # print(os.path.join(root, file))
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r') as in_file:
                        for line in in_file:
                            if line.find('@RequestMapping') != -1 and line.find('"/') != -1:
                                strippedLine = line.strip()
                                extractedURLString = re.match(r'(.*?")(/.*?)(".*?)', strippedLine, re.I)
                                setOfExtractedLinks.add(extractedURLString.group(2))
                                mappingOutfile.write('Path: \n' + filepath + '\nLink: \n' + extractedURLString.group(2) + '\n\n')

                                extractedParam = re.match(r'.*?(\{.*?\}).*?', extractedURLString.group(2), re.I)
                                if extractedParam:
                                    setOfExtractedParameters.add(extractedParam.group(1))

        outfile.write('List of Extracted Links from ' + self.searchSubDirectory + ' Pages:\n\n')
        for item in sorted(setOfExtractedLinks):
            outfile.write(item + '\n')
            #print(item)

        outfile.write('List of Extracted Parameters from ' + self.searchSubDirectory + ' Pages:\n\n')
        for item in sorted(setOfExtractedParameters):
            paramOutfile.write(item + '\n')
            # print(item)

        outfile.close()
        mappingOutfile.close()
        print('Links have been copied to the following location:\n ' + self.absoluteOutFilename + '\n')


    def searchAndCopyFoldersWithName(self, rootDirectoryAbsolutePath, foldername):
        for root, dirs, files in os.walk(rootDirectoryAbsolutePath):
            for dir in dirs:
                if dir.find('controller') != -1:
                    srcFolder = os.path.join(root, dir)
                    destFolder = os.path.join(self.directoryPath,os.path.join('OUTPUT','CopiedFiles'))
                    self.copyFolder(srcFolder, destFolder)

        self.absoluteOutFoldername = destFolder
        print('Files have been copied to the following location:\n ' + destFolder + '\n')


    def copyFolder(self, srcAbsFolder, destAbsFolder):
        if not os.path.exists(destAbsFolder):
            os.makedirs(destAbsFolder)
        for root, dirs, files in os.walk(srcAbsFolder):
            for file in files:
                shutil.copy(os.path.join(root, file), destAbsFolder)


obj = getControllerLinks('D:\\2017\\Work\\Yes\\Docs\\SourceCode\\Phoenix-Web-master-432e0bc352409d44771b480ccc8af5bcc4cef5ec\\src', 'controller')
