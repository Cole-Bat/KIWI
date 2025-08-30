import commands2
import ntcore


class LoggingSubsystem(commands2.SubsystemBase):
    def __init__(self): 
        super().__init__()
       
        # Initialize Network Table
        nt = ntcore.NetworkTableInstance.getDefault()
        table = nt.getTable("Encoders")

        # Initialize tables for datasets
        self.cv1_pub = table.getDoubleTopic("WHEEL A SPEED").publish()
        self.cv2_pub= table.getDoubleTopic("WHEEL B SPEED").publish()
        self.cv3_pub = table.getDoubleTopic("WHEEL C SPEED").publish()
        
   
    def log_encoder_data(self,velocities):
        
        # Switch case for unpacking the dictionary into the respective velocity data sets
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
