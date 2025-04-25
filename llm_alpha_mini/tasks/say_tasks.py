from twisted.internet.defer import inlineCallbacks
from llm_alpha_mini.tasks.task import BaseTask, TaskInfo, Parameter
from llm_alpha_mini.tasks.registry import register_task


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
        yield session.call(
            "rie.dialogue.say",
            text=self.text
        )
        print(f"{self.text}")

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


@register_task
class AnimatedSay(BaseTask):
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
        yield session.call(
            "rie.dialogue.say_animated",
            text=self.text
        )
        print(f"<with gestures>: {self.text}")

    @classmethod
    def get_task_info(cls) -> TaskInfo:
        """
        Get the task information for the function description

        returns:
            TaskInfo (TaskInfo): Information about the task.
        """
        return TaskInfo(
            name="AnimatedSay",
            task_description="Speak a specified sequence of text aloud",
            parameters=[
                Parameter("text", "What to say", "string")
            ],
            task_cls=cls
        )
