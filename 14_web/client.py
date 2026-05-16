import asyncio
import time

from aiohttp import ClientSession


URL = "http://127.0.0.1:8003"


async def solve_hash(session, hash_value, algorithm):
    params = {
        "hash": hash_value,
        "algorithm": algorithm
    }

    async with session.get(f"{URL}/solve", params=params) as response:
        data = await response.json()

    return algorithm, data["solve"]


async def main():
    hash_value = "c4ca4238a0b923820dcc509a6f75849b"

    async with ClientSession() as session:
        async with session.get(f"{URL}/define/{hash_value}") as response:
            data = await response.json()

        algorithms = data["algorithms"]
        print("Algorithms:", algorithms)

        tasks = [
            solve_hash(session, hash_value, algorithm)
            for algorithm in algorithms
        ]

        results = await asyncio.gather(*tasks)

        for algorithm, password in results:
            print(f"{algorithm}: {password}")


if __name__ == "__main__":
    asyncio.run(main())