import sys
import re
import pydicom
import dorg_utilities
import os_utilities


class dicomFormatter:

    def __init__(self):
        pass

    def getOutputDirectory(self, df, outputDirectory, dos):
        patientName = dorg_utilities.getPatientName(df)
        patientID = dorg_utilities.getPatientID(df)
        studyDate = dorg_utilities.getStudyDate(df)
        studyID = dorg_utilities.getStudyID(df)
        seriesNumber = dorg_utilities.getSeriesNumber(df)
        prefix = dorg_utilities.getSOPprefix(df, dos)

        #print("Patient Name of " + patientName)
        #print("Patient ID of " + patientID)
        #print("Study Date of " + studyDate)
        #print("Study ID of " + studyID)
        #print("Series Number of " + seriesNumber)

        path1 = "%s" % (outputDirectory)
        path2 = "%s-%s" % (patientName, patientID)
        path1 = os_utilities.joinPaths(path1, path2)
        path2 = "%s-%s" % (studyDate, studyID)
        path1 = os_utilities.joinPaths(path1, path2)
        path2 = "%s_%s" % (prefix, seriesNumber)
        fileDirectory = os_utilities.joinPaths(path1, path2)
        #print("Returning output directory of %s" % (fileDirectory))

        return fileDirectory

    def getOutputName(self, df):
        seriesDescription = dorg_utilities.getSeriesDescription(df)
        instanceNumber = dorg_utilities.getInstanceNumber(df)
        #print("Series Description of " + seriesDescription)
        #print("Instance Number of " + instanceNumber)
        fileName = "%s_%s.dcm" % (seriesDescription, instanceNumber)

        return fileName

    def organizeDataByInstanceNumberAndCreator(self):
        existingSeriesUID = None
        implementationList = []
        self.renameItemsDict = {}

        fullname = ''

        for f in self.fileListExisting:
            try:
                df = pydicom.dcmread(f, stop_before_pixels=True)
            except Exception as ex:
                print("Ignoring %s\n\t(%s)" % (f, ex))
                continue
            existingSeriesUID = df.SeriesInstanceUID
            existingCreator = df.file_meta.ImplementationClassUID
            existingKey = "%s-%s" % (existingSeriesUID, existingCreator)
            break

        for f in self.fileList:
            try:
                df = pydicom.dcmread(f, stop_before_pixels=True)
            except Exception as ex:
                print("Ignoring %s\n\t(%s)" % (f, ex))
                continue
            creator = df.file_meta.ImplementationClassUID
            seriesUID = df.SeriesInstanceUID
            if (seriesUID != existingSeriesUID):
                postfix = "s02"
            currentKey = "%s-%s" % (seriesUID, creator)
            if (not creator in implementationList):
                implementationList.append(creator)

        implementationList.sort()

        for f in self.fileList:
            try:
                df = pydicom.dcmread(f, stop_before_pixels=True)
            except Exception as ex:
                print("Ignoring %s\n\t(%s)" % (f, ex))
                continue

            seriesNum = '00000'
            instanceNum = df.InstanceNumber
            instanceNum = "%05d" % (instanceNum)
            creator = df.file_meta.ImplementationClassUID
            outdir = self.seriesOutputDirectory
            postfix = None
            index = implementationList.index(creator)
            if (index > 0):
                index = index+1
                postfix = "c%02d" % (index)

            if (self.prefix is not None) and (postfix is not None):
                newName = "%s-%s/%s-%s.dcm" % (self.seriesOutputDirectory,
                                               postfix, self.prefix, instanceNum)
            elif (self.prefix is not None):
                newName = "%s/%s-%s.dcm" % (self.seriesOutputDirectory,
                                            self.prefix, instanceNum)
            elif (postfix is not None):
                newName = "%s-%s/%s.dcm" % (self.seriesOutputDirectory,
                                            postfix, instanceNum)
            else:
                newName = "%s/%s" % (self.seriesOutputDirectory, instanceNum)

            self.renameItemsDict[f] = newName
