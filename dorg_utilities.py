import os
import re

def getPatientName(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0010, 0x0010))  # patient Name
    valueFound = False
    defaultValue = "UNKNOWN_SUBJECT"

    for tag in possibleTagList:
        if tag in fileDataSet:
            tagValue = fileDataSet[tag].value
            tagValueString = "%s" % tagValue
            if (tagValueString is not None and len(tagValueString.strip()) > 0):
                valueFound = True
                break
    if valueFound:
        tagValueString = re.sub('[^a-zA-Z0-9_]', '_', tagValueString)
        tagValueString = re.sub('_+', '_', tagValueString)
        tagValueString = re.sub('^_', '', tagValueString)
        tagValueString = re.sub('_$', '', tagValueString)
    else:
        tagValueString = defaultValue

    tagValueString = tagValueString.strip()
    tagValueString = tagValueString.upper()

    return tagValueString


def getPatientID(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0010, 0x0020))  # patient ID
    valueFound = False
    defaultValue = "00000000"

    for tag in possibleTagList:
        if tag in fileDataSet:
            tagValue = fileDataSet[tag].value
            tagValueString = "%s" % tagValue
            tagValueString = re.sub('[-_\s]', '', tagValueString)
            while (len(tagValueString) < 8):
                tagValueString = "0%s" % tagValueString
            if (tagValueString is not None and len(tagValueString.strip()) > 0):
                valueFound = True
                break

    if (not valueFound):
        tagValueString = defaultValue

    tagValueString = tagValueString.strip()

    return tagValueString


def getStudyDate(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0008, 0x0020))  # study Date
    possibleTagList.append((0x0008, 0x0021))  # series Date
    possibleTagList.append((0x0008, 0x0022))  # Acquisition Date
    possibleTagList.append((0x0008, 0x0023))  # content Date
    valueFound = False
    defaultValue = "19000101"

    for tag in possibleTagList:
        if tag in fileDataSet:
            tagValue = fileDataSet[tag].value
            tagValueString = "%s" % tagValue
            if (len(tagValueString.strip()) == 8):
                valueFound = True
                break

    if not valueFound:
        tagValueString = defaultValue

    value = tagValueString.strip()
    year = value[0:4]
    month = value[4:6]
    day = value[6:8]
    dateString = '%s_%s_%s' % (year, month, day)
    dateString = '%s%s%s' % (year, month, day)
    return dateString


def getStudyID(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0020, 0x0010))  # study ID

    valueFound = False
    defaultValue = "00000"

    for tag in possibleTagList:
        if tag in fileDataSet:
            tagValue = fileDataSet[tag].value
            tagValueString = "%s" % tagValue
            valueFound = True
            break

    if not valueFound:
        tagValueString = defaultValue

    tagValueString = tagValueString.strip()

    while (len(tagValueString) < 5):
        tagValueString = "0%s" % (tagValueString)

    return tagValueString


def getSeriesDescription(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0008, 0x103E))  # study ID

    valueFound = False
    defaultValue = "NO_DESCRIPTION"

    for tag in possibleTagList:
        if tag in fileDataSet:
            tagValue = fileDataSet[tag].value
            tagValueString = "%s" % tagValue
            tagValueString = tagValueString.strip()
            valueFound = True
            break

    if valueFound:
        tagValueString = re.sub('[^a-zA-Z0-9_]', '_', tagValueString)
        tagValueString = re.sub('_+', '_', tagValueString)
        #tagValueString = re.sub('^_', '', tagValueString)
        #tagValueString = re.sub('_$', '', tagValueString)
        tagValueString = re.sub('_', '', tagValueString)
    else:
        tagValue = defaultValue
        tagValueString = "%s" % tagValue

    tagValueString = tagValueString.strip()
    tagValueString = tagValueString.lower()

    return tagValueString


def getSeriesNumber(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0020, 0x0011))  # series Number

    valueFound = False
    defaultValue = 1

    for tag in possibleTagList:
        if tag in fileDataSet:
            tagValue = fileDataSet[tag].value
            tagValueString = "%s" % (tagValue)
            valueFound = True

    if not valueFound:
        tagValue = defaultValue
        tagValueString = "%s" % (tagValue)

    while (len(tagValueString) < 4):
        tagValueString = "0%s" % (tagValueString)

    return tagValueString


def getInstanceNumber(fileDataSet):
    possibleTagList = []
    possibleTagList.append((0x0020, 0x0013))  # instance Number

    valueFound = False
    defaultValue = 1

    for tag in possibleTagList:
        if tag in fileDataSet:
            tagValue = fileDataSet[tag].value
            tagValueString = "%s" % (tagValue)
            valueFound = True

    if not valueFound:
        tagValue = defaultValue
        tagValueString = "%s" % (tagValue)

    while (len(tagValueString) < 5):
        tagValueString = "0%s" % (tagValueString)

    return tagValueString

def getSOPprefix(fileDataSet, dos):
    possibleTagList = []
    possibleTagList.append((0x0008, 0x0016))  # SOP instance UID

    valueFound = False
    defaultValue = "uk"

    for tag in possibleTagList:
        if tag in fileDataSet:
            tagValue = fileDataSet[tag].value
            tagValueString = "%s" % (tagValue)
            valueFound = True

    if (valueFound):
        prefix = dos.getPrefix(tagValueString)
    else:
        prefix = defaultValue

    return prefix
