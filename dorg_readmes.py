import pydicom
import glob
import os
import dorg_utilities

class readmeCreator():
    def _init__(self):
        pass

    def createSeriesReadmeFiles(self, seriesDirectoryList):
        for seriesDir in seriesDirectoryList:
            self.createSeriesReadmeFile(seriesDir)

    def createSeriesReadmeFile(self, seriesDir):
        readmefile = "%s/Readme_Series.txt" % (seriesDir)
        searchString = "%s/*.dcm" % (seriesDir)
        sampleFiles = glob.glob(seriesDir+"/*.dcm")
        sampleFiles.sort()
        dicomFile = sampleFiles[0]
        if (len(sampleFiles) == 0):
            return
        f = open(readmefile, 'w')
        ds = pydicom.dcmread(dicomFile, stop_before_pixels=True)
        for d in ds:
            if (d.VR != "SQ") and (not d.is_private) and (not d.is_empty):
                line = "%s: %s\n" % (d.name, d.value)
                f.write(line)
        f.close()

    def createStudyReadmeFiles(self, studyDirectoryList, dos):
        for studyDir in studyDirectoryList:
            self.createStudyReadmeFile(studyDir, dos)

    def createStudyReadmeFile(self, studyDir, dos):
        readmefile = "%s/Readme_Study.txt" % (studyDir)
        seriesDirsFound = []

        searchString = "%s/*/Readme_Series.txt" % (studyDir)
        sList = glob.glob(searchString)
        if (len(sList) > 0):
            seriesDirsFound.extend(sList)

        searchString = "%s/*/*/Readme_Series.txt" % (studyDir)
        sList = glob.glob(searchString)
        if (len(sList) > 0):
            seriesDirsFound.extend(sList)

        f = open(readmefile, 'w')

        studyInformationWritten = False
        for seriesDirFound in seriesDirsFound:
            dirname = os.path.dirname(seriesDirFound)
            sampleFiles = glob.glob(dirname+"/*.dcm")
            sampleFiles.sort()
            count = len(sampleFiles)
            dicomFile = sampleFiles[0]
            ds = pydicom.dcmread(dicomFile, stop_before_pixels=True)
            if (len(sampleFiles) == 0):
                continue
            if (not studyInformationWritten):
                subjectName = dorg_utilities.getPatientName(ds)
                line = "Subject Name: %s\n" % (subjectName)
                f.write(line)
                subjectID = dorg_utilities.getPatientID(ds)
                line = "Subject ID: %s\n" % (subjectID)
                f.write(line)
                studyDate = dorg_utilities.getStudyDate(ds)
                line = "Study Date: %s\n" % (studyDate)
                f.write(line)
                studyID = dorg_utilities.getStudyID(ds)
                line = "Study ID: %s\n" % (studyID)
                f.write(line)
                accessionNumber = dorg_utilities.getAccessionNumber(ds)
                line = "Accession Number: %s\n" % (accessionNumber)
                f.write(line)
                stationName = dorg_utilities.getStationName(ds)
                line = "Station Name: %s\n" % (stationName)
                f.write(line)
                line = "Series Information\n"
                f.write(line)
                studyInformationWritten = True

            seriesDescription = dorg_utilities.getSeriesDescription(ds)
            seriesNumber = dorg_utilities.getSeriesNumber(ds)
            seriesType = dorg_utilities.getSOPprefix(ds, dos)

            line = "  Series Description: %18s,  Series Type: %s,  Series Number: %s,  Number Images: %s\n" % (
                seriesDescription, seriesType, seriesNumber, len(sampleFiles))
            f.write(line)
        f.close()
