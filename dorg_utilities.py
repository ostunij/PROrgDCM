import re
import pydicom


def getDataSetFromFile(f):
    try:
        ds = pydicom.dcmread(f, stop_before_pixels=True)
    except:
        ds = None
        print("file %s has null data set" % (f))
    return ds


def getPatientName(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0010, 0x0010))  # patient Name
    valueFound = False
    defaultValue = "UNKNOWN_SUBJECT"
    try:
        for tag in possibleTagList:
            if tag in fileDataSet:
                tagValue = fileDataSet[tag].value
                tagValueString = "%s" % tagValue
                if (tagValueString is not None and len(tagValueString.strip()) > 0):
                    valueFound = True
                    break
    except:
        valueFound = False

    if valueFound:
        tagValueString = re.sub('[^a-zA-Z0-9_]', '_', tagValueString)
        tagValueString = re.sub('_+', '_', tagValueString)
        tagValueString = re.sub('^_', '', tagValueString)
        tagValueString = re.sub('_$', '', tagValueString)
        tagValueString = tagValueString.strip()
        tagValueString = tagValueString.upper()
    else:
        tagValueString = defaultValue

    return tagValueString


def getPatientID(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0010, 0x0020))  # patient ID
    valueFound = False
    defaultValue = "00000000"
    try:
        for tag in possibleTagList:
            if tag in fileDataSet:
                tagValue = fileDataSet[tag].value
                tagValueString = "%s" % tagValue
                tagValueString = re.sub('[-_\s]', '', tagValueString)
                if (tagValueString is not None and len(tagValueString.strip()) > 0):
                    valueFound = True
                    break
    except:
        valueFound = False

    if valueFound:
        tagValueString = tagValueString.strip()
        while (len(tagValueString) < 8):
            tagValueString = "0%s" % tagValueString
    else:
        tagValueString = defaultValue

    return tagValueString


def getStudyDate(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0008, 0x0020))  # study Date
    possibleTagList.append((0x0008, 0x0022))  # acquisition Date
    possibleTagList.append((0x0008, 0x0023))  # content Date
    possibleTagList.append((0x0008, 0x0021))  # series Date
    valueFound = False
    defaultValue = "19000101"
    try:
        for tag in possibleTagList:
            if tag in fileDataSet:
                tagValue = fileDataSet[tag].value
                tagValueString = "%s" % tagValue
                if (len(tagValueString.strip()) == 8):
                    valueFound = True
                    break
    except:
        valueFound = False

    if valueFound:
        value = tagValueString.strip()
        year = value[0:4]
        month = value[4:6]
        day = value[6:8]
        dateString = '%s%s%s' % (year, month, day)
    else:
        dateString = defaultValue

    return dateString


def getSeriesDateTokens(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0008, 0x0021))  # series Date
    possibleTagList.append((0x0008, 0x0020))  # study Date
    possibleTagList.append((0x0008, 0x0022))  # acquisition Date
    possibleTagList.append((0x0008, 0x0023))  # content Date
    valueFound = False
    defaultYear = "1900"
    defaultMonth = "01"
    defaultDay = "01"
    try:
        for tag in possibleTagList:
            if tag in fileDataSet:
                tagValue = fileDataSet[tag].value
                tagValueString = "%s" % tagValue
                if (len(tagValueString.strip()) == 8):
                    valueFound = True
                    break
    except:
        valueFound = False

    if valueFound:
        value = tagValueString.strip()
        year = value[0:4]
        month = value[4:6]
        day = value[6:8]
    else:
        year = defaultYear
        month = defaultMonth
        day = defaultDay

    return (year, month, day)


def getSeriesTimeTokens(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0008, 0x0031))  # series Time
    possibleTagList.append((0x0008, 0x0030))  # study Time
    possibleTagList.append((0x0008, 0x0032))  # acquisition Time
    possibleTagList.append((0x0008, 0x0033))  # content Time
    valueFound = False
    defaultHour = "12"
    defaultMinute = "00"
    defaultSecond = "00"
    try:
        for tag in possibleTagList:
            if tag in fileDataSet:
                tagValue = fileDataSet[tag].value
                tagValueString = "%s" % tagValue
                if (len(tagValueString.strip()) == 8):
                    valueFound = True
                    break
    except:
        valueFound = False

    if valueFound:
        hour = tagValueString[0:4]
        minute = tagValueString[4:6]
        second = tagValueString[6:8]
    else:
        hour = defaultHour
        minute = defaultMinute
        second = defaultSecond

    return (hour, minute, second)


def getStudyID(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0020, 0x0010))  # study ID
    valueFound = False
    defaultValue = "00000"
    try:
        for tag in possibleTagList:
            if tag in fileDataSet:
                tagValue = fileDataSet[tag].value
                tagValueString = "%s" % tagValue
                valueFound = True
                break
    except:
        valueFound = False

    if valueFound:
        tagValueString = tagValueString.strip()
        while (len(tagValueString) < 5):
            tagValueString = "0%s" % (tagValueString)
    else:
        tagValueString = defaultValue

    return tagValueString


