import wpilib
import commands2
from subsystems.drivetrain import Drivetrain
from subsystems.logging_manager import LoggingSubsystem
from subsystems.encoder import CAN_coder
from commands.drive_command import DriveCommand


class MyRobot(commands2.TimedCommandRobot):
    def robotInit(self):
    
        
        # Initialize controllers
        self.driver_controller = wpilib.XboxController(0)

        # Initialize subsystems
        self.drivetrain = Drivetrain()
        self.encoder = CAN_coder()

        # Initialize data logging
        self.logging_subsystem = LoggingSubsystem(self.driver_controller) 

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

    def teleopPeriodic(self):
        print(f"{self.encoder.get_velocity()}")
         

if __name__ == "__main__":
    wpilib.run(MyRobot)