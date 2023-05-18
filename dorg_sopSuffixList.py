import re


class dicomOrganizerSOPSuffixList:
    def __init__(self):
        SOPlist = self.getSOPSuffixList()
        self.readSOPprefixlist(SOPlist)

    def getPrefix(self, SOPinstanceUID):
        if (SOPinstanceUID in self.SOPdict.keys()):
            return self.SOPdict[SOPinstanceUID]
        else:
            return "uk"

    def readSOPprefixlist(self, SOPlist):
        self.SOPdict = {}

        for line in SOPlist:
            line = re.sub("\s+", " ", line)
            line = line.strip()
            tokens = line.split(" ")
            if len(tokens) == 3:
                sopname = tokens[0]
                sopprefix = tokens[1]
                self.SOPdict[sopname] = sopprefix
                # print("mapping -%s- to -%s-" % (sopprefix, sopname))

    def getSOPSuffixList(self):
        SOPlist = [
            "1.2.840.10008.5.1.4.1.1.1                       cr   ComputedRadiographyImageStorage",
            "1.2.840.10008.5.1.4.1.1.1.1  	                 xn   DigitalXRayImageStorageForPresentation",
            "1.2.840.10008.5.1.4.1.1.1.1.1                   xg   DigitalXRayImageStorageForProcessing",
            "1.2.840.10008.5.1.4.1.1.1.2                    mxn   DigitalMammographyXRayImageStorageForPresentation",
            "1.2.840.10008.5.1.4.1.1.1.2.1                  mxg   DigitalMammographyXRayImageStorageForProcessing",
            "1.2.840.10008.5.1.4.1.1.1.3                    ixn   DigitalIntraOralXRayImageStorageForPresentation",
            "1.2.840.10008.5.1.4.1.1.1.3.1                  ixp   DigitalIntraOralXRayImageStorageForProcessing",
            "1.2.840.10008.5.1.4.1.1.104.1                 epdf   EncapsulatedPDFStorage",
            "1.2.840.10008.5.1.4.1.1.11.1                   gsp   GrayscaleSoftcopyPresentationStateStorage",
            "1.2.840.10008.5.1.4.1.1.11.2                   csp   ColorSoftcopyPresentationStateStorage",
            "1.2.840.10008.5.1.4.1.1.11.3                   psp   PseudoColorSoftcopyPresentationStateStorage",
            "1.2.840.10008.5.1.4.1.1.11.4                   bsp   BlendingSoftcopyPresentationStateStorage",
            "1.2.840.10008.5.1.4.1.1.12.1                    xa   XRayAngiographicImageStorage",
            "1.2.840.10008.5.1.4.1.1.12.1.1                 exa   EnhancedXAImageStorage",
            "1.2.840.10008.5.1.4.1.1.12.2                    xf   XRayFluoroscopyImageStorage",
            "1.2.840.10008.5.1.4.1.1.12.2.1                 exf   EnhancedXRFImageStorage",
            "1.2.840.10008.5.1.4.1.1.128                    pet   PETImageStorage",
            "1.2.840.10008.5.1.4.1.1.129                    ptc   PETCurveStorage",
            "1.2.840.10008.5.1.4.1.1.2                       ct   CTImageStorage",
            "1.2.840.10008.5.1.4.1.1.2.1                    ect   EnhancedCTImageStorage",
            "1.2.840.10008.5.1.4.1.1.20                      nm   NuclearMedicineImageStorage",
            "1.2.840.10008.5.1.4.1.1.3.1                    usm   UltrasoundMultiframeImageStorage",
            "1.2.840.10008.5.1.4.1.1.4                       mr   MRImageStorage",
            "1.2.840.10008.5.1.4.1.1.4.1                    emr   EnhancedMRImageStorage",
            "1.2.840.10008.5.1.4.1.1.4.2                    mrs   MRSpectroscopyStorage",
            "1.2.840.10008.5.1.4.1.1.481.1                   rt   RTImageStorage",
            "1.2.840.10008.5.1.4.1.1.481.2                  rtd   RTDoseStorage",
            "1.2.840.10008.5.1.4.1.1.481.3                 rtss   RTStructureSetStorage",
            "1.2.840.10008.5.1.4.1.1.481.4                 rtbm   RTBeamsTreatmentRecordStorage",
            "1.2.840.10008.5.1.4.1.1.481.5                  rtp   RTPlanStorage",
            "1.2.840.10008.5.1.4.1.1.481.6                 rtby   RTBrachyTreatmentRecordStorage",
            "1.2.840.10008.5.1.4.1.1.481.7                  rtt   RTTreatmentSummaryRecordStorage",
            "1.2.840.10008.5.1.4.1.1.6.1                     us   UltrasoundImageStorage",
            "1.2.840.10008.5.1.4.1.1.66                     raw   RawDataStorage",
            "1.2.840.10008.5.1.4.1.1.66.1                   srg   SpatialRegistrationStorage",
            "1.2.840.10008.5.1.4.1.1.66.2                   sfl   SpatialFiducialsStorage",
            "1.2.840.10008.5.1.4.1.1.67                     rwm   RealWorldValueMappingStorage",
            "1.2.840.10008.5.1.4.1.1.7                       sc   SecondaryCaptureImageStorage",
            "1.2.840.10008.5.1.4.1.1.7.1                   mssc   MultiframeSingleBitSecondaryCaptureImageStorage",
            "1.2.840.10008.5.1.4.1.1.7.2                   mbsc   MultiframeGrayscaleByteSecondaryCaptureImageStorage",
            "1.2.840.10008.5.1.4.1.1.7.3                   mwsc   MultiframeGrayscaleWordSecondaryCaptureImageStorage",
            "1.2.840.10008.5.1.4.1.1.7.4                   mtsc   MultiframeTrueColorSecondaryCaptureImageStorage",
            "1.2.840.10008.5.1.4.1.1.77.1.1                 vle   VLEndoscopicImageStorage",
            "1.2.840.10008.5.1.4.1.1.77.1.2                 vlm   VLMicroscopicImageStorage",
            "1.2.840.10008.5.1.4.1.1.77.1.3                 vls   VLSlideCoordinatesMicroscopicImageStorage",
            "1.2.840.10008.5.1.4.1.1.77.1.4                 vlp   VLPhotographicImageStorage",
            "1.2.840.10008.5.1.4.1.1.77.1.5.1               op8   OphthalmicPhotography8BitImageStorage",
            "1.2.840.10008.5.1.4.1.1.77.1.5.2              op16   OphthalmicPhotography16BitImageStorage",
            "1.2.840.10008.5.1.4.1.1.77.1.5.3               smr   StereometricRelationshipStorage",
            "1.2.840.10008.5.1.4.1.1.88.11                   sr   BasicTextSR",
            "1.2.840.10008.5.1.4.1.1.88.22                  esr   EnhancedSR",
            "1.2.840.10008.5.1.4.1.1.88.33                  csr   ComprehensiveSR",
            "1.2.840.10008.5.1.4.1.1.88.40                   pl   ProcedureLogStorage",
            "1.2.840.10008.5.1.4.1.1.88.50                 mcsr   MammographyCADSR",
            "1.2.840.10008.5.1.4.1.1.88.59                  key   KeyObjectSelectionDocument",
            "1.2.840.10008.5.1.4.1.1.88.65                 ccsr   ChestCADSR",
            "1.2.840.10008.5.1.4.1.1.88.67                  xsr   XRayRadiationDoseSR",
            "1.2.840.10008.5.1.4.1.1.9.1.1                 tecg   TwelveLeadECGWaveformStorage",
            "1.2.840.10008.5.1.4.1.1.9.1.2                  ecg   GeneralECGWaveformStorage",
            "1.2.840.10008.5.1.4.1.1.9.1.3                 aecg   AmbulatoryECGWaveformStorage",
            "1.2.840.10008.5.1.4.1.1.9.2.1                   hw   HemodynamicWaveformStorage",
            "1.2.840.10008.5.1.4.1.1.9.3.1                  cew   CardiacElectrophysiologyWaveformStorage",
            "1.2.840.10008.5.1.4.1.1.9.4.1                  bvw   BasicVoiceAudioWaveformStorage",
        ]
        return SOPlist
