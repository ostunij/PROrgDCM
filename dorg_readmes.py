import pydicom
import glob

class readmeCreator():
    def _init__(self):
        pass

    def createSeriesReadmeFiles(self, seriesDirectoryList):
        for seriesDir in seriesDirectoryList:
            self.createSeriesReadmeFile(seriesDir)


    def createSeriesReadmeFile(self, seriesDir):
        readmefile = "%s/Readme_series.txt" % (seriesDir)
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
