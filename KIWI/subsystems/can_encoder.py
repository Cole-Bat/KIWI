import wpilib
from phoenix6.hardware import CANcoder
import math

class CANcoderSubsystem():
    def __init__(self):
        super().__init__()
        
        cancoder_id = 9  # CAN ID is current set to 9 should add a constants file
        self.cancoder = CANcoder(cancoder_id)
        
        # Get velocity status signal
        self.velocity_signal = self.cancoder.get_velocity()
        
        # Set update frequency for velocity
        self.velocity_signal.set_update_frequency(100)  # 100Hz for fast velocity updates
        
    def get_velocity_rpm(self) -> float:
        """Get flywheel velocity in RPM"""
        # Get velocity in rotations per second
        velocity_rps = self.velocity_signal.value
        
        # Convert to RPM
        rpm = velocity_rps * 60.0
        return rpm
    
    def get_velocity_deg_per_sec(self) -> float:
        """Get flywheel velocity in degrees per second"""
        # Get velocity in rotations per second
        velocity_rps = self.velocity_signal.value
        
        # Convert to degrees per second
        deg_per_sec = velocity_rps * 360.0
        return deg_per_sec
    
 
   