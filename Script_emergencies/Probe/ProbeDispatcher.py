# coding: UTF-8
"""
Script: Trame/ProbeDispatcher
Création: rdouet, le 25/05/2021
"""


# Import
from Probe.probe import Co2Probe, CovProbe, PmProbe

# Programme principal
class ProbeDispatcher:

    _probe = [Co2Probe(), CovProbe(), PmProbe()]

    def getProbe(self, senderId):
        for probe in self._probe:
            if probe.canParse(self.getIdSender(senderId)):
                return probe
        raise NoProbeFoundException


    def getIdSender(self, frame):
        if frame == None or len(frame)<1:
            raise NoProbeFoundException
        return frame[11:11+4]

class NoProbeFoundException(Exception):
    print("Unknown probe")

# Fin
