"""
Implements the functions described in:
https://blksail-edu.github.io/docs/module/physics
Eben Quenneville
7/13/2023
"""
def calculate_buoyancy(V: float, density_fluid: float) -> float:
    """
    Arguments:
        V: float, the volume of the object in cubic meters
        density_fluid: float, the density of the fluid in kg/m^3
    Returns:
        float: buoyancy force in Newtons
    """
    if (V < 0 or density_fluid < 0):
        raise ValueError("Volume or density is negative.")
    gravity = 9.81 # m/s^2, adjust if you are in space
    buoyancy = density_fluid * V * gravity
    return buoyancy

def will_it_float(V: float, mass: float) -> bool:
    """
    Arguments:
        V: float, the volume of the object in m^3
        mass: float, the mass of the object in kg
    Returns:
        bool: True if the object will float, False if it will sink
    """
    if (V < 0 or mass < 0):
        raise ValueError("Volume or mass is negative.")
    density_water = 1000 # kg/m^3
    gravity = 9.81 # m/s^2
    buoyancy_force = calculate_buoyancy(V, density_water)
    gravity_force = mass * gravity
    if buoyancy_force > gravity_force:
        return True
    elif buoyancy_force == gravity_force:
        return None
    else:
        return False

def calculate_pressure(depth: float) -> float:
    """
    Arguments:
        depth: float, the depth in meters
    Returns:
        float: pressure in Pascals
    """
    if depth < 0:
        raise Exception("Depth is negative. This function assumes depth is positive below the surface.")
    density_water = 1000 # kg/m^3
    gravity = 9.81 # m/s^2
    pressure = density_water * gravity * depth
    return pressure
