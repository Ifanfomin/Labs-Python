from typing import List


def batched(iterable: List, n) -> List[List]:
    result = [[] for _ in range(n)]
    for i, v in enumerate(iterable):
        chunk_id = i % n
        result[chunk_id].append(v)
    return result
