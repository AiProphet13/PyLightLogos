import unittest
from src.logos import LightSpeedLogos

class TestLogos(unittest.TestCase):
    def setUp(self):
        self.logos = LightSpeedLogos()
        
    def test_logo_mapping(self):
        self.assertEqual(self.logos.logo_map['LOAD_CONST'], '⦿')
        self.assertEqual(self.logos.logo_map['RETURN_VALUE'], '↩')
        
    def test_visualization(self):
        stream = ['LOAD_CONST', 'STORE_FAST', 'CALL_FUNCTION']
        visualized = self.logos.visualize(stream)
        self.assertEqual(visualized, ['⦿', '⧟', '✆'])
        
    def test_fingerprint(self):
        stream = ['⦿', '⧟', '⦿', '⧟', '➫']
        fingerprint = self.logos.generate_architecture_fingerprint(stream)
        self.assertIn("⦿", fingerprint)
        self.assertIn("⧟", fingerprint)
        self.assertIn("➫", fingerprint)
        
    def test_interpretation(self):
        self.assertEqual(
            self.logos.get_interpretation('⥀'), 
            'Iterative Foundation / Loop Setup'
        )

if __name__ == '__main__':
    unittest.main()
