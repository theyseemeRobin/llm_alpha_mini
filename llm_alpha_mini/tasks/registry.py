from typing import Dict, List

from llm_alpha_mini.tasks.task import BaseTask, TaskInfo

__TASK_REGISTRY: Dict[str, TaskInfo] = {}

def register_task(task_cls: BaseTask):
    task_str = task_cls.get_task_info().name
    task_info = task_cls.get_task_info()
    if task_str in __TASK_REGISTRY:
        raise ValueError(f"Task {task_str} already registered")
    __TASK_REGISTRY[task_str] = task_info
    return task_cls

def get_task_cls(task_str: str) -> BaseTask:
    if task_str not in __TASK_REGISTRY:
        raise ValueError(f"Task {task_str} not registered")
    return __TASK_REGISTRY[task_str].task_cls

def get_registered_tasks() -> Dict[str, TaskInfo]:
    return __TASK_REGISTRY.copy()

def get_task_info(task_str: str) -> TaskInfo:
    if task_str not in __TASK_REGISTRY:
        raise ValueError(f"Task {task_str} not registered")
    return __TASK_REGISTRY[task_str]

def print_registered_tasks():
    print("Registered tasks:")
    tasks = get_registered_tasks()
    for task in tasks:
        info = get_task_info(task)
        print(info)