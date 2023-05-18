import os

class dicomOrganizerTouch:
    def __init__(self):
        pass
    
    
    def setTimes(self):
        if self.usetimestamps and self.verbose:
            print ("Setting DICOM file date/times")

        items = self.touchItemsDict.keys()
        items.sort()
        items.reverse()
        for item in items:
            timestamp = self.touchItemsDict[item]
            if self.usetimestamps:
                if os.path.exists(item):
                    command = 'touch -t %s %s' % (timestamp, item)
                    os.system(command)

        items = self.touchSeriesDirDict.keys()
        items.sort()
        items.reverse()
        for item in items:
            timestamp = self.touchSeriesDirDict[item]
            if self.usetimestamps:
                if os.path.exists(item):
                    command = 'touch -t %s %s' % (timestamp, item)
                    os.system(command)                    

  