def getSeriesDescription(fileDataSet):
    tagValueString = getSeriesDescriptionFull(fileDataSet)
    tagValueString = re.sub('[^a-zA-Z0-9_]', '_', tagValueString)
    tagValueString = re.sub('_+', '_', tagValueString)
    tagValueString = re.sub('_', '', tagValueString)
    if (len(tagValueString) > 8):
        tagValueString = tagValueString[0:8]
    return tagValueString


def getSeriesDescriptionFull(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0008, 0x103E))  # series Description

    valueFound = False
    defaultValue = "no_desc"
    try:
        for tag in possibleTagList:
            if tag in fileDataSet:
                tagValue = fileDataSet[tag].value
                tagValueString = "%s" % tagValue
                valueFound = True
                break
    except:
        valueFound = False

    if valueFound:
        tagValueString = tagValueString.strip()
        tagValueString = tagValueString.lower()
    else:
        tagValueString = defaultValue

    return tagValueString



def SeriesDescriptionFromFile(dicomFile):
    defaultValue = "no_desc"
    try:
        ds = pydicom.dcmread(dicomFile, stop_before_pixels=True)
        seriesDescription = getSeriesDescription(ds)
    except:
        seriesDescription = defaultValue

    return seriesDescription

def getSeriesUID(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0020, 0x000E))  # series UID 
    valueFound = False
    defaultValue = "0"
    try:
        for tag in possibleTagList:
            if tag in fileDataSet:
                tagValue = fileDataSet[tag].value
                tagValueString = "%s" % tagValue
                valueFound = True
                break
    except:
        valueFound = False

    if valueFound:
        tagValueString = tagValueString.strip()
    else:
        tagValueString = defaultValue

    return tagValueString


def getAccessionNumber(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0008, 0x0050))  # accession Number

    valueFound = False
    defaultValue = "No_Accession_Number"
    try:
        for tag in possibleTagList:
            if tag in fileDataSet:
                tagValue = fileDataSet[tag].value
                tagValueString = "%s" % tagValue
                valueFound = True
                break
    except:
        valueFound = False

    if valueFound:
        tagValueString = re.sub('[^-a-zA-Z0-9_]', '_', tagValueString)
        tagValueString = re.sub('_+', '_', tagValueString)
        tagValueString = re.sub('_', '', tagValueString)
        tagValueString = tagValueString.strip()
    else:
        tagValueString = defaultValue

    return tagValueString


def getStationName(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0008, 0x1010))  # station Name
    valueFound = False
    defaultValue = "None_Provided"
    try:
        for tag in possibleTagList:
            if tag in fileDataSet:
                tagValue = fileDataSet[tag].value
                tagValueString = "%s" % tagValue
                valueFound = True
                break
    except:
        valueFound = False

    if valueFound:
        tagValueString = re.sub('[^-a-zA-Z0-9_]', '_', tagValueString)
        tagValueString = re.sub('_+', '_', tagValueString)
        tagValueString = re.sub('_', '', tagValueString)
        tagValueString = tagValueString.strip()
    else:
        tagValueString = defaultValue

    return tagValueString


def getSeriesNumber(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0020, 0x0011))  # series Number

    valueFound = False
    defaultValue = "0000"
    try:
        for tag in possibleTagList:
            if tag in fileDataSet:
                tagValue = fileDataSet[tag].value
                tagValueString = "%s" % (tagValue)
                valueFound = True
    except:
        valueFound = False

    if valueFound:
        while (len(tagValueString) < 4):
            tagValueString = "0%s" % (tagValueString)
    else:
        tagValueString = defaultValue

    return tagValueString


def getInstanceNumber(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0020, 0x0013))  # instance Number

    valueFound = False
    defaultValue = "00000"

    try:
        for tag in possibleTagList:
            if tag in fileDataSet:
                tagValue = fileDataSet[tag].value
                tagValueString = "%s" % (tagValue)
                valueFound = True
    except:
        valueFound = False

    if valueFound:
        while (len(tagValueString) < 5):
            tagValueString = "0%s" % (tagValueString)
    else:
        tagValueString = defaultValue

    return tagValueString


def getSOPprefix(fileDataSet, dos):
    possibleTagList = []
    possibleTagList.append((0x0008, 0x0016))  # SOP instance UID

    valueFound = False
    defaultValue = "uk"
    try:
        for tag in possibleTagList:
            if tag in fileDataSet:
                tagValue = fileDataSet[tag].value
                tagValueString = "%s" % (tagValue)
                valueFound = True
    except:
        valueFound = False

    if (valueFound):
        prefix = dos.getPrefix(tagValueString)
    else:
        prefix = defaultValue

    return prefix


def getDateTimeString(fileDataSet):
    (year, month, day) = getSeriesDateTokens(fileDataSet)
    (hour, minute, second) = getSeriesTimeTokens(fileDataSet)
    return (year, month, day, hour, minute, second)
