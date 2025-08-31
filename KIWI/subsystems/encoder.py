import commands2
import phoenix5.sensors as sen
import subsystems.constants as con


class cancoder(commands2.SubsystemBase):
    def __init__(self):
        super().__init__()
        # should swap this to be a numpy array and clean up the code here and in the drivetrain / logging manager / robot
        # self.cancoder_A = CANCoder(con.CANCODER_ID_WA)

        self.cancoders = {
            "cancoder_A": sen.CANCoder(con.CANCODER_ID_WA),
            "cancoder_B": sen.CANCoder(con.CANCODER_ID_WB),
            "cancoder_C": sen.CANCoder(con.CANCODER_ID_WC),
        }

        self.configure_cancoders()

    def configure_cancoders(self):
        """Configure all encoders with consistent settings"""
        for cancoder in self.cancoders.values():
            config = sen.CANCoderConfiguration()
            unit_denom = sen.SensorTimeBase.PerMinute
            data = sen.CANCoderStatusFrame.SensorData
            # velo_meas = SensorVelocityMeasPeriod(25)
            cancoder.configAllSettings(config)

            cancoder.configFeedbackCoefficient(0.087890625 / 360, "RPM", unit_denom, 0)
            cancoder.setStatusFramePeriod(data, 5, 0)
            cancoder.configVelocityMeasurementWindow(
                4, 0
            )  # need to add this average to the constants file
            # cancoder.configVelocityMeasurementPeriod(velo_meas , 0) if a filter is required i think this is that bode plot frequency thing

    def get_velocity(self, cancoder_name) -> float:
        """Get velocity in degrees per second from specified encoder"""
        if cancoder_name in self.cancoders:
            return self.cancoders[cancoder_name].getVelocity()
        else:
            print(f"Warning: Encoder '{cancoder_name}' not found!")
            return 0.0

    def get_all_velocities(self):
        """Get all encoder velocities as a dictionary"""
        velocities = {}

        for name, cancoder in self.cancoders.items():
            velocities[name] = cancoder.getVelocity()
        return velocities
