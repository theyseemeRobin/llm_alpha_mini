from typing import Dict, List

from llm_alpha_mini.tasks.task import BaseTask, TaskInfo
"""
Registry that keeps track of all of the available tasks.
"""

__TASK_REGISTRY: Dict[str, TaskInfo] = {}

def register_task(task_cls: BaseTask) -> BaseTask:
    """
    Register a task class using the decorator.

    Args:
        task_cls (BaseTask): The task class to register.

    Returns:
        BaseTask: The task class.
    """
    task_str = task_cls.get_task_info().name
    task_info = task_cls.get_task_info()
    if task_str in __TASK_REGISTRY:
        raise ValueError(f"Task {task_str} already registered")
    __TASK_REGISTRY[task_str] = task_info
    return task_cls

def get_task_cls(task_str: str) -> BaseTask:
    """
    Retrieve a task class by its name.

    Args:
        task_str (str): The name of the task.

    Returns:
        BaseTask: The task class.
    """
    if task_str not in __TASK_REGISTRY:
        raise ValueError(f"Task {task_str} not registered")
    return __TASK_REGISTRY[task_str].task_cls

def get_registered_tasks() -> Dict[str, TaskInfo]:
    """
    Retrieve all registered task infos.

    Returns:
        Dict[str, TaskInfo]: Dictionary of the registered task infos.
    """
    return __TASK_REGISTRY.copy()

def get_task_info(task_str: str) -> TaskInfo:
    """
    Retrieve a task info by its name.

    Args:
        task_str (str): The name of the task.
    """
    if task_str not in __TASK_REGISTRY:
        raise ValueError(f"Task {task_str} not registered")
    return __TASK_REGISTRY[task_str]

def print_registered_tasks():
    """
    Print the registered task infos.
    """
    print("Registered tasks:")
    tasks = get_registered_tasks()
    for task in tasks:
        info = get_task_info(task)
        print(info)