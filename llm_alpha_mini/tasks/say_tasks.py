from llm_alpha_mini.tasks.task import BaseTask, TaskInfo, Parameter
from llm_alpha_mini.tasks.registry import register_task


@register_task
class Say(BaseTask):

    def __init__(self, text: str):
        self.text = text

    def execute(self, session):
        # yield session.call(
        #     "rie.dialogue.say",
        #     text=self.text
        # )
        print(f"{self.text}")

    @classmethod
    def get_task_info(cls) -> TaskInfo:
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

    def __init__(self, text: str):
        self.text = text

    def execute(self, session):
        # yield session.call(
        #     "rie.dialogue.say_animated",
        #     text=self.text
        # )
        print(f"<with gestures>: {self.text}")

    @classmethod
    def get_task_info(cls) -> TaskInfo:
        return TaskInfo(
            name="AnimatedSay",
            task_description="Speak a specified sequence of text aloud",
            parameters=[
                Parameter("text", "What to say", "string")
            ],
            task_cls=cls
        )