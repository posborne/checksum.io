from crcmod.predefined import _crc_definitions_by_name, mkPredefinedCrcFun

class CRCAlgorithm(object):
    """Provide methods for reverse engineering CRC algorithms

    There are a couple types of classifiers here:
     - Brute force classifiers for "common" algorithms.  This will
       classify many of the algorithms including in the crcmod package.
     - More nuanced algorithms for finding crc algorithm polynomials
       using the research published by Gregory Ewing
       (http://www.cosc.canterbury.ac.nz/greg.ewing/essays/CRC-Reverse-Engineering.html)

    """
    
    def classify(self, payload, checksum):
        for name in _crc_definitions_by_name:
            crcfun = mkPredefinedCrcFun(name)
            if crcfun(payload) == checksum:
                return name

def main():
    algo = CRCAlgorithm()
    algo.classify('123456789', '\x4B\x37')

