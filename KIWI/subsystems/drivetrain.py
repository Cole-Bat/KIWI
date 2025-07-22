# subsystems/drivetrain.py - Drivetrain subsystem
import wpilib
import commands2
import math
import subsystems.constants

class Drivetrain(commands2.SubsystemBase):
    def __init__(self):
        super().__init__()
        
        # Gearbox A (0° direction) - 2 motors
        self.motor_a1 = wpilib.PWMTalonSRX(subsystems.constants.MOTOR_A1_PWM)  # First motor in gearbox A
        self.motor_a2 = wpilib.PWMTalonSRX(subsystems.constants.MOTOR_A2_PWM)  # Second motor in gearbox A
        
        # Gearbox B (120° direction) - 2 motors  
        self.motor_b1 = wpilib.PWMTalonSRX(subsystems.constants.MOTOR_B1_PWM)  # First motor in gearbox B
        self.motor_b2 = wpilib.PWMTalonSRX(subsystems.constants.MOTOR_B2_PWM)  # Second motor in gearbox B
        
        # Gearbox C (240° direction) - 2 motors
        self.motor_c1 = wpilib.PWMTalonSRX(subsystems.constants.MOTOR_C1_PWM)  # First motor in gearbox C
        self.motor_c2 = wpilib.PWMTalonSRX(subsystems.constants.MOTOR_C2_PWM)  # Second motor in gearbox C
        
        # Kiwi drive angles (in radians)
        self.motor_angles = [2*math.pi/3, 0, 4*math.pi/3]  # 120°, 0°, 240°
        
    def drive(self, vx, vy, vz):
        """
        Drive the robot using kiwi drive kinematics
        vx: velocity in x direction (-1 to 1)
        vy: velocity in y direction (-1 to 1) 
        vz: angular velocity (-1 to 1)
        """

        # Apply non-linear curves first
        vx, vy = self.apply_translation_curve(vx, vy)
        vz = self.apply_curve(vz, subsystems.constants.CURVE_BASE)

        # Apply deadband
        vx = self.apply_deadband(vx, subsystems.constants.DEADBAND_VALUE)
        vy = self.apply_deadband(vy, subsystems.constants.DEADBAND_VALUE)
        vz = self.apply_deadband(vz, subsystems.constants.DEADBAND_VALUE)
        
        # Kiwi drive inverse kinematics
        motor_speeds = []
        for angle in self.motor_angles:
            speed = (vx * math.sin(angle) - 
                     vy * math.cos(angle) - 
                     vz)
            motor_speeds.append(speed)
        
        # Normalize speeds to [-1, 1] range (lowkey no clue what this does)
        max_speed = max(abs(speed) for speed in motor_speeds)
        if max_speed > 1.0:
            motor_speeds = [speed / max_speed for speed in motor_speeds]
        
        # Apply speed modifier to cap at 80% duty cycle (can this not just be added to the inverse kinematics section?)
        motor_speeds = [speed * subsystems.constants.PWM_SPEED_MODIFIER for speed in motor_speeds]

        # Set motor speeds for each gearbox (both motors in each gearbox get same speed)
        self.motor_a1.set(motor_speeds[0])
        self.motor_a2.set(motor_speeds[0])
        
        self.motor_b1.set(motor_speeds[1])
        self.motor_b2.set(motor_speeds[1])
        
        self.motor_c1.set(motor_speeds[2])
        self.motor_c2.set(motor_speeds[2])

    def apply_curve(self, input_value, curve_base):
        """
        Apply a non-linear curve to joystick input (no deadband)
        
        Args:
            input_value: Raw joystick input (-1.0 to 1.0)
            curve_power: Exponent for the curve (1.0 = linear, >1.0 = more precise at low speeds)
        
        Returns:
            Curved output value (-1.0 to 1.0)
        """
        sign = 1.0 if input_value >= 0 else -1.0
        magnitude = abs(input_value)
        
        # Apply curve
        curved_magnitude = math.log(1 + magnitude, curve_base)
        
        return sign * curved_magnitude
        
    def apply_deadband(self, value, deadband):
        """Apply deadband to joystick input"""
        if abs(value) < deadband:
            return 0.0
        return (value - math.copysign(deadband, value)) / (1.0 - deadband)

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
        curved_magnitude = self.apply_curve(magnitude, subsystems.constants.CURVE_BASE)
        
        # Maintain original direction
        scale_factor = curved_magnitude / magnitude
        return vx * scale_factor, vy * scale_factor

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