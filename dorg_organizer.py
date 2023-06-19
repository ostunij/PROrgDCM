import os
import sys
import pydicom
import filecmp
import shutil
import os_utilities
from dorg_args import dicomOrganizerArgs

class dicomOrganizer:
    def __init__(self, do_args):

        # initialize dictionaries
        self.renameItemsDict = {}  # holds creation times for each file
        self.seriesCountDict = {}  # holds number of slices for each series
        self.touchItemsDict = {}  # holds creation times for each file
        self.touchSeriesDirDict = {}  # holds creation time for series
        self.seriesUIDDict = {}
        self.seriesUIDDict = {}
        self.fileList = None
        self.fileListExisting = None
        self.seriesOutputDirectoriesList = []
        self.studyOutputDirectoriesList = []
        self.readArguments(do_args)

    def readArguments(self, doa):
        self.verbose = doa.getVerboseMode()
        self.dicomInputDirectory = os_utilities.getCurrentWorkingDirectory()
        self.dicomOutputDirectory = os_utilities.getFullDirectoryPath(
            doa.getOutputDirectory())

        os_utilities.createDirectoryIfNeeded(self.dicomOutputDirectory)
        # self.prefix = doa.getPrefix()
        self.formatter = doa.getFormatter()

    def organizeData(self, fileList, dos):
        self.fileList = fileList

        for f in self.fileList:
            try:
                df = pydicom.dcmread(f, stop_before_pixels=True)
            except Exception as ex:
                print("Ignoring %s\n\t(%s)\n" % (f, ex))
                self.fileList.remove(f)
                continue

            (studyDirectory, seriesDirectory) = self.formatter.getOutputDirectories(
                df, self.dicomOutputDirectory, dos)
            if (not seriesDirectory in self.seriesOutputDirectoriesList):
                os_utilities.createDirectoryIfNeeded(seriesDirectory)
                self.seriesOutputDirectoriesList.append(seriesDirectory)
                if (not studyDirectory in self.studyOutputDirectoriesList):
                    self.studyOutputDirectoriesList.append(studyDirectory)

            outputName = self.formatter.getOutputFilename(df)
            self.renameItemsDict[f] = "%s/%s" % (seriesDirectory, outputName)

    def copyData(self, writeover, verbose):
        for itemName in self.renameItemsDict.keys():
            newItemName = self.renameItemsDict[itemName]
            index = 1
            newItemNameUpdated = newItemName
            if (verbose):
                print("Copying %s to %s" % (itemName, newItemName))
            while (not self.copyFileAndVerify(itemName, newItemNameUpdated, writeover, verbose)):
                index = index + 1
                newItemNameUpdated = self.getUpdatedVersionName(
                    newItemName, index)
                print("Copy Not Performed: \n\tNow copying %s to %s" % (itemName, newItemNameUpdated))

    def moveData(self, writeover, verbose):
        for itemName in self.renameItemsDict.keys():
            newItemName = self.renameItemsDict[itemName]
            index = 1
            newItemNameUpdated = newItemName
            if (verbose):
                print("Moving %s to %s" % (itemName, newItemName))
            while (not self.moveFileAndVerify(itemName, newItemNameUpdated, writeover, verbose)):
                index = index + 1
                newItemNameUpdated = self.getUpdatedVersionName(
                    newItemName, index)
                print("Move Not Performed: \n\tNow moving %s to %s" % (itemName, newItemNameUpdated))

    def copyFileAndVerify(self, itemName, newItemName, writeover, verbose):
        if (not os.path.exists(newItemName)):
            shutil.copyfile(itemName, newItemName)
            return True
        
        if writeover:
            if verbose:
                print("\tCopied - Overwrite Mode Set\n")
            shutil.copyfile(itemName, newItemName)
            return True

        if (self.dicomFilesAreTheSame(itemName, newItemName)):
            if verbose:
                print("\tCopied - Identical Files Found\n")
            shutil.copyfile(itemName, newItemName)
            return True

        if (self.dicomPixelsAreTheSame(itemName, newItemName)):
            if verbose:
                print("\tCopied - Identical Pixel Data Found\n")
            shutil.copyfile(itemName, newItemName)
            return True

        return False

    def moveFileAndVerify(self, itemName, newItemName, writeover, verbose):
        if (not os.path.exists(newItemName)):
            shutil.move(itemName, newItemName)
            return True

        if writeover:
            if verbose:
                print("\Moved - Overwrite Mode Set\n")
            shutil.movefile(itemName, newItemName)
            return True

        if (self.dicomFilesAreTheSame(itemName, newItemName)):
            if verbose:
                print("\Moved - Identical Files Found\n")
            shutil.move(itemName, newItemName)
            return True

        if (self.dicomPixelsAreTheSame(itemName, newItemName)):
            if verbose:
                print("\Moved - Identical Pixel Data Found\n")
            shutil.move(itemName, newItemName)
            return True

        return False

    def getOutputStudyDirectoryList(self):
        return self.studyOutputDirectoriesList

    def getOutputSeriesDirectoryList(self):
        return self.seriesOutputDirectoriesList

    def dicomFilesAreTheSame(self, file1, file2):
        sameFile = filecmp.cmp(file1, file2)
        return sameFile

    def dicomPixelsAreTheSame(self, file1, file2):
        df1 = pydicom.dcmread(file1)
        df2 = pydicom.dcmread(file2)
        try:
            pixels1 = df1.PixelData
            pixels2 = df2.PixelData
        except:
            print("\t No Pixel Data in %s or %s" % (file1, file2))
            return False

        samePixels = False
        if (pixels1 is None) or (pixels2 is None):
            return samePixels

        if (len(pixels1) > 0):
            samePixels = pixels1 == pixels2
        return samePixels

    def sameInstanceUID(self, file1, file2):
        df1 = pydicom.dcmread(file1, stop_before_pixels=True)
        df2 = pydicom.dcmread(file2, stop_before_pixels=True)
        uid1 = df1.file_meta.MediaStorageSOPInstanceUID
        uid2 = df2.file_meta.MediaStorageSOPInstanceUID
        value = uid1 == uid2
        return value

    def getUpdatedVersionName(self, newItemName, index):
        indexString = "_v%02d.dcm" % (index)
        vfile = newItemName.replace(".dcm", indexString)
        return vfile
