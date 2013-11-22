import unittest
from checksumio.algorithms.crc import PredefinedCRCAlgorithClassifier
from crcmod.predefined import mkPredefinedCrcFun


class TestPredefinedCRCAlgorithmClassifer(unittest.TestCase):

    def setUp(self):
        self.classifier = PredefinedCRCAlgorithClassifier()

    def test_crcmod_crc16(self):
        crcfun = mkPredefinedCrcFun("crc-16")
        self.assertEqual(crcfun('123456789'), 0xBB3D)

    def test_classify_crc16(self):
        classification = self.classifier.classify('123456789', 0xBB3D)
        self.assertEqual(classification, 'crc-16')

if __name__ == '__main__':
    unittest.main()
