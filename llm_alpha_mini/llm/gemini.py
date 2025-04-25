from typing import List

from google import genai
from google.genai import types
from google.genai.types import AutomaticFunctionCallingConfig

from llm_alpha_mini.llm.llm import LLM
from llm_alpha_mini.tasks import TaskInfo, Parameter
from llm_alpha_mini.tasks.registry import get_registered_tasks

SYSTEM_INSTRUCTIONS = """System:
You are a robot verbally interacting with the elderly. Your task is hold a conversation to get to know the elder 
you are speaking with. During this conversation, you have to estimate and match the level intelligence of the 
other person. 

output format: Your output strictly consists of api calls that perform tasks to control the robot, and will never 
just be text. 

Your goal is to gather information about the elder to personalize future interactions. To this end, whenever you 
learn something new about the elder, use the UpdateMemoryTask to store this information. For a more natural interaction, 
you can use gestures to be more engaging.
"""

def parameter_to_description(parameter: Parameter):
    """
    Function to retrieve the description of the parameter.

    Args:
        parameter (Parameter): The selected parameter.

    Returns:
        str: The description of the parameter.
    """
    description = {}
    description["type"] = parameter.type
    description["description"] = parameter.description
    if parameter.enum is not None:
        description["enum"] = parameter.enum
    return description

def task_info_to_function_description(task_info: TaskInfo):
    """
    Function to retrieve the description of the task.

    Args:
        task_info (TaskInfo): The task info.

    Returns:
        str: The description of the task.
    """
    return {
        "name": task_info.name,
        "description": task_info.task_description,
        "parameters": {
            "type": "object",
            "properties": {param.name: parameter_to_description(param) for param in task_info.parameters},
        "required": [info.name for info in task_info.parameters],
        },
    }

def build_function_descriptions():
    """
    Function to build function descriptions.

    Returns:
        List[FunctionDescription]: The list of function descriptions.
    """
    functions = []
    for task_name, task_info in get_registered_tasks().items():
        function = task_info_to_function_description(task_info)
        functions.append(function)
    return functions


class Gemini(LLM):
    """
    Gemini LLM class.
    """
    def __init__(
            self,
            model: str,
            api_key: str,
            system_instruction: str = SYSTEM_INSTRUCTIONS,
            allowed_functions: List[str] = None
    ):
        """
        Constructor of the Gemini LLM class.
        Args:
            model (str): The model to use.
            api_key (str): The API key to use.
            system_instruction (str, optional): The system instruction to use. Defaults to SYSTEM_INSTRUCTIONS.
            allowed_functions (List[str], optional): The allowed functions to use. Defaults to None.
        """
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.system_instruction = system_instruction
        self.allowed_functions = allowed_functions
        self.tools = None
        self.tool_config = None
        self.config = None
        self.chat = None
        self.start_chat()


    def start_chat(self):
        """
        Start a new chat with Gemini.
        """
        self.tools = types.Tool(function_declarations=build_function_descriptions())
        self.tool_config = types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(
                mode="ANY",
                allowed_function_names=self.allowed_functions
            )
        )
        self.config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            tools=[self.tools],
            tool_config=self.tool_config,
            automatic_function_calling= AutomaticFunctionCallingConfig(disable=True)
        )
        self.chat = self.client.chats.create(model=self.model, config=self.config)

    def query(self, prompt: str) -> str:
        """
        Query the Gemini LLM model.
        Args:
            prompt (str): The prompt to give the LLM.

        Returns:
            str: The response.
        """
        response = self.chat.send_message(prompt)
        return response