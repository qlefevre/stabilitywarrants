import unittest
from utils import extract_number


class TestUtilsMethods(unittest.TestCase):

    def test_extract_number(self):
        self.assertEqual(extract_number('7600,0000 POINTS'), '7600')
        self.assertEqual(extract_number('7800,00 Points'), '7800')
        self.assertEqual(extract_number('13,0000 EUR'), '13')
        self.assertEqual(extract_number('22,50 EUR'), '22,50')
        self.assertEqual(extract_number('7,5000'), '7,50')


if __name__ == '__main__':
    unittest.main()
