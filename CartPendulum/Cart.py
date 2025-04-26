from pythonfmu import Fmi2Slave, Real, Fmi2Causality
import numpy as np

class Cart(Fmi2Slave):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Physical parameters
        self.initial_position = 0.0
        self.initial_velocity = 0.0
        self.mass = 1.0
        self.mass_pendulum = 0.1
        self.length_pendulum = 1.0  # pendulum length for force calculation


        # State variables
        self.position = 0.0
        self.velocity = 0.0
        self.force = 0.0           # input from regulator
        self.force_pendulum = 0.0  # reaction force computed here
        self.acceleration = 0.0

        # Pendulum inputs
        self.angle = 0.0
        self.angular_velocity = 0.0
        self.angular_acceleration = 0.0
        self.force_pendulum = 0.0

        # Register parameters
        self.register_variable(Real("mass", causality=Fmi2Causality.parameter))
        self.register_variable(Real("mass_pendulum", causality=Fmi2Causality.parameter))
        self.register_variable(Real("length_pendulum", causality=Fmi2Causality.parameter))
        self.register_variable(Real("initial_position", causality=Fmi2Causality.parameter))
        self.register_variable(Real("initial_velocity", causality=Fmi2Causality.parameter))

        # Register outputs
        self.register_variable(Real("position", causality=Fmi2Causality.output, getter=lambda: self.position))
        self.register_variable(Real("velocity", causality=Fmi2Causality.output, getter=lambda: self.velocity))
        self.register_variable(Real("acceleration", causality=Fmi2Causality.output, getter=lambda: self.acceleration))

        # Register inputs
        self.register_variable(Real("force_pendulum", causality=Fmi2Causality.input, setter=lambda x: setattr(self, "force_pendulum", x)))
        self.register_variable(Real("force", causality=Fmi2Causality.input, setter=lambda x: setattr(self, "force", x)))

    def exit_initialization_mode(self):
        self.position = self.initial_position
        self.velocity = self.initial_velocity

    def do_step(self, t, dt):

        # Total force on cart
        total_force = self.force + self.force_pendulum
        self.acceleration = total_force / (self.mass + self.mass_pendulum)

        #
        self.velocity = self.acceleration * dt
        self.position = self.velocity * dt

        return True