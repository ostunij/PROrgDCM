import sys
import os
from optparse import OptionParser
from dorg_formatter import dicomFormatter

class dicomOrganizerArgs:
    def __init__(self):
        usage = 'usage: %prog [options] directoryName'
        self.parser = OptionParser(usage=usage, add_help_option=False)
        self.setOptions()
        self.readOptions()
        self.checkOptions()
        if self.verbose:
            self.preamble()
            self.printOptions()

    def setOptions(self):
        self.parser.add_option("-o", "--outdir", action="store", type="string",
                               dest="outdir", help="output directory -- default is cwd", default=os.getcwd())
        self.parser.add_option("-r", "--removeorigdata", action="store_true", dest="removeorigdata",
                               help="remove original data after organization", default=False)
        self.parser.add_option("-n", "--notimestamps", action="store_false",
                               dest="usetimestamps", help="don't set time stamps", default=True)
        self.parser.add_option("-s", "--showPatientName", action="store_true",
                               dest="showpatientname", help="show patient name in directory structure", default=False)
        self.parser.add_option("-w", "--writeover", action="store_true", dest="overwrite",
                               help="write over existing organized data", default=False)
        self.parser.add_option("-v", "--verbose", action="store_true",
                               dest="verbose", help="verbose mode", default=False)
        self.parser.add_option("-h", "--help", action="store_true",
                               dest="help", help="print help", default=False)

    def readOptions(self):
        (options, args) = self.parser.parse_args()
        if options.help:
            self.__preamble()
            self.parser.print_help()
            sys.exit()
        self.usetimestamps = options.usetimestamps
        self.removeorigdata = options.removeorigdata
        self.overwrite = options.overwrite
        self.verbose = options.verbose
        self.outdir = options.outdir
        self.showpatientname = options.showpatientname
        self.programArgs = args

    def checkOptions(self):
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir, 0o755)

        if not os.path.exists(self.outdir):
            errorLine = 'Specified output directory (%s) does not exist\n' % self.outdir
            sys.stderr.write(errorLine)
            sys.exit(1)

        if not os.path.isdir(self.outdir):
            errorLine = 'Specified output directory (%s) is not a directory)\n' % self.outdir
            sys.stderr.write(errorLine)
            sys.exit(1)
        if not os.access(self.outdir, os.W_OK):
            errorLine = 'Specified output directory (%s) is not writable\n' % self.outdir
            sys.stderr.write(errorLine)
            sys.exit(1)

        self.seriesOutputDirectory = os.path.abspath(self.outdir)

        if len(self.programArgs) == 0:
            sys.stderr.write('Error - no DICOM directories provided\n\n')
            self.__preamble()
            self.parser.print_help()
            sys.exit(1)

        if len(self.programArgs) > 1:
            sys.stderr.write('Error - multiple DICOM directories provided\n\n')
            self.__preamble()
            self.parser.print_help()
            sys.exit(1)

        self.seriesInputDirectory = self.programArgs[0]

        if not os.path.exists(self.seriesInputDirectory):
            errorLine = 'Specified DICOM directory (%s) does not exist\n' % self.seriesInputDirectory
            sys.stderr.write(errorLine)
            sys.exit(1)
        if not os.path.isdir(self.seriesInputDirectory):
            errorLine = 'Specified DICOM directory (%s) is not a directory\n' % self.seriesInputDirectory
            sys.stderr.write(errorLine)
            sys.exit(1)
        if not os.access(self.seriesInputDirectory, os.R_OK):
            errorLine = 'Specified DICOM directory (%s) is not readable\n' % self.seriesInputDirectory
            sys.stderr.write(errorLine)
            sys.exit(1)

    def preamble(self):
        print("PackRat Software")
        print("John Ostuni, ostunij@mail.nih.gov (NIH/NIAAA)")
        print()

    def printOptions(self):
        print("Input directory: ")
        print("\t %s " % self.seriesInputDirectory)

        print("Options:")
        print("\tOutput Directory: %s " % self.seriesOutputDirectory)

        print("\tVerbose mode set")

        if not self.usetimestamps:
            print("\tTime Stamps will not be set")

        if self.removeorigdata:
            print("\tOriginal data will be removed after organization")

        if self.overwrite:
            print("\tExisting organized files will be overwritten if they exist")
        if self.showpatientname:
            print("\tPatient Name will be included in output directory structure")
        print()

    def getVerboseMode(self):
        return self.verbose

    def getInputDirectory(self):
        return self.seriesInputDirectory

    def getOutputDirectory(self):
        return self.seriesOutputDirectory

    def getFormatter(self):
        return dicomFormatter(self.showpatientname)
