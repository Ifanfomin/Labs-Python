import random

import time
import queue

from consumer_producer.entities import QueueTaskStatus

from consumer_producer.consumer import Consumer, ThreadConsumer, ThreadConsumerGroup
from consumer_producer.producer import Producer, ThreadProducer, ThreadProducerGroup


def hdr(msg) -> QueueTaskStatus:
    time_to_handle_one_task = 0.5
    time.sleep(time_to_handle_one_task)  # имитация времени работы функции
    # имитация успешности обработки сообщения
    status = QueueTaskStatus.ACK if random.randint(0, 10) >= 2 else QueueTaskStatus.NACK
    print(f'Handle msg={msg} with status {status}\n')
    return status


def main():
    q = queue.Queue()
    cons = [ThreadConsumer(Consumer(q)) for _ in range(2)]
    prods = [ThreadProducer(Producer(q)) for _ in range(2)]

    with ThreadProducerGroup(prods).produce([{str(i): i} for i in range(10)], 0.5):
        ThreadConsumerGroup(cons).consume(hdr)


if __name__ == '__main__':
    main()
