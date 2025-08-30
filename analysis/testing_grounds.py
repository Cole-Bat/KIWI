import numpy as np
import math
from wpimath.controller import PIDController

t = 0
t_inc = 0.1
input_range = 90.0
deg = 0
data = []
time = []

vx = 0.7
vy = 0.0
vz = 0.0

sample_num = input_range / t_inc
deg_inc = input_range / sample_num

motor_angles = np.array([0, 2*math.pi/3, 4*math.pi/3])
pid = PIDController(1.0,0.0,0.0)

print(np.cos(motor_angles))

motor_speeds = (vx * np.cos(motor_angles) - 
                vy * np.sin(motor_angles) + 
                vz)

motor_speeds2 = np.array([vx * math.cos(motor_angles[0]) - vy * math.sin(motor_angles[0]) + vz,
                                      vx * math.cos(motor_angles[1]) - vy * math.sin(motor_angles[1]) + vz,
                                      vx * math.cos(motor_angles[2]) - vy * math.sin(motor_angles[2]) + vz])

motor_set = motor_speeds / 0.00168
print(motor_set[0])
print((pid.calculate(400, motor_set[0])) / motor_set[0])

print(motor_speeds)

'''
while deg <= input_range:
    data.append(round(deg,4))
    time.append(round(t,4))
    
    deg += deg_inc
    # print(deg)
    #t += t_inc
'''





