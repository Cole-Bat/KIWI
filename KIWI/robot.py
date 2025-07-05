import wpilib
import commands2
from subsystems.drivetrain import Drivetrain
from subsystems.logging_manager import LoggingSubsystem
from commands.drive_command import DriveCommand
from phoenix5.sensors import CANCoder
import subsystems.constants

class MyRobot(commands2.TimedCommandRobot):
    def robotInit(self):
        
        # Initialize encoder
        self.cancoder = CANCoder(subsystems.constants.CANCODER_ID_WA)

        # Initialize controllers
        self.driver_controller = wpilib.XboxController(0)
       # self.encoder = CANcoderSubsystem()

        # Initialize subsystems
        self.drivetrain = Drivetrain()

        # Initialize data logging
        self.logging_subsystem = LoggingSubsystem(self.driver_controller) #self.encoder

        # Set default commands
        self.drivetrain.setDefaultCommand(
            DriveCommand(
                self.drivetrain,
                lambda: -self.driver_controller.getLeftY(),   # Forward/backward (inverted)
                lambda: -self.driver_controller.getLeftX(),   # Left/right (inverted)
                lambda: -self.driver_controller.getRightX()   # Rotation (inverted)
            )
        )

    def autonomousInit(self):
        pass
        
    def autonomousPeriodic(self):
        pass
        
    def teleopInit(self):
        print("Logging Initiated")
     
#        try:
 #           self.cancoder = CANcoder(9)
#        except Exception as e:
#            print(f"CANCoder creation failed: {e}")
 #           self.cancoder = None


    def teleopPeriodic(self):
            
            velocity = self.cancoder.getVelocity()
            print(f"{velocity}")


if __name__ == "__main__":
    wpilib.run(MyRobot)