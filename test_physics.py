"""
Unit Test cases for physics.py
Eben Quenneville
7/13/2023
"""
import unittest
import physics

class TestPhysics(unittest.TestCase):
    def test_calculate_buoyancy(self):
        self.assertNotEqual(physics.calculate_buoyancy(1, 1000), 0)
        self.assertEqual(physics.calculate_buoyancy(0.1, 1000), 981)
        self.assertRaises(TypeError, physics.calculate_buoyancy, "foo", "bar")
        self.assertRaises(ValueError, physics.calculate_buoyancy, -100, 1000)


    def test_will_it_float(self):
         self.assertEqual(physics.will_it_float(0.1, 50), True)
         self.assertEqual(physics.will_it_float(0.1, 100), None)
         self.assertNotEqual(physics.will_it_float(0.1, 1000), True)
         self.assertRaises(TypeError, physics.will_it_float, "0.1", "100")
         self.assertRaises(ValueError, physics.will_it_float, -0.1, 100)
         


    def test_calculate_pressure(self):
        self.assertEqual(physics.calculate_pressure(10), 98100)
        self.assertNotEqual(physics.calculate_pressure(100), 0)
        self.assertRaises(TypeError, physics.calculate_pressure, "foo")
        self.assertRaises(Exception, physics.calculate_pressure, -100)

if __name__ == "__main__":
    unittest.main()