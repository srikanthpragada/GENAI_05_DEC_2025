import unittest
from nums import isprime


class TestIsPrime(unittest.TestCase):
    def test_small_primes(self):
        for n in [2, 3, 5, 7, 11, 13]:
            self.assertTrue(isprime(n), f"{n} should be prime")

    def test_small_nonprimes(self):
        for n in [0, 1, 4, 6, 8, 9, 10, 12]:
            self.assertFalse(isprime(n), f"{n} should not be prime")

    def test_negative_numbers(self):
        for n in [-1, -2, -7, -10]:
            self.assertFalse(isprime(n), f"{n} should not be prime")

    def test_large_prime(self):
        self.assertTrue(isprime(97), "97 should be prime")

    def test_large_nonprime(self):
        self.assertFalse(isprime(100), "100 should not be prime")


if __name__ == "__main__":
    unittest.main()
