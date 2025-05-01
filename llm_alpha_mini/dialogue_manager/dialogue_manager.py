from typing import List

from twisted.internet.defer import inlineCallbacks

from llm_alpha_mini.llm.llm import LLM
from llm_alpha_mini.tasks import BaseTask, TaskInfo, Parameter
from llm_alpha_mini.tasks.registry import get_task_cls, register_task
from llm_alpha_mini.tasks import set_motion_available

class DialogueManager:
    """
    DialogueManager Class, manages the dialogue between the user and the Robot
    """
    def __init__(self, session, llm: LLM, include_tasks: List[str] = None, exclude_tasks: List[str] = None):
        """
        Constructor for the DialogueManager Class.
        Args:
            session (Session): The session that the dialogue manager will operate on.
            llm (LLM): The LLM that the robot is using.
            include_tasks (List[str]): List of tasks to include in the dialogue.
            exclude_tasks (List[str]): List of tasks to exclude in the dialogue.
        """
        self.session = session
        self.llm = llm
        self.memory = []

    @inlineCallbacks
    def listen(self, user_input: str) -> str:
        """
        Function that takes the user_input and returns the LLM's response through the robot.

        Args:
            user_input (str): The user_input to send to the LLM.

        Returns:
            str: The LLM's response.'
        """
        print(f"User input: {user_input}")
        responses = self.llm.query(f"User: {user_input}")
        for function_call in responses.function_calls:
            if function_call and function_call.name == "UpdateMemoryTask":
                task_cls = get_task_cls(function_call.name)
                task = task_cls(**function_call.args)
                yield task.execute(self)
            elif function_call:
                task_cls = get_task_cls(function_call.name)
                task = task_cls(**function_call.args)
                yield task.execute(self.session)
        set_motion_available(True)
        return responses

    def update_memory(self, memory: str):
        """
        Update the LLM's memory and notify the user.

        Args:
            memory (str): The new memory to update.
        """
        print(f"Updating memory with: {memory}")
        self.memory.append(memory)


@register_task
class UpdateMemoryTask:
    """
    UpdateMemoryTask Task Class used to update the memory of the LLM.
    """
    def __init__(self, fact: str):
        """
        Constructor for the UpdateMemoryTask Class.

        Args:
            fact (str): The fact to update.
        """
        self.fact = fact

    def execute(self, dialogue_manager: DialogueManager):
        """
        Update the LLM's memory through the dialogue manager.

        Args:
            dialogue_manager (DialogueManager): The dialogue manager that will execute the task.
        """
        dialogue_manager.update_memory(self.fact)

    @classmethod
    def get_task_info(cls) -> TaskInfo:
        """
        Get the task information for the function description

        returns:
            TaskInfo (TaskInfo): Information about the task.
        """
        return TaskInfo(
            name="UpdateMemoryTask",
            task_description="Add a fact about the user to memory",
            parameters=[
                Parameter("fact", "Fact to store", "string")
            ],
            task_cls=cls
        )
