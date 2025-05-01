from twisted.internet.defer import inlineCallbacks
from llm_alpha_mini.tasks.task import BaseTask, TaskInfo, Parameter
from llm_alpha_mini.tasks.registry import register_task
from llm_alpha_mini.tasks.motion_available import set_motion_available

# Dictionary with all the available Blockly commands.
blockly_dict = {
    "wave" : "BlocklyWaveRightArm",
    "dab" : "BlocklyDab",
    "dance" : "BlocklyChickenDance",
    "standup" : "BlocklyStand",
    "haka" : "BlocklyHaka"
}

@register_task
class Gesture(BaseTask):
    """
    Gesture task class, defines several predefined gesture actions.
    """
    def __init__(self, gesture: str):
        self.gesture_name = gesture

    @inlineCallbacks
    def execute(self, session):
        """
        Execute the specified gesture task.

        Args:
            session (Session): Session object that connects to the robot.
        """
        set_motion_available(False)

        if session is not None:
            yield session.call(
                "rom.optional.behavior.play",
                name=blockly_dict[self.gesture_name]
            )
        print(f"*{self.gesture_name}s*")

    @classmethod
    def get_task_info(cls) -> TaskInfo:
        """
        Get the task information for the function description

        returns:
            TaskInfo (TaskInfo): Information about the task.
        """
        return TaskInfo(
            name="Gesture",
            task_description="Gesture to the conversation partner",
            parameters=[
                Parameter("gesture", "The gesture to perform", "string", list(blockly_dict.keys())),
            ],
            task_cls=cls
        )
