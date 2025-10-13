import wpilib
import wpimath
import commands2
from subsystems.drivetrain import Drivetrain
from subsystems.questnav import QuestNav
from wpilib import DataLogManager, DriverStation
from subsystems.logging_manager import LoggingSubsystem
import subsystems.encoder as enc
from commands.drive_command import DriveCommand


class MyRobot(commands2.TimedCommandRobot):
    def robotInit(self):

        # Initialize controllers
        self.driver_controller = commands2.button.CommandXboxController(0)

        # Initialize subsystems
        self.encoder = enc.cancoder()
        self.drivetrain = Drivetrain(self.encoder)
        self.questnav = QuestNav()

        # Initialize data logging
        DataLogManager.start()
        DriverStation.startDataLog(DataLogManager.getLog())
        self.logging_subsystem = LoggingSubsystem()

        self.driver_controller.leftBumper().onTrue(commands2.InstantCommand(lambda: self.questnav.set_pose(wpimath.geometry.Pose2d(8.2, 4.1, 0))))

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
        pass

    def teleopPeriodic(self):

        # quest nav printing
        self.logging_subsystem.log_field_pos()

        # Create a dictionary with velocity values from all of the encoders
        self.velocities = self.encoder.get_all_velocities()

        # Logs the encoder data to the network tables system
        self.logging_subsystem.log_encoder_data(self.velocities)

if __name__ == "__main__":
    wpilib.run(MyRobot)
