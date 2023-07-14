"""
Implements the functions described in:
https://blksail-edu.github.io/docs/module/physics
Eben Quenneville
7/13/2023
"""
import numpy as np

density_water = 1000 # kg/m^3
gravity = 9.81 # m/s^2, change if you are in space

def calculate_buoyancy(volume: float, density_fluid: float) -> float:
    """
    Calculates the buoyancy force on a object in a fluid.

    Arguments:
        volume: float, the volume of the object in cubic meters
        density_fluid: float, the density of the fluid in kg/m^3
    Returns:
        float: buoyancy force in Newtons
    """
    if volume <= 0:
        raise ValueError("Volume is negative.")
    if density_fluid <= 0:
        raise ValueError("Density is negative.")
    
    buoyancy = density_fluid * volume * gravity
    return buoyancy

def will_it_float(volume: float, mass: float) -> bool:
    """
    Calculates whether or not a object will float in water

    Arguments:
        volume: float, the volume of the object in m^3
        mass: float, the mass of the object in kg
    Returns:
        bool: True if the object will float, False if it will sink
    """
    if (volume <= 0):
        raise ValueError("Volume or mass is negative.")
    if (mass <= 0):
        raise ValueError("Volume or mass is negative.")
    
    buoyancy_force = calculate_buoyancy(volume, density_water)
    gravity_force = mass * gravity
    if buoyancy_force == gravity_force:
        return None
    
    if buoyancy_force > gravity_force:
        return True
    elif buoyancy_force < gravity_force:
        return False
    else:
        return None

def calculate_pressure(depth: float) -> float:
    """
    Calculates the pressure on an object at a given depth.
    Assumes that positive depth means further under the water.

    Arguments:
        depth: float, the depth in meters
    Returns:
        float: pressure in Pascals
    """
    pressure_at_surface = 101325
    if depth < 0:
        raise Exception("Depth is negative. This function assumes depth is positive below the surface.")
    
    pressure = density_water * gravity * depth
    return pressure + pressure_at_surface

def calculate_acceleration(force: float, mass: float) -> float:
    """
    Calculates the acceleration on the object given force and mass.
    Arguments:
        force: float, the force, in Newtons
        mass: float, the mass of the object, in kg
    Returns:
        float: the acceleration in m/s^2
    """
    if mass <= 0:
        raise ValueError("Mass is negative.")
    acceleration = force / mass
    return acceleration

def calculate_angular_acceleration(torque: float, moment_of_inertia: float) -> float:
    """
    Calculates the angular acceleration on the object given the torque and moment of inertia.
    Arguments:
        torque: float, the torque applied in Newton meters
        moment_of_inertia: float, the moment of inertia of the object in kg * m^2
    Returns:
        float: the angular acceleration in radians per second squared
    """
    if moment_of_inertia <= 0: 
        raise ValueError("Moment of inertia is less than or equal to 0.")

    angular_acceleration = torque / moment_of_inertia
    return angular_acceleration

def calculate_torque(force_magnitude: float, force_direction: float, moment_arm: float) -> float:
    """
    Calculates the torque applied to an object given the force applied to it and the distance from the axis of rotation.
    Arguments:
        force_magnitude: float, the magnitude of the force applied to the object in Newtons
        force_direction: float, the direction of the force applied to the object in degrees
        moment_arm: float, the distance from the axis of rotation to the point where the force is applied in meters
    Returns:
        float: the torque in Newton-meters
    """
    torque = force_magnitude * np.sin(force_direction * np.pi / 180) * moment_arm
    return torque

def calculate_moment_of_inertia(mass: float, distance: float) -> float:
    """
    Calculates the moment of inertia of an object given mass and distance from the center of mass to axis of rotation.
    Arguments:
        mass: the mass of the object in kg
        distance: the distance from the axis of rotation to the center of mass of the object in meters
    Returns:
        float: the moment of inertia of the object
    """
    if mass <= 0:
        raise ValueError("Mass is less than or equal to 0.")
    
    moment_of_inertia = mass * distance**2
    return moment_of_inertia

def calculate_auv_acceleration(force_magnitude: float, force_angle: float, mass: float = 100, volume: float = 0.1, thruster_distance: float = 0.5) -> float:
    """
    Calculates the acceleration of the AUV in the 2D plane.
    Arguments:
        force_magnitude: float, the magnitude of the force in Newtons
        force_angle: float, the angle of the force applied by the thruster in radians, measured from the x-axis
        mass (optional, default 100): float, the mass of the AUV in kg
        volume (optional, default 0.1): float, the volume of the AUV
        thruster_distance (optional, default 0.5): float, the distance from the center of mass to the thruster in meters.
    Returns:
        float or None: the acceleration in m/s^2, or None if there is an error
    """
    if force_magnitude > 100:
        raise ValueError("The thruster should only apply a force up to 100N.")
    
    try:
        acceleration_x = calculate_acceleration((force_magnitude * np.cos(force_angle)), mass)
        acceleration_y = calculate_acceleration((force_magnitude * np.sin(force_angle)), mass)
        return np.array([acceleration_x, acceleration_y])
    except Exception as e:
        print("There is an exception when calling calculate_acceleration.")
        return None

def calculate_auv_angular_acceleration(force_magnitude: float, force_direction: float, moment_of_inertia: float = 1, thruster_distance: float = 0.5) -> float:
    """
    Calculates the angular acceleration of the AUV in radians / s^2
    Arguments:
        force_magnitude: float, the magnitude of the force in Newtons
        force_direction: float, the angle of the force applied by the thruster in radians, measured from the x-axis
        moment_of_inertia: float = 1, the moment of inertia of the AUV in kg / m^2
        thruster_distance: float = 0.5, the distance from the center of mass of the AUV to the thruster in meters.
    Returns:
        float or None: the angular acceleration in rads / s^2, None if there is an error
    """
    if moment_of_inertia <= 0: 
        raise ValueError("Moment of inertia is less than or equal to 0.")
    
    try:
        torque = calculate_torque(force_magnitude, force_direction, thruster_distance)
        angular_acceleration = calculate_angular_acceleration(torque, moment_of_inertia)
        return angular_acceleration
    except Exception as e:
        print("There is an exception from calculating the angular acceleration. Check the inputs.")
        return None

def calculate_auv2_acceleration(thrusters: np.ndarray, alpha: float, mass: float = 100) -> float:
    """
    Calculates the acceleration of the AUV in the 2D plane given an array of thrusters.
    Arguments:
        thrusters: np.ndarray,  the magnitudes of the forces applied by the thrusters in Newtons
        alpha: float, the angle of the thrusters in radians.
        mass: float = 100: the mass of the AUV in kilograms. The default value is 100kg.
    Returns:
        float, acceleration of the AUV
    """
    projection_matrix = np.ndarray([
        [np.cos(alpha), np.cos(alpha), -np.cos(alpha), -np.cos(alpha)], 
        [np.sin(alpha), -np.sin(alpha), -np.sin(alpha), np.sin(alpha)]])
    (force_x, force_y) = projection_matrix.matmul(thrusters)
    print(force_x, force_y)
    acceleration = np.ndarray([
        calculate_acceleration(force_x, mass), 
        calculate_acceleration(force_y, mass)])
    return acceleration