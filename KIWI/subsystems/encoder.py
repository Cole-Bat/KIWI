from phoenix5.sensors import CANCoder
from phoenix5.sensors import CANCoderConfiguration
import subsystems.constants
import commands2


class CAN_coder(commands2.SubsystemBase):
    def __init__(self):
        super().__init__()

        self.cancoders = {
            "cancoder_1": CANCoder(subsystems.constants.CANCODER_ID_WA),  
            "cancoder_2": CANCoder(subsystems.constants.CANCODER_ID_WB),    
            "cancoder_3": CANCoder(subsystems.constants.CANCODER_ID_WC),  
        }

        self.configure_cancoders()
    
    def configure_cancoders(self):
        """Configure all encoders with consistent settings"""
        for cancoder in self.cancoders.items():
             # Reset encoder to zero
                CANCoderConfiguration.initializationStrategy()
        

    def get_velocity(self, cancoder_name):
        """Get velocity in degrees per second from specified encoder"""
        if cancoder_name in self.cancoders:
            return self.cancoders[cancoder_name].getVelocity()
        else:
            print(f"Warning: Encoder '{cancoder_name}' not found!")
            return 0.0
        
    def get_all_velocities(self):
        """Get all encoder velocities as a dictionary"""
        velocities = {}
        for name, cancoder in self.cancoders.items():
            velocities[name] = cancoder.getVelocity()
        return velocities