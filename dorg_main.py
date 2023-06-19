#"""
#John Ostuni, ostunij@mail.nih.gov
#Version 202306
#"""

import datetime
import os
import sys
from dorg_organizer import dicomOrganizer
from dorg_sopSuffixList import dicomOrganizerSOPSuffixList
from dorg_args import dicomOrganizerArgs
from dorg_filefinder import DCMfileFinder
from dorg_touch import dicomOrganizerTouch
from dorg_readmes import readmeCreator

try:
    currentDateTimeStamp = datetime.datetime.now()
    startingDirectory = os.getcwd()

    doa = dicomOrganizerArgs()
    
    dof = DCMfileFinder(doa)
    origFoundData = dof.getDICOMData()

    dos = dicomOrganizerSOPSuffixList()
    do = dicomOrganizer(doa)
   
    do.organizeData(origFoundData, dos)
    if doa.removeorigdata:
        do.moveData(doa.overwrite, doa.verbose)
        
    else:
        do.copyData(doa.overwrite, doa.verbose)

    outputStudyDirectoryList = do.getOutputStudyDirectoryList()
    outputSeriesDirectoryList = do.getOutputSeriesDirectoryList()

    dor = readmeCreator()
    dor.createSeriesReadmeFiles(outputSeriesDirectoryList)
    dor.createStudyReadmeFiles(outputStudyDirectoryList)
    if doa.usetimestamps:
        dot = dicomOrganizerTouch(outputStudyDirectoryList, currentDateTimeStamp)
        dot.setTimeStamps()

    #cleanup
    os.chdir(startingDirectory)
    if doa.removeorigdata:
        inputSeriesDirectoryList = dof.getInputSeriesDirectoryList()
        for inputSeriesDirectory in inputSeriesDirectoryList:
            if (not os.listdir(inputSeriesDirectory)):
                print("EMPTY checking directory %s from %s" % (inputSeriesDirectory, os.getcwd()))
                os.rmdir(inputSeriesDirectory)
        

except KeyboardInterrupt:
    print ("\nExiting - interrupt received")
except AssertionError:
    errorLine = "\nError: %s\n" % (sys.exc_value)
    sys.stderr.write(errorLine)

