"""
Implements the functions described in:
https://blksail-edu.github.io/docs/module/physics
Eben Quenneville
7/13/2023
"""

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
    if depth < 0:
        raise Exception("Depth is negative. This function assumes depth is positive below the surface.")
    
    pressure = density_water * gravity * depth
    return pressure
