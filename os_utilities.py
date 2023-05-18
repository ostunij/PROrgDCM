import os


def getCurrentWorkingDirectory():
    return os.getcwd()


def getFullDirectoryPath(directoryName):
    fullDirectoryName = os.path.abspath(directoryName)
    return fullDirectoryName


def createDirectoryIfNeeded(directoryName):
    if (os.path.isdir(directoryName)):
        return
    #print("Creating directory" + directoryName)
    os.makedirs(directoryName)


def joinPaths(path1, path2):
    joinedPath = "%s%s%s" % (path1, os.path.sep, path2)
    return joinedPath
