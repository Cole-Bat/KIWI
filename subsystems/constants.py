# ascii art of the kiwi drive and what wheel is 1 2 3 would go hard here

import wpimath
import math as m

# CAN Constants
CANCODER_ID_WA = 9  # CAN ID for Wheel 1
CANCODER_ID_WB = 10  # CAN ID for Wheel 2
CANCODER_ID_WC = 11  # CAN ID for Wheel 3

# PWM Constants
MOTOR_A1_PWM = 4  # Wheel A Motor 1 PWM port
MOTOR_A2_PWM = 5  # Wheel A Motor 2 PWM port
MOTOR_B1_PWM = 6  # Wheel B Motor 1 PWM port
MOTOR_B2_PWM = 7  # Wheel B Motor 2 PWM port
MOTOR_C1_PWM = 8  # Wheel C Motor 1 PWM port
MOTOR_C2_PWM = 9  # Wheel C Motor 2 PWM port

# Motor Controller Constants
PWM_SPEED_MODIFIER = (
    1.0  # leave as 1.0, only required when not applying the curve to the system
)
DEADBAND_VALUE = 0.05  # Should be greater than the deadband of the talon controller
CURVE_BASE = 2  # 2.7 corresponds to a a maximum of 70 % Duty cycle
ROTATION_CURVE = 2  # 2.7 corresponds to a a maximum of 70 % Duty cycle
MAX_VALUE = 0.75

# Constants for slew rate limiting
SRL_RATE_ACC = 0.5 #bring up to 3 to 5 seconds
SRL_RATE_DEC = -2.0 #can increase further than positive

# Constants for the PID controller
PWM_VEL = 0.00168  #previously calculated was 0.00168
kP = 0.68
kI = 1.5
kD = 0.03
CLAMP_MIN = -0.75
CLAMP_MAX = 0.75

ROBOT_TO_QUEST = wpimath.geometry.Transform2d(0, -0.270, m.pi)
