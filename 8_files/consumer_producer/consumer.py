import time
import uuid

from consumer_producer import entities
from dataclasses import dataclass

from queue import Queue

from typing import Protocol, List, Optional


class ConsumerProtocol(Protocol):
    def consume(self, handler: entities.Handler) -> entities.QueueTaskStatus:
        ...


class ThreadConsumerProtocol(Protocol):
    def start_consume(self, handler: entities.Handler) -> entities.QueueTaskStatus:
        ...

    def join(self):
        ...


@dataclass
class Consumer:
    queue: Queue
    id: uuid.UUID = uuid.uuid4()

    def consume(self, handler: entities.Handler) -> entities.QueueTaskStatus:
        task = self.queue.get()
        print(f'Consume msg={task}\n')
        return handler(task)


@dataclass
class ThreadConsumer:
    consumer: ConsumerProtocol
    _t: Optional[entities.ThreadWithReturnValue] = None

    def start_consume(self, handler: entities.Handler) -> entities.QueueTaskStatus:
        self._t = entities.ThreadWithReturnValue(target=self.consumer.consume, args=(handler,))
        self._t.start()

    def join(self):
        return self._t.join()


@dataclass
class ThreadConsumerGroup:
    consumers: List[ThreadConsumerProtocol]
    consume_wait_timeout: int = 2

    def consume(self, handler: entities.Handler):
        while True:
            time.sleep(self.consume_wait_timeout)
            self._consume_once(handler)

    def _consume_once(self, handler: entities.Handler):
        for c in self.consumers:
            c.start_consume(handler)
        for c in self.consumers:
            c.join()
