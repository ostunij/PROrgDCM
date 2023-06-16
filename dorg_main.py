#"""
#John Ostuni, ostunij@mail.nih.gov
#Version 202306
#"""

import datetime
import sys
from dorg_organizer import dicomOrganizer
from dorg_sopSuffixList import dicomOrganizerSOPSuffixList
from dorg_args import dicomOrganizerArgs
from dorg_filefinder import DCMfileFinder
from dorg_touch import dicomOrganizerTouch
from dorg_readmes import readmeCreator

try:
    currentDateTimeStamp = datetime.datetime.now()
    doa = dicomOrganizerArgs()
    
    dof = DCMfileFinder(doa)
    origFoundData = dof.getDICOMData()

    dos = dicomOrganizerSOPSuffixList()
    do = dicomOrganizer(doa)
   
    do.organizeData(origFoundData, dos)
    do.copyData()

    outputStudyDirectoryList = do.getOutputStudyDirectoryList()
    outputSeriesDirectoryList = do.getOutputSeriesDirectoryList()

    dor = readmeCreator()
    dor.createSeriesReadmeFiles(outputSeriesDirectoryList)
    dor.createStudyReadmeFiles(outputStudyDirectoryList)

    dot = dicomOrganizerTouch(outputStudyDirectoryList, currentDateTimeStamp)
    dot.setTimeStamps()
    
except KeyboardInterrupt:
    print ("\nExiting - interrupt received")
except AssertionError:
    errorLine = "\nError: %s\n" % (sys.exc_value)
    sys.stderr.write(errorLine)

