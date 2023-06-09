import sys
import re
import os
import pydicom
import dorg_utilities
import os_utilities
# FORMAT: PATIENTNAME-PATIENTID or PATIENTID
# FORMAT: /STUDYDATE-STUDYID
# FORMAT: /PREFIX_SERIESNUMBER
# FORMAT: /SERIESDESCRIPTION_INSTANCENUMBER.dcm


class dicomFormatter:

    def __init__(self, showpatientname):
        self.showpatientname = showpatientname
        # self.dicomImageToSeriesUID = {}
        # self.seriesDirectoryToSeriesUID = {}
        # self.dicomImageToSeriesDirectory = {}

    def getOutputDirectories(self, filename, df, outputDirectory, dos):
        patientName = dorg_utilities.getPatientName(df)
        patientID = dorg_utilities.getPatientID(df)
        studyDate = dorg_utilities.getStudyDate(df)
        studyID = dorg_utilities.getStudyID(df)
        seriesNumber = dorg_utilities.getSeriesNumber(df)
        prefix = dorg_utilities.getSOPprefix(df, dos)
        seriesUID = dorg_utilities.getSeriesUID(df)
        #self.dicomImageToSeriesUID[os.path.abspath(filename)] = seriesUID
        self.dicomImageToDirectory = []
        # print("Patient Name of " + patientName)
        # print("Patient ID of " + patientID)
        # print("Study Date of " + studyDate)
        # print("Study ID of " + studyID)
        # print("Series Number of " + seriesNumber)

        path1 = "%s" % (outputDirectory)
        path2 = "%s" % (patientID)
        if (self.showpatientname):
            path2 = "%s-%s" % (patientName, patientID)
        patientDirectory = os_utilities.joinPaths(path1, path2)

        path2 = "%s-%s" % (studyDate, studyID)
        studyDirectory = os_utilities.joinPaths(patientDirectory, path2)

        path2 = "%s_%s" % (prefix, seriesNumber)
        seriesDirectoryBase = os_utilities.joinPaths(studyDirectory, path2)

        seriesDirectory = seriesDirectoryBase
        useSeriesDirectory = False
        index = 1
        while (not useSeriesDirectory):
            if os.path.isdir(seriesDirectory):
                uidReadmeFile = "%s/SUID.txt" % seriesDirectory
                if os.path.isfile(uidReadmeFile):
                    f = open(uidReadmeFile, 'r')
                    line = f.readline()
                    f.close()

                    if (line.strip() == seriesUID):
                        useSeriesDirectory = True
                    else:
                        seriesDirectory = "%s_v%s" % (
                            seriesDirectoryBase, index)
                        index += 1
                else:
                    f = open(uidReadmeFile, 'w')
                    line = "%s\n" % (seriesUID)
                    f.write(line)
                    useSeriesDirectory = True
            else:
                useSeriesDirectory = True
        #self.dicomImageToSeriesDirectory[filename] = seriesDirectory

        return (studyDirectory, seriesDirectory)

    def getOutputFilename(self, df):
        seriesDescription = dorg_utilities.getSeriesDescription(df)
        instanceNumber = dorg_utilities.getInstanceNumber(df)
        # print("Series Description of " + seriesDescription)
        # print("Instance Number of " + instanceNumber)
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
