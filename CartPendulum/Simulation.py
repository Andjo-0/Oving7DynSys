from ecospy import EcosSimulation, EcosSimulationStructure
from ecospy.plotter import Plotter, TimeSeriesConfig
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
    ss = EcosSimulationStructure()
    ss.add_model("cart", "Cart.fmu")
    ss.add_model("pendulum", "Pendulum.fmu")
    ss.add_model("regulator", "Regulator.fmu")

    # Connections
    ss.make_real_connection("cart::position", "regulator::position")
    ss.make_real_connection("cart::velocity", "regulator::velocity")
    ss.make_real_connection("pendulum::angle", "regulator::angle")
    ss.make_real_connection("pendulum::angular_velocity", "regulator::angular_velocity")

    ss.make_real_connection("regulator::force", "cart::force")
    ss.make_real_connection("cart::acceleration", "pendulum::cart_acceleration")
    ss.make_real_connection("pendulum::force", "cart::force_pendulum")

    # Parameter set
    params = {
        "cart::initial_position": 0.0,
        "cart::initial_velocity": 0.0,
        "cart::mass": 1.0,
        "cart::mass_pendulum": 0.1,
        "cart::length_pendulum": 1.0,
        "pendulum::initial_angle": 20*np.pi/180,
        "pendulum::initial_angular_velocity": 0.0,
        "pendulum::mass": 0.1,
        "pendulum::length": 1.0,

        "regulator::k1": -15.0,
        "regulator::k2": -15.0,
        "regulator::k3": -30.0,
        "regulator::k4": -10.0,

    }
    ss.add_parameter_set("initialValues", params)

    result_file = "results.csv"

    with EcosSimulation(structure=ss, step_size=1/100) as sim:
        sim.add_csv_writer(result_file)
        sim.init(parameter_set="initialValues")
        sim.step_until(30)
        sim.terminate()

    configPosition = TimeSeriesConfig(

        title="Cart-Pendulum-Regulator System",
        y_label="Position ",
        identifiers=["cart::position"]

    )

    configAngle = TimeSeriesConfig(

        title="Cart-Pendulum-Regulator System",
        y_label="Angle [m / rad]",
        identifiers=["pendulum::angle"]

    )

    plotter = Plotter(result_file, configPosition)
    plotter.show()

    plotter = Plotter(result_file, configAngle)
    plotter.show()