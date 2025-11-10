import commands2
import subsystems.constants as con
import ntcore
from protobuf.commands_pb2 import ProtobufQuestNavCommand
import protobuf.data_pb2
import wpimath

class QuestNav(commands2.SubsystemBase):
    def __init__(self):
        super().__init__()

        self.command_id = 0

        self.nt = ntcore.NetworkTableInstance.getDefault()

        self.quest_nav_table = self.nt.getTable("QuestNav")
        self.request_topic = self.quest_nav_table.getRawTopic("request").publish("ProtobufQuestNavCommand")

        self.pos_table = self.nt.getTable("Position")
        self.pos_pub = self.pos_table.getStructTopic("Position", wpimath.geometry.Pose2d).publish()

    def set_pose(self, pose):
        quest_pos_init = pose.transformBy(con.ROBOT_TO_QUEST)
        print("I am working")
        reset_command = ProtobufQuestNavCommand()

        reset_command.type = 1
        reset_command.command_id = self.command_id
        self.command_id += 1

        reset_command.pose_reset_payload.target_pose.translation.x = quest_pos_init.translation().X()
        reset_command.pose_reset_payload.target_pose.translation.y = quest_pos_init.translation().Y()
        reset_command.pose_reset_payload.target_pose.rotation.value = quest_pos_init.rotation().radians()

        self.request_topic.set(reset_command.SerializeToString())

    def log_field_pos(self):
        
        position = self.get_field_postion()
        if position is not None:

            self.pos_pub.set(self.get_field_postion())

    def get_field_postion(self):
        encodedFrameData = self.quest_nav_table.getRaw("frameData", None)
        
        if encodedFrameData is not None:
            decodedFrameData = protobuf.data_pb2.ProtobufQuestNavFrameData()
            decodedFrameData.ParseFromString(encodedFrameData)

            pos_data = wpimath.geometry.Pose2d(decodedFrameData.pose2d.translation.x, 
                                                             decodedFrameData.pose2d.translation.y,
                                                             decodedFrameData.pose2d.rotation.value)
            
            return pos_data.transformBy(con.ROBOT_TO_QUEST.inverse())
        return None
    
    def periodic(self):
        self.log_field_pos()
