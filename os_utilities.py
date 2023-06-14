import datetime
import os
import filedate


def getCurrentWorkingDirectory():
    return os.getcwd()


def getFullDirectoryPath(directoryName):
    fullDirectoryName = os.path.abspath(directoryName)
    return fullDirectoryName


def createDirectoryIfNeeded(directoryName):
    if (os.path.isdir(directoryName)):
        return
    # print("Creating directory" + directoryName)
    os.makedirs(directoryName)


def joinPaths(path1, path2):
    joinedPath = "%s%s%s" % (path1, os.path.sep, path2)
    return joinedPath


def setFileTime(filename, datetimeString):
    a_file = filedate.File(filename)

    a_file.set(
        created=datetimeString,
        modified=datetimeString,
        accessed=datetimeString
    )


def setDirectoryTimeIfNeeded(directoryName, seriesdatetime, organizerdatetime):
    a_file = filedate.File(directoryName)
    currentdatetime = a_file.get()["created"]
    print("Comparing dates current: %s to series: %s to organizer:%s" % (currentdatetime, seriesdatetime, organizerdatetime))
    if (currentdatetime > organizerdatetime):
        #print("1 setting %s to  %s" % (directoryName, seriesdatetime))
        a_file.set(
            created=seriesdatetime,
            modified=seriesdatetime,
            accessed=seriesdatetime
        )
    elif (currentdatetime < seriesdatetime):
        print("2 setting %s to  %s" % (directoryName, seriesdatetime))
        a_file.set(
            created=seriesdatetime,
            modified=seriesdatetime,
            accessed=seriesdatetime
        )


def setParentDirectoryTimeIfNeeded(directoryName, seriesdatetime, organizerdatetime):
    parentDirectory = os.path.dirname(directoryName)
    setDirectoryTimeIfNeeded(
        parentDirectory, seriesdatetime, organizerdatetime)


def getDateTimeFromTokens(year, month, day, hour, minute, second):
    year = int(year)
    month = int(month)
    day = int(day)
    hour = int(hour)
    minute = int(minute)
    second = int(second)
    millsecond = 0
    datetimeString = datetime.datetime(
        year, month, day, hour, minute, second, millsecond)
    return datetimeString
