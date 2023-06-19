import glob
import os
import dorg_utilities


class readmeCreator():
    def _init__(self):
        pass

    def createSeriesReadmeFiles(self, seriesDirectoryList):
        for seriesDir in seriesDirectoryList:
            try:
                self.createSeriesReadmeFile(seriesDir)
            except:
                pass

    def createSeriesReadmeFile(self, seriesDir):
        readmefile = "%s/Readme-Series.txt" % (seriesDir)
        searchString = "%s/*.dcm" % (seriesDir)
        sampleFiles = glob.glob(seriesDir+"/*.dcm")
        sampleFiles.sort()
        dicomFile = sampleFiles[0]
        if (len(sampleFiles) == 0):
            return
        f = open(readmefile, 'w')
        ds = dorg_utilities.getDataSetFromFile(dicomFile)
        if (ds is not None):
            for d in ds:
                if (d.VR != "SQ") and (not d.is_private) and (not d.is_empty):
                    line = "%s: %s\n" % (d.name, d.value)
                    f.write(line)
        f.close()

    def createStudyReadmeFiles(self, studyDirectoryList):
        for studyDir in studyDirectoryList:
            self.createStudyReadmeFile(studyDir)

    
    def createStudyReadmeFile(self, studyDir):
        readmefile = "%s/Readme-Study.txt" % (studyDir)
        seriesDirsFound = []

        searchString = "%s/*/Readme-Series.txt" % (studyDir)
        sList = glob.glob(searchString)
        if (len(sList) > 0):
            seriesDirsFound.extend(sList)
        f = open(readmefile, 'w')

        studyInformationWritten = False
        for seriesDirFound in seriesDirsFound:
            currentSeriesDir = os.path.dirname(seriesDirFound)
            currentSeriesDir = os.path.basename(currentSeriesDir)
            if (os.path.basename(currentSeriesDir).startswith("mr_")):
                dirname = os.path.dirname(seriesDirFound)
                sampleFiles = glob.glob(dirname+"/*.dcm")
                if (len(sampleFiles) == 0):
                    continue
                sampleFiles.sort()
                dicomFile = sampleFiles[0]
                ds = dorg_utilities.getDataSetFromFile(dicomFile)
                if (ds is None):
                    continue
    
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
                line = "MR Station Name: %s\n" % (stationName)
                f.write(line)
                line = "Series Information\n"
                f.write(line)
                break

        for seriesDirFound in seriesDirsFound:
            dirname = os.path.dirname(seriesDirFound)
            sampleFiles = glob.glob(dirname+"/*.dcm")
            sampleFiles.sort()
            count = len(sampleFiles)
            dicomFile = sampleFiles[0]
            ds = dorg_utilities.getDataSetFromFile(dicomFile)
            if (ds is None):
                continue
            if (len(sampleFiles) == 0):
                continue
            
            seriesDirectory = os.path.dirname(seriesDirFound)
            seriesDirectoryShort = os.path.basename(seriesDirectory)
            seriesDescription = dorg_utilities.getSeriesDescriptionFull(ds)

            line = "  Directory: %8s, Images: %4d, Description: %s\n" % (
                seriesDirectoryShort, len(sampleFiles), seriesDescription)
            f.write(line)
        f.close()
