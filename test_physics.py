"""
Unit Test cases for physics.py
Eben Quenneville
7/13/2023
"""
import unittest
import physics
import numpy as np

class TestPhysics(unittest.TestCase):
    def test_calculate_buoyancy(self):
        self.assertNotEqual(physics.calculate_buoyancy(1, 1000), 0)
        self.assertEqual(physics.calculate_buoyancy(0.1, 1000), 981)
        self.assertRaises(TypeError, physics.calculate_buoyancy, "foo", "bar")
        self.assertRaises(ValueError, physics.calculate_buoyancy, -100, 1000)
        self.assertRaises(ValueError, physics.calculate_buoyancy, 100, -1000)
        self.assertRaises(ValueError, physics.calculate_buoyancy, 100, 0)
        self.assertRaises(ValueError, physics.calculate_buoyancy, 0, 100)


    def test_will_it_float(self):
         self.assertEqual(physics.will_it_float(0.1, 50), True)
         self.assertEqual(physics.will_it_float(0.1, 1000), False)
         self.assertEqual(physics.will_it_float(0.1, 100), None)
         self.assertNotEqual(physics.will_it_float(0.1, 1000), True)
         self.assertRaises(TypeError, physics.will_it_float, "0.1", "100")
         self.assertRaises(ValueError, physics.will_it_float, -0.1, 100)
         self.assertRaises(ValueError, physics.will_it_float, 0.1, -100)
         self.assertRaises(ValueError, physics.will_it_float, 0.0, 100)
         self.assertRaises(ValueError, physics.will_it_float, 0.1, 0.0)
         


    def test_calculate_pressure(self):
        self.assertEqual(physics.calculate_pressure(10), 98100 + 101325)
        self.assertNotEqual(physics.calculate_pressure(11), 98100 + 101325)
        self.assertRaises(TypeError, physics.calculate_pressure, "foo")
        self.assertRaises(Exception, physics.calculate_pressure, -100)

    def test_calculate_acceleration(self):
        self.assertEqual(physics.calculate_acceleration(100, 10), 10)
        self.assertNotEqual(physics.calculate_acceleration(1000, 10), 10)
        self.assertRaises(ValueError, physics.calculate_acceleration, 100, 0)
        self.assertRaises(ValueError, physics.calculate_acceleration, 100, -10)

    def test_calculate_angular_acceleration(self):
        self.assertEqual(physics.calculate_angular_acceleration(10, 1), 10)
        self.assertnotEqual(physics.calculate_angular_acceleration(10, 10), 10)
        self.assertRaises(ValueError, physics.calculate_angular_acceleration, 100, 0)
        self.assertRaises(ValueError, physics.calculate_angular_acceleration, 100, -10)

    def test_calculate_torque(self):
        self.assertEqual(physics.calculate_torque(10, 0, 1), 0)
        self.assertNotEqual(physics.calculate_torque(10, 10, 1), 0)
        self.assertEqual(physics.calculate_torque(10, 90, 1), 10)
    
    def test_calculate_moment_of_inertia(self):
        self.assertEqual(physics.calculate_moment_of_inertia(10, 1), 10)
        self.assertNotEqual(physics.calculate_moment_of_inertia(10, 10), 10)
        self.assertRaises(ValueError, physics.calculate_moment_of_inertia, -100, 10)
        self.assertRaises(ValueError, physics.calculate_moment_of_inertia, 0, 10)

    def test_calculate_auv_acceleration(self):
        self.assertEqual(physics.calculate_auv_acceleration(10, 0), np.array([10, 0]))
        self.assertEqual(physics.calculate_auv_acceleration(10, np.pi / 2), np.array([0, 10]))
        self.assertNotEqual(physics.calculate_auv_acceleration(10, np.pi / 3), np.array([0, 10]))
        self.assertRaises(ValueError, physics.calculate_auv_acceleration, 101, 0)
        


if __name__ == "__main__":
    unittest.main()