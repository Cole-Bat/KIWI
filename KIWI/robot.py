import wpilib
import commands2
from subsystems.drivetrain import Drivetrain
from subsystems.logging_manager import LoggingSubsystem
import subsystems.encoder
from commands.drive_command import DriveCommand
import ntcore

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
        nt = ntcore.NetworkTableInstance.getDefault()
        table = nt.getTable("Encoders")

        self.cv1_pub = table.getDoubleTopic("Cancoder Value 1").publish()
        self.cv2_pub= table.getDoubleTopic("Cancoder Value 2").publish()
        self.cv3_pub = table.getDoubleTopic("Cancoder Value 3").publish()
        self.cv1 = 0.0
        self.cv2 = 0.0
        self.cv3 = 0.0

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
        
        #need help indexing through the dictionary so that each item is published to the respective cancoder graph
        # add in a switch case if, elif optimization isn't a worry. default case else to error

        for encoder_name, velocity in velocities.items():
            
            if encoder_name == "cancoder_1":
                self.cv1 = velocity
                self.cv1_pub.set(self.cv1)

            elif encoder_name == "cancoder_2":
                self.cv2 = velocity
                self.cv2_pub.set(self.cv2)

            elif encoder_name == "cancoder_3":
                self.cv3 = velocity
                self.cv3_pub.set(self.cv3)

            else:
                print("error: cancoder not found")    
            
        print(f"{velocities}")
         

if __name__ == "__main__":
    wpilib.run(MyRobot)