import wpilib
import commands2
from subsystems.drivetrain import Drivetrain
from wpilib import DataLogManager , DriverStation
from subsystems.logging_manager import LoggingSubsystem
import subsystems.encoder
from commands.drive_command import DriveCommand

class MyRobot(commands2.TimedCommandRobot):
    def robotInit(self):
    
        # Initialize controllers
        self.driver_controller = wpilib.XboxController(0)

        # Initialize subsystems
        self.drivetrain = Drivetrain()
        self.encoder = subsystems.encoder.encoder()

        # Initialize data logging
        DataLogManager.start()
        DriverStation.startDataLog(DataLogManager.getLog())
        self.logging_subsystem = LoggingSubsystem() 

        # Set default commands
        PWM_setpoint = 0
        self.setpoint = PWM_setpoint

        self.drivetrain.setDefaultCommand(
            DriveCommand(
                self.drivetrain,
                lambda: -self.driver_controller.getLeftY(),   # Forward/backward (inverted)
                lambda: -self.driver_controller.getLeftX(),   # Left/right (inverted)
                lambda: -self.driver_controller.getRightX()   # Rotation (inverted)
            )
        )

    def autonomousInit(self):
        print("Data Collection Started")


    def autonomousPeriodic(self):

        self.drivetrain.drive(0,0,self.setpoint)
        
        if self.setpoint <= 1:
            self.setpoint += 0.002
        
        else:
            pass

        # Create a dictionary with velocity values from all of the encoders
        self.velocities = self.encoder.get_all_velocities()
        
        # Print the dicitionary to consoles (used primarily for debugging)
        print(f"{self.velocities}")

        # Logs the encoder data to the network tables system
        self.logging_subsystem.log_encoder_data(self.velocities) 
        
    def teleopInit(self):
        print("Logging Initiated")

    def teleopPeriodic(self):
        # Create a dictionary with velocity values from all of the encoders
        self.velocities = self.encoder.get_all_velocities()
        
        # Print the dicitionary to consoles (used primarily for debugging)
        print(f"{self.velocities}")

        # Logs the encoder data to the network tables system
        self.logging_subsystem.log_encoder_data(self.velocities) 
            

if __name__ == "__main__":
    wpilib.run(MyRobot)