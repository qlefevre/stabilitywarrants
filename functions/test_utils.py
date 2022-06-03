import unittest
from utils import to_number
from utils import clean_asset_name
from utils import extract_number
from utils import format_number


class TestUtilsMethods(unittest.TestCase):

    def test_format_number(self):
        self.assertEqual(format_number(7600.0000), '7600')
        self.assertEqual(format_number(5.8523), '5,85')

    def test_extract_number(self):
        self.assertEqual(extract_number('7600,0000 POINTS'), '7600')
        self.assertEqual(extract_number('7800,00 Points'), '7800')
        self.assertEqual(extract_number('13,0000 EUR'), '13')
        self.assertEqual(extract_number('22,50 EUR'), '22,50')
        self.assertEqual(extract_number('7,5000'), '7,50')

    def test_clean_asset_name(self):
        self.assertEqual(clean_asset_name('TotalEnergies SE'), 'TotalEnergies')
        self.assertEqual(clean_asset_name('Sanofi SA'), 'Sanofi')
        self.assertEqual(clean_asset_name('Carrefour S.A.'), 'Carrefour')
        self.assertEqual(clean_asset_name('STMicroelectronics N.V.'),
                         'STMicroelectronics')
        self.assertEqual(clean_asset_name('CAC 40®'), 'CAC 40')

    def test_to_number(self):
        self.assertEqual(to_number('12892,886214'), 12892.89)
        self.assertEqual(to_number('162,12'), 162.12)
        self.assertEqual(to_number('135,0000'), 135)
        self.assertEqual(to_number('13000'), 13000)
        self.assertEqual(to_number('-'), 0)


if __name__ == '__main__':
    unittest.main()
