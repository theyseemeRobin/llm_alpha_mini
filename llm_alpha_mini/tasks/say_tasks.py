from twisted.internet.defer import inlineCallbacks
from llm_alpha_mini.tasks.task import BaseTask, TaskInfo, Parameter
from llm_alpha_mini.tasks.registry import register_task
from llm_alpha_mini.tasks.motion_available import motion_available

@register_task
class Say(BaseTask):
    """
    Say class task class.
    """
    def __init__(self, text: str):
        """
        Constructor of the Say class.

        Args:
            text (str): The text to say.
        """
        self.text = text

    @inlineCallbacks
    def execute(self, session):
        """
        Execute the Say task.

        Args:
            session (Session): Session object that connects to the robot.
        """
        mode = "rie.dialogue.say_animated" if motion_available() else "rie.dialogue.say"
        if session is not None:
            yield session.call(
                mode,
                text=self.text
            )
        print(f"{self.text} | {mode}")

    @classmethod
    def get_task_info(cls) -> TaskInfo:
        """
        Get the task information for the function description

        returns:
            TaskInfo (TaskInfo): Information about the task.
        """
        return TaskInfo(
            name="Say",
            task_description="Speak a specified sequence of text aloud",
            parameters=[
                Parameter("text", "What to say", "string")
            ],
            task_cls=cls
        )
