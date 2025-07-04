# subsystems/drivetrain.py - Drivetrain subsystem
import wpilib
import commands2
import math
import numpy as np
from subsystems.constants import Constants

class Drivetrain(commands2.SubsystemBase):
    def __init__(self):
        super().__init__()
        
        # Gearbox A (0° direction) - 2 motors
        self.motor_a1 = wpilib.PWMTalonSRX(Constants.motor_A1_pwm)  # First motor in gearbox A
        self.motor_a2 = wpilib.PWMTalonSRX(Constants.motor_A2_pwm)  # Second motor in gearbox A
        
        # Gearbox B (120° direction) - 2 motors  
        self.motor_b1 = wpilib.PWMTalonSRX(Constants.motor_B1_pwm)  # First motor in gearbox B
        self.motor_b2 = wpilib.PWMTalonSRX(Constants.motor_B2_pwm)  # Second motor in gearbox B
        
        # Gearbox C (240° direction) - 2 motors
        self.motor_c1 = wpilib.PWMTalonSRX(Constants.motor_C1_pwm)  # First motor in gearbox C
        self.motor_c2 = wpilib.PWMTalonSRX(Constants.motor_C2_pwm)  # Second motor in gearbox C
        
        # Kiwi drive angles (in radians)
        self.motor_angles = [2*math.pi/3, 0, 4*math.pi/3]  # 120°, 0°, 240°
        
    def drive(self, vx, vy, vz):
        """
        Drive the robot using kiwi drive kinematics
        vx: velocity in x direction (-1 to 1)
        vy: velocity in y direction (-1 to 1) 
        vz: angular velocity (-1 to 1)
        """
        
        # Apply deadband
        vx = self.apply_deadband(vx, 0.1)
        vy = self.apply_deadband(vy, 0.1)
        vz = self.apply_deadband(vz, 0.1)
        
        # Kiwi drive inverse kinematics
        motor_speeds = []
        for angle in self.motor_angles:
            speed = (vx * math.sin(angle) - 
                     vy * math.cos(angle) - 
                     vz)
            motor_speeds.append(speed)
        
        # Normalize speeds to [-1, 1] range
        max_speed = max(abs(speed) for speed in motor_speeds)
        if max_speed > 1.0:
            motor_speeds = [speed / max_speed for speed in motor_speeds]
        
        # Set motor speeds for each gearbox (both motors in each gearbox get same speed)
        self.motor_a1.set(motor_speeds[0])
        self.motor_a2.set(motor_speeds[0])
        
        self.motor_b1.set(motor_speeds[1])
        self.motor_b2.set(motor_speeds[1])
        
        self.motor_c1.set(motor_speeds[2])
        self.motor_c2.set(motor_speeds[2])
        
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