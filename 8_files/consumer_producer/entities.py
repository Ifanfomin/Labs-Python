from enum import Enum
from threading import Thread

from typing import (
    Any,
    Callable,
    Dict,
)


class QueueTaskStatus(Enum):
    ACK = 1
    NACK = 0
    DEFER = 2


class ThreadWithReturnValue(Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


# Type hints
Message = Dict[str, Any]
Handler = Callable[[Message], QueueTaskStatus]