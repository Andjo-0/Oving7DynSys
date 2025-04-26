from pythonfmu import Fmi2Slave, Real, Fmi2Causality
import numpy as np

class Regulator(Fmi2Slave):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.force = 0.0
        self.k1 = 0.0
        self.k2 = 0.0
        self.k3 = 0.0
        self.k4 = 0.0

        self.angle = 0.0
        self.angular_velocity = 0.0
        self.position = 0.0
        self.velocity = 0.0

        # Register parameters
        self.register_variable(Real("k1", causality=Fmi2Causality.parameter))
        self.register_variable(Real("k2", causality=Fmi2Causality.parameter))
        self.register_variable(Real("k3", causality=Fmi2Causality.parameter))
        self.register_variable(Real("k4", causality=Fmi2Causality.parameter))

        # Register inputs
        self.register_variable(Real("angle", causality=Fmi2Causality.input, setter=lambda x: setattr(self, "angle", x)))
        self.register_variable(Real("angular_velocity", causality=Fmi2Causality.input, setter=lambda x: setattr(self, "angular_velocity", x)))
        self.register_variable(Real("position", causality=Fmi2Causality.input, setter=lambda x: setattr(self, "position", x)))
        self.register_variable(Real("velocity", causality=Fmi2Causality.input, setter=lambda x: setattr(self, "velocity", x)))

        # Register output
        self.register_variable(Real("force", causality=Fmi2Causality.output, getter=lambda: self.force))

    def do_step(self, t, dt):
        self.force = - self.k1 * self.angle - self.k2 * self.angular_velocity - self.k3 * self.position - self.k4 * self.velocity
        return True