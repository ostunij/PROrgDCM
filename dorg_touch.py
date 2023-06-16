import os
import glob
import dorg_utilities
import os_utilities
import pydicom


class dicomOrganizerTouch:
    def __init__(self, studyList, currentDateTimeStamp):
        self.studyList = studyList
        self.currentDateTimeStamp = currentDateTimeStamp

    def setTimeStamps(self):
        for studyItem in self.studyList:
            #print("DOT: -----> Checking study: %s" % (studyItem))
            seriesDirectoryList = self.findSeriesDirectories(studyItem)
            #print("\tDOT:  Checking series: %s" % (seriesDirectoryList))
            for seriesDirectory in seriesDirectoryList:
                seriesDCMFileList = self.getSeriesDCMFilesList(seriesDirectory)
                if (len(seriesDCMFileList) > 0):
                    seriesDateTime = self.getSeriesDateTime(
                        seriesDCMFileList[0])
                    self.processSeriesDateTime(
                        seriesDirectory, seriesDCMFileList, seriesDateTime)

    def findSeriesDirectories(self, studyItem):
        cwd = os.getcwd()
        os.chdir(studyItem)
        seriesItems = glob.glob("*/Readme_Series.txt")
        seriesDirectoryList = []
        for seriesItem in seriesItems:
            seriesDirectoryList.append(
                os.path.dirname(os.path.abspath(seriesItem)))
        os.chdir(cwd)
        return seriesDirectoryList

    def getSeriesDCMFilesList(self, series):
        searchString = "%s/*dcm" % (series)
        seriesDCMFiles = glob.glob(searchString)
        if (len(seriesDCMFiles) > 0):
            seriesDCMFiles.sort()
        return seriesDCMFiles

    def getSeriesDateTime(self, dicomFile):
        ds = pydicom.dcmread(dicomFile, stop_before_pixels=True)
        (year, month, day, hour, minute,
         second) = dorg_utilities.getDateTimeString(ds)
        datetimeString = os_utilities.getDateTimeFromTokens(
            year, month, day, hour, minute, second)
        return datetimeString

    def processSeriesDateTime(self, series, seriesDCMFileList, dateString):
        for seriesItem in seriesDCMFileList:
            os_utilities.setFileTime(seriesItem, dateString)
        os_utilities.setDirectoryTimeIfNeeded(series, dateString, self.currentDateTimeStamp)
        parentDirectory = os.path.dirname(series)
        os_utilities.setDirectoryTimeIfNeeded(parentDirectory, dateString, self.currentDateTimeStamp)
        parentDirectory = os.path.dirname(parentDirectory)
        os_utilities.setDirectoryTimeIfNeeded(parentDirectory, dateString, self.currentDateTimeStamp)
