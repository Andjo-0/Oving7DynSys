from pythonfmu import Fmi2Slave, Real, Fmi2Causality
import numpy as np

class Pendulum(Fmi2Slave):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Physical parameters
        self.initial_angle = 0.0
        self.initial_angular_velocity = 0.0
        self.mass = 0.1
        self.length = 1.0


        # State variables
        self.angle = 0.0
        self.angular_velocity = 0.0
        self.acceleration = 0.0
        self.cart_acceleration = 0.0  # input from cart
        self.force = 0.0

        # Register parameters
        self.register_variable(Real("mass", causality=Fmi2Causality.parameter))
        self.register_variable(Real("length", causality=Fmi2Causality.parameter))
        self.register_variable(Real("initial_angle", causality=Fmi2Causality.parameter))
        self.register_variable(Real("initial_angular_velocity", causality=Fmi2Causality.parameter))
        self.register_variable(Real("acceleration", causality=Fmi2Causality.parameter))

        # Register outputs
        self.register_variable(Real("angle", causality=Fmi2Causality.output, getter=lambda: self.angle))
        self.register_variable(Real("angular_velocity", causality=Fmi2Causality.output, getter=lambda: self.angular_velocity))

        self.register_variable(Real("force", causality=Fmi2Causality.output, getter=lambda: self.force))

        # Register input
        self.register_variable(Real("cart_acceleration", causality=Fmi2Causality.input, setter=lambda x: setattr(self, "cart_acceleration", x)))

    def exit_initialization_mode(self):
        self.angle = self.initial_angle
        self.angular_velocity = self.initial_angular_velocity

    def do_step(self, t, dt):

        # Compute torques
        torque_gravity = self.mass * 9.81 * self.length * np.sin(self.angle)
        torque_cart = - self.mass * self.length * np.cos(self.angle) * self.cart_acceleration

        # Angular acceleration (I = m*L^2)
        self.acceleration = (torque_gravity + torque_cart) / (self.mass * self.length**2)

        # Semi-implicit Euler integration
        self.angular_velocity += self.acceleration * dt
        self.angle += self.angular_velocity * dt

        self.force =  self.mass * self.length * (
            np.sin(self.angle) * self.angular_velocity**2
            - np.cos(self.angle) * self.acceleration
        )

        return True