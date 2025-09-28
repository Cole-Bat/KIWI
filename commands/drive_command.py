# commands/drive_command.py - Teleop drive command
from commands2 import Command


class DriveCommand(Command):
    def __init__(self, drivetrain, vx_supplier, vy_supplier, vz_supplier):
        super().__init__()

        self.drivetrain = drivetrain
        self.vx_supplier = vx_supplier
        self.vy_supplier = vy_supplier
        self.vz_supplier = vz_supplier

        # This command requires the drivetrain
        self.addRequirements(drivetrain)

    def execute(self):
        # Get joystick inputs
        joy_vx = self.vx_supplier()
        joy_vy = self.vy_supplier()
        joy_vz = self.vz_supplier()

        # Drive the robot (robot-oriented only)
        self.drivetrain.drive(joy_vx, joy_vy, joy_vz)

    def end(self, interrupted):
        self.drivetrain.stop()

    def isFinished(self):
        return False  # This command never finishes on its own
