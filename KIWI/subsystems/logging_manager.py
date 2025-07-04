import commands2
import wpilib
from subsystems.can_encoder import CANcoderSubsystem
from wpilib import DataLogManager, DriverStation
from wpiutil.log import DoubleLogEntry


class LoggingSubsystem(commands2.SubsystemBase):
    def __init__(self, driver_controller: wpilib.XboxController, encoder:CANcoderSubsystem):
        super().__init__()
           # Initialize data logging
        DataLogManager.start()
        DriverStation.startDataLog(DataLogManager.getLog())

        self.driver_controller = driver_controller
        self.setup_joystick_logging()
        self.encoder = encoder
        self.setup_encoder_logging()

    def setup_joystick_logging(self):
            #Create log entries for AdvantageScope
        self.left_x_entry = DoubleLogEntry(DataLogManager.getLog(), "/JoystickData/LeftStick/X")
        self.left_y_entry = DoubleLogEntry(DataLogManager.getLog(), "/JoystickData/LeftStick/Y")
        self.right_x_entry = DoubleLogEntry(DataLogManager.getLog(), "/JoystickData/RightStick/X")
        self.right_y_entry = DoubleLogEntry(DataLogManager.getLog(), "/JoystickData/RightStick/Y")
        self.encoder_M1_entry = DoubleLogEntry(DataLogManager.getLog(), "/Encoder/M1")
    
    def setup_encoder_logging(self):
        pass
    
    def log_joystick_data(self):
            #raw joystick values
        left_x = self.driver_controller.getLeftX()
        left_y = self.driver_controller.getLeftY()
        right_x = self.driver_controller.getRightX()
        right_y = self.driver_controller.getRightY()

            #log raw values to Datalog
        self.left_x_entry.append(left_x)
        self.left_y_entry.append(left_y)
        self.right_x_entry.append(right_x)
        self.right_y_entry.append(right_y)
    
    def log_encoder_data(self):
            #raw encoder values
        encoder_M1 = self.encoder.get_velocity_rpm()

            #log raw value to Datalog
        self.encoder_M1_entry.append(encoder_M1)
 
    def periodic(self):
        self.log_joystick_data()
        self.log_encoder_data()
