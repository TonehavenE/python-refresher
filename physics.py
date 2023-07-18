"""
Implements the functions described in:
https://blksail-edu.github.io/docs/module/physics
Eben Quenneville
7/13/2023
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

density_water = 1000  # kg/m^3
gravity = 9.81  # m/s^2, change if you are in space


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
    if volume <= 0:
        raise ValueError("Volume is less than or equal to 0.")
    if mass <= 0:
        raise ValueError("Mass is less than or equal to 0.")

    buoyancy_force = calculate_buoyancy(volume, density_water)
    gravity_force = mass * gravity
    if buoyancy_force == gravity_force:
        return None
    else:
        return buoyancy_force > gravity_force


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
        raise Exception(
            "Depth is negative. This function assumes depth is positive below the surface."
        )

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
        raise ValueError("Mass is less than or equal to 0.")
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


def calculate_torque(
    force_magnitude: float, force_direction: float, moment_arm: float
) -> float:
    """
    Calculates the torque applied to an object given the force applied to it and the distance from the axis of rotation.
    Arguments:
        force_magnitude: float, the magnitude of the force applied to the object in Newtons. Errors if magnitude is less than or equal to 0.
        force_direction: float, the direction of the force applied to the object in degrees
        moment_arm: float, the distance from the axis of rotation to the point where the force is applied in meters
    Returns:
        float: the torque in Newton-meters.
    """
    if force_magnitude <= 0:
        raise ValueError("Force magnitude is less than or 0.")
    if moment_arm <= 0:
        raise ValueError("Moment arm is less than or equal to 0.")
    torque = force_magnitude * np.sin(np.deg2rad(force_direction)) * moment_arm
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

    moment_of_inertia = mass * np.power(distance, 2)
    return moment_of_inertia


def calculate_auv_acceleration(
    force_magnitude: float,
    force_angle: float,
    mass: float = 100,
    volume: float = 0.1,
    thruster_distance: float = 0.5,
) -> np.ndarray:
    """
    Calculates the acceleration of the AUV in the 2D plane of the vehicle.
    Arguments:
        force_magnitude: float, the magnitude of the force in Newtons
        force_angle: float, the angle of the force applied by the thruster in radians, measured from the x-axis
        mass (optional, default 100): float, the mass of the AUV in kg
        volume (optional, default 0.1): float, the volume of the AUV
        thruster_distance (optional, default 0.5): float, the distance from the center of mass to the thruster in meters.
    Returns:
        np.ndarray: the acceleration in m/s^2, or None if there is an error
    """
    if mass <= 0:
        raise ValueError("Mass is less than or equal to 0.")

    acceleration_x = calculate_acceleration(force_magnitude * np.cos(force_angle), mass)
    acceleration_y = calculate_acceleration(force_magnitude * np.sin(force_angle), mass)
    return np.array([acceleration_x, acceleration_y])


def calculate_auv_angular_acceleration(
    force_magnitude: float,
    force_direction: float,
    moment_of_inertia: float = 1,
    thruster_distance: float = 0.5,
) -> float:
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

    if thruster_distance < 0:
        raise ValueError("The thruster distance is negative.")

    torque = calculate_torque(
        force_magnitude, np.rad2deg(force_direction), thruster_distance
    )
    angular_acceleration = calculate_angular_acceleration(torque, moment_of_inertia)
    return angular_acceleration


def calculate_auv2_acceleration(
    thrusters: np.ndarray, alpha: float, theta: float, mass: float = 100
) -> np.ndarray:
    """
    Calculates the acceleration of the AUV in the 2D plane given an array of thrusters.
    Arguments:
        thrusters: np.ndarray, the magnitudes of the forces applied by the thrusters in Newtons. e.g. np.array([10, 10, 10, 10])
        alpha: float, the angle of the thrusters in radians.
        theta: float, the angle of the AUV
        mass: float = 100: the mass of the AUV in kilograms. The default value is 100kg.
    Returns:
        np.ndarray, acceleration of the AUV
    """
    if mass <= 0:
        raise ValueError("Mass is less than or equal to 0.")

    if type(thrusters) != np.ndarray:
        raise TypeError("Thrusters is not a Numpy array.")

    if np.shape(thrusters) != (4,):
        raise ValueError("The shape of the thrusters vector is incorrect.")

    # Matrix to project the thrust vectors onto the relative X and Y plane of the AUV
    projection_matrix = np.array(
        [
            [np.cos(alpha), np.cos(alpha), -np.cos(alpha), -np.cos(alpha)],
            [np.sin(alpha), -np.sin(alpha), -np.sin(alpha), np.sin(alpha)],
        ]
    )

    projected_forces = np.matmul(projection_matrix, thrusters)
    # Rotation matrix to project the total force vectors on to the global X and Y axis
    rotation_matrix = np.array(
        [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
    )
    force = np.matmul(rotation_matrix, projected_forces)
    # Convert force into acceleration
    acceleration = calculate_acceleration(force, mass)
    return acceleration


def calculate_auv2_angular_acceleration(
    thrusters: np.ndarray,
    alpha: float,
    horizontal_distance: float,
    vertical_distance: float,
    moment_of_inertia: float = 100,
):
    """
    Calculates the angular acceleration of the AUV.

    Arguments:
        thrusters: float, an array of the magnitudes of the forces in Newtons
        alpha: float, the angle of the thrusters
        horizontal_distance: float, the horizontal distance from the center of mass of the AUV to the thrusters, in meters
        vertical_distance: float, the vertical distance from the center of mass of the AUV to the thrusters, in meters
        moment_of_inertia: float=100, the moment of inertia of the AUV in kg * m^2

    Returns:
        float: the angular acceleration of the AUV in rads/s^2
    """
    if vertical_distance <= 0 or horizontal_distance <= 0:
        raise ValueError("Horizontal or vertical distance is less than or equal to 0.")
    if moment_of_inertia <= 0:
        raise ValueError("Moment of inertia is less than or equal to 0.")
    if type(thrusters) != np.ndarray:
        raise TypeError("Thrusters is not a Numpy array.")
    if np.shape(thrusters) != (4,):
        raise ValueError("The shape of the thrusters vector is incorrect.")

    moment_arm = np.sqrt(
        np.power(horizontal_distance, 2) + np.power(vertical_distance, 2)
    )

    beta = np.arctan(vertical_distance / horizontal_distance)
    # alpha + beta is the angle from the vector to the moment arm
    total_angle = alpha + beta

    projection_array = (
        np.array(
            [
                np.sin(total_angle),
                -np.sin(total_angle),
                np.sin(total_angle),
                -np.sin(total_angle),
            ]
        )
        * moment_arm
    )

    torques = np.matmul(projection_array, thrusters)  # Calculate each torque
    total_torque = np.sum(torques)  # Sum the torque
    angular_acceleration = calculate_angular_acceleration(
        total_torque, moment_of_inertia
    )
    return angular_acceleration


def simulate_auv2_motion(
    thrusters: np.ndarray,
    alpha: float,
    horizontal_distance: float,
    vertical_distance: float,
    moment_of_inertia: float = 100,
    mass: float = 100,
    time_step: float = 0.1,
    time_final: float = 10,
    initial_x: float = 0,
    initial_y: float = 0,
    initial_theta: float = 0,
):
    """
    Simulates the motion of an AUV in the 2D plane.
    Arguments:
        thrusters: np.ndarray, an array of the magnitudes of the forces applied by the thrusters in Newtons
        alpha: float, the angle of the thrusters in radians
        horizontal_distance: float, the horizontal distance to the thrusters in meters
        vertical_distance: float, the vertical distance to the thrusters in meters
        moment_of_inertia: float = 100, the moment of inertia of the AUV in kg * m^2
        time_step: float = 0.1, the time step of the simulation in seconds
        time_final: float = 10, the final time of the simulation in seconds
        initial_x: float = 0, the initial x position of the simulation in meters
        initial_y: float = 0, the initial y position of the simulation in meters
        initial_theta: float = 0, the initial angle of the AUV in radians
    Returns a tuple with the following elements:
        times: np.ndarray, the time steps of the simulation in seconds.
        x_array: np.ndarray, the x-positions of the AUV in meters.
        y_array: np.ndarray, the y-positions of the AUV in meters.
        theta_array: np.ndarray, the angles of the AUV in radians.
        velocity_array: np.ndarray, the velocities of the AUV in meters per second.
        angular_velocity_array: np.ndarray, the angular velocities of the AUV in radians per second.
        acceleration_array: np.ndarray, the accelerations of the AUV in meters per second squared.
    """
    if type(thrusters) != np.ndarray:
        raise TypeError("Thrusters is not a Numpy array.")
    if np.shape(thrusters) != (4,):
        raise ValueError("The shape of the thrusters vector is incorrect.")
    times = np.arange(0, time_final, time_step)
    x_array = np.zeros_like(times)
    x_array[0] = initial_x
    y_array = np.zeros_like(times)
    y_array[0] = initial_y
    theta_array = np.zeros_like(times)
    theta_array[0] = initial_theta
    velocity_array = np.zeros(
        shape=(len(times), 2)
    )  # np.arange(np.array([0, 0]), time_final, time_step)
    acceleration_array = np.zeros(
        shape=(len(times), 2)
    )  # np.arange(np.array([0, 0]), time_final, time_step)
    angular_acceleration_array = np.zeros_like(times)
    angular_velocity_array = np.zeros_like(times)

    # Simulation Loop
    for i in range(1, len(times)):
        acceleration_array[i] = calculate_auv2_acceleration(
            thrusters, alpha, theta_array[i], mass
        )
        velocity_array[i] = velocity_array[i - 1] + acceleration_array[i] * time_step
        x_array[i] = x_array[i - 1] + velocity_array[i][0] * time_step
        y_array[i] = y_array[i - 1] + velocity_array[i][1] * time_step
        angular_acceleration_array[i] = calculate_auv2_angular_acceleration(
            thrusters, alpha, horizontal_distance, vertical_distance, moment_of_inertia
        )
        angular_velocity_array[i] = (
            angular_velocity_array[i - 1] + angular_acceleration_array[i] * time_step
        )
        theta_array[i] = np.mod(
            theta_array[i - 1] + angular_velocity_array[i] * time_step, np.pi * 2
        )

    output_tuple = (
        times,
        x_array,
        y_array,
        theta_array,
        velocity_array,
        angular_velocity_array,
        acceleration_array,
    )
    return output_tuple


def plot_auv2_motion(
    times: np.ndarray,
    x_array: np.ndarray,
    y_array: np.ndarray,
    theta_array: np.ndarray,
    velocity_array: np.ndarray,
    angular_velocity_array: np.ndarray,
    acceleration_array: np.ndarray,
):
    plt.plot(times, x_array, label="X Positions")
    plt.plot(times, y_array, label="Y Positions")
    plt.plot(times, theta_array, label="Theta")
    velocity_x = np.zeros_like(times)
    velocity_y = np.zeros_like(times)
    acceleration_x = np.zeros_like(times)
    acceleration_y = np.zeros_like(times)
    for i in range(0, len(times)):
        velocity_x[i] = velocity_array[i][0]
        velocity_y[i] = velocity_array[i][1]
        acceleration_x[i] = acceleration_array[i][0]
        acceleration_y[i] = acceleration_array[i][1]
    plt.plot(times, velocity_x, label="X Velocity")
    plt.plot(times, velocity_y, label="Y Velocity")
    plt.plot(times, acceleration_x, label="X Acceleration")
    plt.plot(times, acceleration_y, label="Y Acceleration")
    plt.plot(times, angular_velocity_array, label="Angular Velocity")

    plt.xlabel("Time (s)")
    plt.ylabel("Variables")
    plt.legend()
    plt.show()


def plot_auv2_motion_individual(
    times: np.ndarray,
    x_array: np.ndarray,
    y_array: np.ndarray,
    theta_array: np.ndarray,
    velocity_array: np.ndarray,
    angular_velocity_array: np.ndarray,
    acceleration_array: np.ndarray,
    title: str,
):
    plt.style.use("dark_background")
    figure, axs = plt.subplots(2, 4, figsize=(15, 15))
    axs[0, 0].plot(times, x_array)
    axs[0, 0].set_title("X Position")
    axs[0, 0].set_ylabel("m")

    axs[0, 1].plot(times, y_array)
    axs[0, 1].set_title("Y Position")
    axs[0, 1].set_ylabel("m")

    axs[0, 2].plot(times, theta_array)
    axs[0, 2].set_title("Angle")
    axs[0, 2].set_ylabel("rad")

    axs[0, 3].plot(times, velocity_array[:, 0])
    axs[0, 3].set_title("X Velocity")
    axs[0, 3].set_ylabel("m/s")

    axs[1, 0].plot(times, velocity_array[:, 1])
    axs[1, 0].set_title("Y Velocity")
    axs[1, 0].set_ylabel("m/s")

    axs[1, 1].plot(times, angular_velocity_array)
    axs[1, 1].set_title("Angular Velocity")
    axs[1, 1].set_ylabel("rad/s")

    axs[1, 2].plot(times, acceleration_array[:, 0])
    axs[1, 2].set_title("X Acceleration")
    axs[1, 2].set_ylabel("m/s^2")

    axs[1, 3].plot(times, acceleration_array[:, 1])
    axs[1, 3].set_title("Y Acceleration")
    axs[1, 3].set_ylabel("m/s^2")

    figure.tight_layout()
    figure.suptitle(title)

    plt.show()


def plot_auv2_motion_animated(times: np.ndarray, x: np.ndarray, y: np.ndarray):
    (x_max, x_min) = (np.max(x), np.min(x))
    (y_max, y_min) = (np.max(y), np.min(y))

    # Setting up Data Set for Animation
    dataSet = np.array([x, y])  # Combining our position coordinates
    numDataPoints = len(times)

    def animate_func(num):
        ax.clear()  # Clears the figure to update the line, point,
        # title, and axes
        # Updating Trajectory Line (num+1 due to Python indexing)
        ax.plot(dataSet[0, : num + 1], dataSet[1, : num + 1], c="blue")
        # Updating Point Location
        ax.scatter(dataSet[0, num], dataSet[1, num], c="blue", marker="o")
        # Adding Constant Origin
        ax.plot(dataSet[0, 0], dataSet[1, 0], c="black", marker="o")
        ax.set_xlim([x_min, x_max])
        ax.set_ylim([y_min, y_max])

        # Adding Figure Labels
        ax.set_title(
            "Trajectory \nTime = " + str(np.round(times[num], decimals=2)) + " sec"
        )
        ax.set_xlabel("x")
        ax.set_ylabel("y")

    # Plotting the Animation
    fig = plt.figure()
    ax = plt.axes()
    line_ani = animation.FuncAnimation(
        fig, animate_func, interval=100, frames=numDataPoints
    )

    f = r"./animated_motion.gif"
    writergif = animation.PillowWriter(fps=numDataPoints / 6)
    line_ani.save(f, writer=writergif)
