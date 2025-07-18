import wpilib
import commands2
from subsystems.drivetrain import Drivetrain
from subsystems.logging_manager import LoggingSubsystem
import subsystems.encoder
from commands.drive_command import DriveCommand
from networktables import NetworkTablesInstance

class MyRobot(commands2.TimedCommandRobot):
    def robotInit(self):
    
        # Initialize controllers
        self.driver_controller = wpilib.XboxController(0)

        # Initialize subsystems
        self.drivetrain = Drivetrain()
        self.encoder = subsystems.encoder.encoder()

        # Initialize data logging
        self.logging_subsystem = LoggingSubsystem(self.driver_controller) 

        # Initialize Network Table
        nt = NetworkTablesInstance.getDefault()
        self.table = nt.getTable("Encoders")

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
        velocities = self.encoder.get_all_velocities()

        for encoder_name, velocity in velocities.items():
            subtable = self.table.getSubTable(encoder_name)
            subtable.putNumber("Velocity", velocity)
        
        print(f"{velocities}")
         

if __name__ == "__main__":
    wpilib.run(MyRobot)