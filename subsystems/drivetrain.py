import wpilib
import commands2
import math
import numpy as np
import subsystems.constants as con
import subsystems.encoder as enc
from wpimath.controller import PIDController

class Drivetrain(commands2.SubsystemBase):
    def __init__(self):
        super().__init__()
        
        # Gearbox A (0° direction) - 2 motors
        self.motor_a1 = wpilib.PWMTalonSRX(con.MOTOR_A1_PWM)  # First motor in gearbox A
        self.motor_a2 = wpilib.PWMTalonSRX(con.MOTOR_A2_PWM)  # Second motor in gearbox A
        
        # Gearbox B (120° direction) - 2 motors  
        self.motor_b1 = wpilib.PWMTalonSRX(con.MOTOR_B1_PWM)  # First motor in gearbox B
        self.motor_b2 = wpilib.PWMTalonSRX(con.MOTOR_B2_PWM)  # Second motor in gearbox B
        
        # Gearbox C (240° direction) - 2 motors
        self.motor_c1 = wpilib.PWMTalonSRX(con.MOTOR_C1_PWM)  # First motor in gearbox C
        self.motor_c2 = wpilib.PWMTalonSRX(con.MOTOR_C2_PWM)  # Second motor in gearbox C
        
        # Kiwi drive angles (in radians)
        
        self.motor_angles = np.array([0, 2*math.pi/3, 4*math.pi/3])  # 0°, 120°, 240°
        self.motor_speeds = np.zeros(3)

        self.pid_a = PIDController(con.kP, con.kI, con.kD)
        self.pid_b = PIDController(con.kP, con.kI, con.kD)
        self.pid_c = PIDController(con.kP, con.kI, con.kD)

    def drive(self, vx, vy, vz):
        """
        Drive the robot using kiwi drive kinematics
        vx: velocity in x direction (-1 to 1)
        vy: velocity in y direction (-1 to 1) 
        vz: angular velocity (-1 to 1)
        """

        # Apply non-linear curves first
        vx, vy = self.apply_translation_curve(vx, vy)
        vz = self.apply_curve(vz, con.CURVE_BASE)

        # Apply deadband
        vx = self.apply_deadband(vx, con.DEADBAND_VALUE)
        vy = self.apply_deadband(vy, con.DEADBAND_VALUE)
        vz = self.apply_deadband(vz, con.DEADBAND_VALUE)
        
        # Kiwi drive kinematics
        self.motor_speeds = (vx * np.cos(self.motor_angles) - 
                            vy * np.sin(self.motor_angles) + 
                            vz)
    
        # Normalize speeds to [-1, 1] range (i.e. useful if rotating at max speed and the trig function equals 1)
        max_speed = np.max(np.abs(self.motor_speeds))
        if max_speed > con.MAX_VALUE:
            self.motor_speeds = self.motor_speeds / max_speed
        
        # PID Controller Section
        self.motor_speeds_enc = np.array([enc.cancoder.get_velocity(cancoder_name = "cancoder_A"), 
                                          enc.cancoder.get_velocity(cancoder_name = "cancoder_B"), 
                                          enc.cancoder.get_velocity(cancoder_name = "cancoder_C")])

        if np.any(np.isnan(self.motor_speeds_enc)) or np.any(np.isinf(self.motor_speeds_enc)):
            print("Encoder Failure Detected")
            self.plant_input = self.motor_speeds  # Fallback to open-loop
        else:

            motor_speeds_set = self.motor_speeds * con.PWM_VEL                           
        
            pid_a = self.pid_a.calculate(self.motor_speeds_enc[0], motor_speeds_set[0])
            pid_b = self.pid_b.calculate(self.motor_speeds_enc[1], motor_speeds_set[1])
            pid_c = self.pid_c.calculate(self.motor_speeds_enc[2], motor_speeds_set[2])

            pid_values = np.array([pid_a, pid_b, pid_c]) / con.PWM_VEL

            self.plant_input = self.motor_speeds + pid_values
            
            self.plant_input = np.clip(self.plant_input, con.CLAMP_MIN, con.CLAMP_MAX)


        # Set motor speeds for each gearbox (both motors in each gearbox get same speed)
        self.motor_a1.set(self.plant_input[0])
        self.motor_a2.set(self.plant_input[0])
        
        self.motor_b1.set(self.plant_input[1])
        self.motor_b2.set(self.plant_input[1])
        
        self.motor_c1.set(self.plant_input[2])
        self.motor_c2.set(self.plant_input[2])

    def apply_curve(self, input_value, curve_base):
        """
        Apply a non-linear curve to joystick input (no deadband)
        
        Args:
            input_value: Raw joystick input (-1.0 to 1.0)
            curve_base: Exponent for the curve (1.0 = linear, >1.0 = more precise at low speeds)
        
        Returns:
            Curved output value (-1.0 to 1.0)
        """
        sign = 1.0 if input_value >= 0 else -1.0
        magnitude = abs(input_value)
        
        # Apply curve
        curved_magnitude = math.log(1 + magnitude, curve_base)
        
        return sign * curved_magnitude

    def apply_translation_curve(self, vx, vy):
        """
        Apply non-linear curve to translation inputs (vx, vy)
        This preserves the direction while applying the curve to the magnitude
        """
        # Calculate magnitude and direction
        magnitude = math.sqrt(vx*vx + vy*vy)
        
        if magnitude == 0:
            return 0.0, 0.0
        
        # Apply curve to magnitude only
        curved_magnitude = self.apply_curve(magnitude, con.CURVE_BASE)
        
        # Maintain original direction
        scale_factor = curved_magnitude / magnitude
        return vx * scale_factor, vy * scale_factor
    
    def apply_deadband(self, value, deadband):
        """Apply deadband to joystick input"""
        if abs(value) < deadband:
            return 0.0
        return (value - math.copysign(deadband, value)) / (1.0 - deadband)

    def stop(self):
        """Stop all motors"""
        self.motor_a1.set(0)
        self.motor_a2.set(0)
        self.motor_b1.set(0)
        self.motor_b2.set(0)
        self.motor_c1.set(0)
        self.motor_c2.set(0)    
        
    def periodic(self):
        """Called periodically by the scheduler"""
        pass  # Add telemetry here if needed