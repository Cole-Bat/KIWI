import wpilib
import commands2
from subsystems.drivetrain import Drivetrain
from wpilib import DataLogManager, DriverStation
from subsystems.logging_manager import LoggingSubsystem
import subsystems.encoder as enc
from commands.drive_command import DriveCommand


class MyRobot(commands2.TimedCommandRobot):
    def robotInit(self):

        # Initialize controllers
        self.driver_controller = wpilib.XboxController(0)

        # Initialize subsystems
        self.encoder = enc.cancoder()
        self.drivetrain = Drivetrain(self.encoder)

        # Initialize data logging
        DataLogManager.start()
        DriverStation.startDataLog(DataLogManager.getLog())
        self.logging_subsystem = LoggingSubsystem()

        self.teleDrive = self.drivetrain.setDefaultCommand(
                    DriveCommand(
                        self.drivetrain,
                        lambda: self.driver_controller.getLeftX(),  # Left/right
                        lambda: self.driver_controller.getLeftY(),  # Forward/backward 
                        lambda: self.driver_controller.getRightX(),  # Rotation
                    )
                )

    def autonomousInit(self):
        print("Data Collection Started")

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        print("Logging Initiated")

    def teleopPeriodic(self):

        # Create some output of the PID error values for debugging

        # Create a dictionary with velocity values from all of the encoders
        self.velocities = self.encoder.get_all_velocities()

        # Logs the encoder data to the network tables system
        self.logging_subsystem.log_encoder_data(self.velocities)

        # Print the dicitionary to consoles (used primarily for debugging)
        # print(f"{self.velocities}")


if __name__ == "__main__":
    wpilib.run(MyRobot)
