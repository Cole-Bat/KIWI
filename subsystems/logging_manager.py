import wpilib
import wpimath
import commands2
import ntcore
import protobuf.data_pb2


class LoggingSubsystem(commands2.SubsystemBase):
    def __init__(self): 
        super().__init__()
       
        # Initialize Network Tables
        self.field = wpilib.Field2d()
        nt = ntcore.NetworkTableInstance.getDefault()
        enc_table = nt.getTable("Encoders")
        self.quest_nav_table = nt.getTable("QuestNav")
        self.pos_table = nt.getTable("Position")

        # Initialize tables for datasets
        self.cv1_pub = enc_table.getDoubleTopic("WHEEL A SPEED").publish()
        self.cv2_pub = enc_table.getDoubleTopic("WHEEL B SPEED").publish()
        self.cv3_pub = enc_table.getDoubleTopic("WHEEL C SPEED").publish()
        
        self.pos_pub = self.pos_table.getStructTopic("Position", wpimath.geometry.Pose2d).publish() 

       

    def log_field_pos(self):
        
        encodedFrameData = self.quest_nav_table.getRaw("frameData", None)
        
        if encodedFrameData is not None:
            decodedFrameData = protobuf.data_pb2.ProtobufQuestNavFrameData()
            decodedFrameData.ParseFromString(encodedFrameData)

            pos_data = wpimath.geometry.Pose2d(decodedFrameData.pose2d.translation.x, 
                                                             decodedFrameData.pose2d.translation.y,
                                                             decodedFrameData.pose2d.rotation.value)
            # self.field.setRobotPose(pos_data)
            
            self.pos_pub.set(pos_data)
            #print(decodedFrameData)
   
    def log_encoder_data(self,velocities):
        
        # Switch case for unpacking the dictionary into the respective velocity data sets
        for encoder_name, velocity in velocities.items():
            
            if encoder_name == "cancoder_A":
                self.cv1 = velocity
                self.cv1_pub.set(self.cv1)

            elif encoder_name == "cancoder_B":
                self.cv2 = velocity
                self.cv2_pub.set(self.cv2)

            elif encoder_name == "cancoder_C":
                self.cv3 = velocity
                self.cv3_pub.set(self.cv3)

            else:
                print("error: cancoder not found")    
