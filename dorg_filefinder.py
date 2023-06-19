import sys
import os
import glob

class DCMfileFinder:
    def __init__(self, do_args):
        self.fileList = []
        self.inputSeriesList = []
        self.readArguments(do_args)

    def  readArguments(self, doa):
        self.verbose = doa.getVerboseMode()
        self.seriesInputDirectory = doa.getInputDirectory()
        

    def getDICOMData(self):
        os.chdir(self.seriesInputDirectory)
        self.fileList = glob.glob("**/*.dcm", recursive=True)
        if len(self.fileList) == 0:
            errorLine = 'No DICOM files found is %s -- exiting\n' % (self.programArgs)
            sys.stderr.write(errorLine)
            sys.exit(1)

        for dcmfile in self.fileList:
            dcmfileDirectory = os.path.dirname(dcmfile)
            absdcmfile = os.path.abspath(dcmfileDirectory)
            if (not absdcmfile in self.inputSeriesList):
                self.inputSeriesList.append(absdcmfile)

        return self.fileList
    
    def getInputSeriesDirectoryList(self):
        return self.inputSeriesList
