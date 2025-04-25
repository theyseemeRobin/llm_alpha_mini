from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from twisted.internet.defer import inlineCallbacks


@dataclass
class Parameter:
    name: str
    description: str
    type: str
    enum: list = None

@dataclass
class TaskInfo:
    name: str                        # what is the name of the task?
    parameters: List[Parameter]       # what has to be specified to perform the task?
    task_description: str            # what does the task accomplish given these specifications?
    task_cls: BaseTask               # the actual task class


class BaseTask(ABC):
    """
    Base task, all tasks should inherit from this class.
    """
    @abstractmethod
    @inlineCallbacks
    def execute(self, session):
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    @abstractmethod
    def get_task_info(cls) -> TaskInfo:
        return TaskInfo("base_task", [], "base class for tasks", cls)

