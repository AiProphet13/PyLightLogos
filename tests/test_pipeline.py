import unittest
from src.pipeline import extract_bytecode_patterns, compress_bytecode, optimize_with_peephole

class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.sample_code = "x = 5\ny = 10\nz = x + y"
        
    def test_pattern_extraction(self):
        micro_ops, instructions, normalized = extract_bytecode_patterns(self.sample_code)
        self.assertGreater(len(micro_ops), 0)
        self.assertGreater(len(instructions), 0)
        self.assertEqual(len(instructions), len(normalized))
        
    def test_compression(self):
        micro_ops, instructions, normalized = extract_bytecode_patterns(self.sample_code)
        compressed = compress_bytecode(instructions, normalized, micro_ops)
        self.assertLessEqual(len(compressed), len(instructions))
        
    def test_peephole_optimization(self):
        compressed = ['LOAD_CONST', 'STORE_FAST', 'LOAD_CONST', 'STORE_FAST']
        rules = {('LOAD_CONST', 'STORE_FAST'): 'SUPER_MACRO_ASSIGN'}
        optimized = optimize_with_peephole(compressed, rules)
        self.assertEqual(optimized, ['SUPER_MACRO_ASSIGN', 'SUPER_MACRO_ASSIGN'])
        
    def test_invalid_code(self):
        with self.assertRaises(ValueError):
            extract_bytecode_patterns("invalid python code")

if __name__ == '__main__':
    unittest.main()
