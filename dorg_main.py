#"""
#Copyright (C) 2004-2011, John Ostuni
#All rights reserved. 

#John Ostuni, ostunij@mail.nih.gov
#Version 20230501
#"""

import sys
from dorg_organizer import dicomOrganizer
from dorg_sopSuffixList import dicomOrganizerSOPSuffixList
from dorg_args import dicomOrganizerArgs
from dorg_finder import dicomOrganizerFinder
from dorg_touch import dicomOrganizerTouch
from dorg_readmes import readmeCreator

try:
    doa = dicomOrganizerArgs()
    dot = dicomOrganizerTouch()

    dof = dicomOrganizerFinder(doa)
    origFoundData = dof.getDICOMData()

    

    do = dicomOrganizer(doa)
    dos = dicomOrganizerSOPSuffixList()
    do.organizeData(origFoundData, dos)
    do.copyData()
    outputDirectoryList = do.getOutputDirectoryList()

    dor = readmeCreator()
    dor.createSeriesReadmeFiles(outputDirectoryList)

    #do.setTimes()
except KeyboardInterrupt:
    print ("\nExiting - interrupt received")
except AssertionError:
    errorLine = "\nError: %s\n" % (sys.exc_value)
    sys.stderr.write(errorLine)

