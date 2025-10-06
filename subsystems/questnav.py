import wpimath
import subsystems.constants as con
import ntcore
from protobuf.commands_pb2 import ProtobufQuestNavCommand, ProtobufQuestNavPoseResetPayload
from protobuf.geometry2d_pb2 import ProtobufTranslation2d, ProtobufRotation2d, ProtobufPose2d

def set_pose():

    pos_init = wpimath.geometry.Pose2d(8.2, 4.1, 0)

    quest_pos_init = pos_init.transformBy(con. ROBOT_TO_QUEST)

    nt = ntcore.NetworkTableInstance.getDefault()
    
    quest_nav_table = nt.getTable("QuestNav")

    reset_command = ProtobufQuestNavCommand()

    reset_command.type = 1
    reset_command.command_id = 0
    reset_command.pose_reset_payload.target_pose.translation.x = quest_pos_init.translation().X()
    reset_command.pose_reset_payload.target_pose.translation.y = quest_pos_init.translation().Y()
    reset_command.pose_reset_payload.target_pose.rotation.value = quest_pos_init.rotation().radians()

    request_topic = quest_nav_table.getStringTopic("request").publish()

    request_topic.set(reset_command.SerializeToString())
    reset_string = reset_command.SerializeToString()

    print(reset_string)