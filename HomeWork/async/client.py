import asyncio

from aiohttp import ClientSession


URL = "http://127.0.0.1:8003"


async def create_task(session, hash_value, algorithm):
    params = {
        "hash": hash_value,
        "algorithm": algorithm
    }

    async with session.get(
        f"{URL}/createSolveTask",
        params=params
    ) as response:

        data = await response.json()

    return algorithm, data["taskId"]


async def wait_for_password(session, task_id, algorithm):
    params = {
        "taskId": task_id
    }

    while True:
        async with session.get(
            f"{URL}/getPassword",
            params=params
        ) as response:

            data = await response.json()

        if data["err"] is None:
            return algorithm, data["password"]

        if data["err"]["code"] == 1001:
            print(f"{algorithm}: задача в процессе...")
            await asyncio.sleep(1)
            continue


async def main():
    hash_value = "c4ca4238a0b923820dcc509a6f75849b"

    async with ClientSession() as session:
        async with session.get(
            f"{URL}/define/{hash_value}"
        ) as response:

            data = await response.json()

        algorithms = data["algs"]

        print("Возможные алгоритмы:")
        for alg in algorithms:
            print(alg)

        create_tasks = [
            create_task(session, hash_value, algorithm)
            for algorithm in algorithms
        ]

        task_infos = await asyncio.gather(*create_tasks)

        result_tasks = [
            wait_for_password(session, task_id, algorithm)
            for algorithm, task_id in task_infos
        ]

        results = await asyncio.gather(*result_tasks)

        print("Пароли:")

        for algorithm, password in results:
            print(f"{algorithm}: {password}")


if __name__ == "__main__":
    asyncio.run(main())
