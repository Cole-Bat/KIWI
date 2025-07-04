import wpilib
from phoenix5.sensors import CANCoder
from phoenix5.sensors import CANCoderStatusFrame
from phoenix5.sensors import SensorVelocityMeasPeriod
from constants import Constants
import math

class CANcoderSubsystem():
    def __init__(self):
        super().__init__()
        
        
        self.cancoder = CANCoder(Constants.cancoder_id_WA)
        
        self.configure_cancoder()

    def configure_cancoder(self):
        """Configure CANCoder settings for velocity"""
        # Sensor direction - set based on your flywheel's positive spin direction
        # False = counter-clockwise positive, True = clockwise positive
        self.cancoder.configSensorDirection(False)
        
        # Magnet offset doesn't matter much for velocity-only measurement
        self.cancoder.configMagnetOffset(0.0)
        
        # Use 0-360 degree range (absolute range doesn't affect velocity)
        self.cancoder.configAbsoluteSensorRange(False)

        # CRITICAL: Fast status frame period for velocity measurement
        # 10ms gives you ~100Hz velocity updates - important for flywheel control
        self.cancoder.setStatusFramePeriod(CANCoderStatusFrame.SensorData, 10)  # 10ms for fast velocity
        self.cancoder.setStatusFramePeriod(CANCoderStatusFrame.VbatAndFaults, 255)  # Slow for faults

        # Velocity measurement period - shorter = more responsive but noisier
        # Options: 1ms, 2ms, 5ms, 10ms, 20ms, 25ms, 50ms, 100ms
        self.cancoder.configVelocityMeasurementPeriod(SensorVelocityMeasPeriod.Period_10Ms)
        
        # Velocity measurement window - how many samples to average
        # Higher = smoother but less responsive. Range: 1-64
        self.cancoder.configVelocityMeasurementWindow(8)
        
    def get_velocity_rpm(self) -> float:
        """Get flywheel velocity in RPM"""
        deg_per_sec = self.get_flywheel_velocity_deg_per_sec()
        rpm = deg_per_sec * 60.0 / 360.0  # Convert deg/sec to RPM
        return rpm
    
    def has_fault(self) -> bool:
        """Check if CANCoder has any faults"""
        return self.cancoder.hasResetOccurred()