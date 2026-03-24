import contextlib

import time

import uuid

from consumer_producer import entities, utils
from dataclasses import dataclass

from queue import Queue

from typing import Protocol, Optional, List


class ProducerProtocol(Protocol):
    def produce(self, message: entities.Message):
        ...


class ThreadProducerProtocol(Protocol):
    def start_produce(self, message: entities.Message, time_to_produce: float):
        ...

    def join(self):
        ...


@dataclass
class Producer:
    queue: Queue
    id: uuid.UUID = uuid.uuid4()

    def produce(self, messages: List[entities.Message], time_to_produce: float):
        for msg in messages:
            time.sleep(time_to_produce)  # имитация врмени генерации задачи
            print(f'Produce msg={msg}\n')
            self.queue.put(msg)


@dataclass
class ThreadProducer:
    producer: ProducerProtocol
    _t: Optional[entities.ThreadWithReturnValue] = None

    def start_produce(self, messages: List[entities.Message], time_to_produce: float):
        self._t = entities.ThreadWithReturnValue(target=self.producer.produce, args=(messages, time_to_produce))
        self._t.start()

    def join(self):
        return self._t.join()


@dataclass
class ThreadProducerGroup:
    producers: List[ThreadProducer]

    @contextlib.contextmanager
    def produce(self, messages: List[entities.Message], time_to_produce: float):
        msgs_batches = utils.batched(messages, len(self.producers))
        for i, p in enumerate(self.producers):
            p.start_produce(msgs_batches[i], time_to_produce)
        try:
            yield
        finally:
            for p in self.producers:
                p.join()
