### Задача 1
# Требуется реализовать мьютекс через редис (Redis / Valkey)

import time
from concurrent.futures import ThreadPoolExecutor
import redis
import time
import uuid

class RedisLock():
    def __init__(self):
        self.r = redis.Redis()
        self.id = str(uuid.uuid4())
        if self.r.exists("mu"):
            self.r.delete("mu")
            

    def __enter__(self):
        while True:
            result = self.r.set("mu", self.id, nx=True)
            
            if result:
                return self
            else:
                time.sleep(0.01)
            
    def __exit__(self, exc_type, exc, tb):
        result = self.r.get("mu")
        if result.decode() == self.id:
            self.r.delete("mu")

    

mu = RedisLock()  # вот его нужно реализовать
result = 0

def function():
    with mu:
        global result
        r = result
        time.sleep(0.2)
        result = r + 1
        print(result)

    
def main():  
    with ThreadPoolExecutor(max_workers=5) as executor:
        for _ in range(10):
            executor.submit(function)
    print(result)  # хотим получить в итоге 10
    
main()