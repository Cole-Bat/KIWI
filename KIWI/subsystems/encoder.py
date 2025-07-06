from phoenix5.sensors import CANCoder
import subsystems.constants
import commands2


class CAN_coder(commands2.SubsystemBase):
    def __init__(self):
        super().__init__()

        self.cancoder = CANCoder(subsystems.constants.CANCODER_ID_WA)

        self.configure_cancoder()
    
    def configure_cancoder(self):
        pass

    def get_velocity(self):
           velocity = self.cancoder.getVelocity()
           velocity_rpm = velocity * 60 / 360
           return velocity_rpm