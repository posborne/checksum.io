from crcmod.predefined import mkPredefinedCrcFun, _crc_definitions_table


class PredefinedCRCAlgorithClassifier(object):
    """Provide methods for reverse engineering CRC algorithms

    There are a couple types of classifiers here:
     - Brute force classifiers for "common" algorithms.  This will
       classify many of the algorithms including in the crcmod package.
     - More nuanced algorithms for finding crc algorithm polynomials
       using the research published by Gregory Ewing
       (http://www.cosc.canterbury.ac.nz/greg.ewing/essays/CRC-Reverse-Engineering.html)

    """

    CRC_ALGORITHM_NAMES = [defn[0] for defn in _crc_definitions_table]

    def classify(self, payload, checksum):
        for name in self.CRC_ALGORITHM_NAMES:
            crcfun = mkPredefinedCrcFun(name)
            computed_checksum = crcfun(payload)
            if computed_checksum == checksum:
                return name
        return None
