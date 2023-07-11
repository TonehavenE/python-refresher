import unittest
import hello
import numpy as np


class TestHello(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello.hello(), "Hello, world!")

    def test_add(self):
        self.assertEqual(hello.add(1, 1), 2)
        self.assertEqual(hello.add(1, -1), 0)
        self.assertEqual(hello.add(1.5, 1.5), 3)

    def test_sub(self):
        self.assertEqual(hello.sub(2, 2), 0)
        self.assertEqual(hello.sub(2, -1), 3)
        self.assertEqual(hello.sub(1.5, 1.5), 0)

    def test_mul(self):
        self.assertEqual(hello.mul(3, 3), 9)
        self.assertEqual(hello.mul(2, -2), -4)
        self.assertEqual(hello.mul(0.5, 0.5), 0.25)

    def test_div(self):
        self.assertEqual(hello.div(1, 1), 1)
        self.assertEqual(hello.div(-1, 2), -0.5)
        self.assertRaises(ValueError, hello.div, 100, 0)

    def test_sqrt(self):
        self.assertEqual(hello.sqrt(4), 2)
        self.assertEqual(hello.sqrt(9.0), 3.0)
        self.assertEqual(np.isnan(hello.sqrt(-1)), True)

    def test_power(self):
        self.assertEqual(hello.power(1, 1), 1)
        self.assertEqual(hello.power(2.0, -1), 0.5)
        self.assertEqual(hello.power(3.0, 3), 27.0)

    def test_log(self):
        self.assertEqual(hello.log(1), 0)
        self.assertEqual(hello.log(np.e), 1)
        self.assertEqual(hello.log(0), -np.Inf)

    def test_exp(self):
        self.assertEqual(hello.exp(1), np.e)
        self.assertEqual(hello.exp(-np.Inf), 0)
        self.assertEqual(hello.exp(0), 1)

    def test_sin(self):
        self.assertEqual(hello.sin(0), 0)
        self.assertEqual(hello.sin(1), 0.8414709848078965)
        self.assertEqual(hello.sin(np.pi / 2), 1.0)

    def test_cos(self):
        self.assertEqual(hello.cos(0), 1)
        self.assertEqual(hello.cos(1), 0.5403023058681398)
        self.assertAlmostEqual(hello.cos(np.pi / 2), 0.0)

    def test_tan(self):
        self.assertEqual(hello.tan(0), 0)
        self.assertEqual(hello.tan(1), 1.5574077246549023)
        self.assertAlmostEqual(hello.tan(np.pi / 4), 1.0)

    def test_cot(self):
        self.assertEqual(hello.cot(0), float("inf"))
        self.assertEqual(hello.cot(1), 0.6420926159343306)
        self.assertAlmostEqual(hello.cot(np.pi / 2), 0)


if __name__ == "__main__":
    unittest.main()
