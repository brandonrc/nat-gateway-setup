import unittest
from dnsmasq import time_check

class TestDNSMasq(unittest.TestCase):

    def test_time_check_valid(self):
        self.assertEqual(time_check("12m"), "12m")
        self.assertEqual(time_check("12h"), "12h")

    def test_time_check_invalid_format(self):
        with self.assertRaises(ValueError):
            time_check("12s")
            time_check("12")
            time_check("m12")

    def test_time_check_invalid_value(self):
        with self.assertRaises(ValueError):
            time_check("0m")
            time_check("0h")
            time_check("-12m")
            time_check("-12h")

    def test_time_check_leading_zeros(self):
        with self.assertRaises(ValueError):
            time_check("00m")
            time_check("00h")

if __name__ == "__main__":
    unittest.main()
