from typing import List

from llm_alpha_mini.llm.llm import LLM
from llm_alpha_mini.tasks import BaseTask, TaskInfo, Parameter
from llm_alpha_mini.tasks.registry import get_task_cls, register_task


class DialogueManager:
    def __init__(self, session, llm: LLM, include_tasks: List[str] = None, exclude_tasks: List[str] = None):
        self.session = session
        self.llm = llm
        self.memory = []

    def listen(self, user_input: str) -> str:
        response = self.llm.query(f"User: {user_input}")
        for candidate in response.candidates:
            function_call = candidate.content.parts[0].function_call
            if function_call and function_call.name == "UpdateMemoryTask":
                task_cls = get_task_cls(function_call.name)
                task = task_cls(**function_call.args)
                task.execute(self)
            elif function_call:
                task_cls = get_task_cls(function_call.name)
                task = task_cls(**function_call.args)
                task.execute(self.session)
        return response

    def update_memory(self, memory: str):
        print(f"Updating memory with: {memory}")
        self.memory.append(memory)


@register_task
class UpdateMemoryTask:

    def __init__(self, fact: str):
        self.fact = fact

    def execute(self, dialogue_manager: DialogueManager):
        dialogue_manager.update_memory(self.fact)

    @classmethod
    def get_task_info(cls) -> TaskInfo:
        return TaskInfo(
            name="UpdateMemoryTask",
            task_description="Add a fact about the user to memory",
            parameters=[
                Parameter("fact", "Fact to store", "string")
            ],
            task_cls=cls
        )