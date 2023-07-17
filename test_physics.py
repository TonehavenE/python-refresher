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
        self.assertEqual(physics.calculate_pressure(10), 199425)
        self.assertNotEqual(physics.calculate_pressure(11), 199425)
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
        self.assertTrue(
            np.allclose(physics.calculate_auv_acceleration(10, 0), np.array([0.1, 0]))
        )
        self.assertTrue(
            np.allclose(
                physics.calculate_auv_acceleration(10, np.pi / 2), np.array([0, 0.1])
            )
        )
        self.assertFalse(
            np.allclose(
                physics.calculate_auv_acceleration(10, np.pi / 3), np.array([0, 0.1])
            )
        )

    def test_calculate_angular_acceleration(self):
        # Test for expected output
        self.assertEqual(physics.calculate_auv_angular_acceleration(100, np.pi / 2), 50)
        # Confirm we don't always get 50
        self.assertNotEqual(
            physics.calculate_auv_angular_acceleration(1000, np.pi / 2), 50
        )
        # Negative moment of inertia should raise an error
        with self.assertRaises(ValueError):
            physics.calculate_auv_angular_acceleration(1000, np.pi / 2, -10, 1)

    def test_calculate_auv2_acceleration(self):
        # 0 forces should result in no acceleration
        self.assertTrue(
            np.allclose(
                physics.calculate_auv2_acceleration(
                    np.array([0, 0, 0, 0]), np.pi / 4, 0.0
                ),
                np.array([0, 0]),
            )
        )
        # Equivalent forces should cancel out
        self.assertTrue(
            np.allclose(
                physics.calculate_auv2_acceleration(
                    np.array([10, 10, 10, 10]), np.pi / 4, 0.0
                ),
                np.array([0, 0]),
            )
        )
        # If F1 and F2 are positive and equal, then the object should only accelerate in X
        self.assertTrue(
            np.allclose(
                physics.calculate_auv2_acceleration(
                    np.array([10, 10, 0, 0]), np.pi / 4, 0.0
                ),
                np.array([0.141422, 0]),
            )
        )
        # if alpha is pi/2 rads, then all acceleration should be vertical
        self.assertTrue(
            np.allclose(
                physics.calculate_auv2_acceleration(
                    np.array([10, 0, 0, 10]), np.pi / 2, 0
                ),
                np.array([0, 0.2]),
            )
        )
        # if all relative acceleration is vertical but theta is pi/2, then all acceleration should become -X
        self.assertTrue(
            np.allclose(
                physics.calculate_auv2_acceleration(
                    np.array([10, 0, 0, 10]), np.pi / 2, np.pi / 2
                ),
                np.array([-0.2, 0]),
            )
        )
        # if theta is not pi/2, then all relative Y-acceleration should not become -X
        self.assertFalse(
            np.allclose(
                physics.calculate_auv2_acceleration(
                    np.array([10, 0, 0, 10]), np.pi / 3, np.pi / 2
                ),
                np.array([-0.2, 0]),
            )
        )

        # Check that negative mass or incorrect np.array throws an error
        with self.assertRaises(ValueError):
            physics.calculate_auv2_acceleration(np.array([0, 0, 0, 0]), 45, 0, -100)
            physics.calculate_auv2_acceleration(np.array([[], []]), 45, 0)
            physics.calculate_auv2_acceleration([], 45, 0)

    def test_calculate_auv2_angular_acceleration(self):
        # No force should have no torque
        self.assertEqual(
            physics.calculate_auv2_angular_acceleration(
                np.array([0, 0, 0, 0]), 0, 1, 1
            ),
            0,
        )
        # If all of the force is perpendicular, than it should all be torque
        self.assertAlmostEqual(
            physics.calculate_auv2_angular_acceleration(
                np.array([10, 0, 0, 0]), np.pi / 2, 1, 1
            ),
            0.1,
        )
        # Equal forces should cancel out
        self.assertEqual(
            physics.calculate_auv2_angular_acceleration(
                np.array([10, 10, 10, 10]), np.pi / 4, 1, 1
            ),
            0,
        )
        # Unequal forces should create some torque
        self.assertNotEqual(
            physics.calculate_auv2_angular_acceleration(
                np.array([15, 10, 14, 10]), np.pi / 4, 1, 1
            ),
            0,
        )
        # Sample case: only T1 is active, exerting a force of 10 Newtons at an angle alpha of pi / 4 with a moment arm of sqrt(2)
        self.assertAlmostEqual(
            physics.calculate_auv2_angular_acceleration(
                np.array([10, 0, 0, 0]), np.pi / 4, 1, 1
            ),
            0.14142135623,
        )
        # Check that negative distances, and moment of inertia throw errors
        with self.assertRaises(ValueError):
            physics.calculate_auv2_angular_acceleration(
                np.array([0, 0, 0, 0]), 45, -10, 10
            )
            physics.calculate_auv2_angular_acceleration(
                np.array([0, 0, 0, 0]), 45, 10, -10
            )
            physics.calculate_auv2_angular_acceleration(
                np.array([0, 0, 0, 0]), 45, 10, 10, -100
            )
            physics.calculate_auv2_angular_acceleration(np.array([[], []]), 45, 10, 10)
            physics.calculate_auv2_angular_acceleration([], 45, 10, 10)

    def test_simulate_auv2_motion(self):
        (times, x, y, theta, v, omega, a) = physics.simulate_auv2_motion(
            [0, 0, 0, 0], 45, 1, 1, 100, 100, 0.1, 0.3, 0, 0, 0
        )
        self.assertTrue(np.allclose(times, np.array([0, 0.1, 0.2])))


if __name__ == "__main__":
    unittest.main()
