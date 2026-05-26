from aiohttp import web
import asyncio
import random

from hident import long_solve_hash, identify_hashes


routes = web.RouteTableDef()

tasks: dict[int, asyncio.Task] = {}

ERR_TASK_NOT_FOUND = {
    "code": 1000,
    "message": "task not found"
}

ERR_TASK_NOT_FINISHED = {
    "code": 1001,
    "message": "task not finished"
}

@routes.get('/define/{hash}')
async def define(request: web.Request) -> web.Response:
    input_hash = request.match_info['hash']

    algorithms = identify_hashes(input_hash)

    return web.json_response({
        "algs": algorithms
    })

@routes.get('/createSolveTask')
async def create_solve_task(request: web.Request) -> web.Response:
    input_hash = request.query.get("hash")
    algorithm = request.query.get("algorithm")

    if not input_hash or not algorithm:
        return web.json_response(
            {"error": "необходимо указать hash и algorithm"},
            status=400
        )
    

    task = asyncio.create_task(
        long_solve_hash(input_hash, algorithm)
    )

    task_id = random.randint(10000, 99999)
    tasks[task_id] = task

    return web.json_response({
        "taskId": task_id
    })

@routes.get('/getPassword')
async def get_password(request: web.Request) -> web.Response:
    task_id = request.query.get("taskId")
    
    if not task_id:
        return web.json_response({
            "password": None,
            "err": ERR_TASK_NOT_FOUND
        })
    
    task_id = int(task_id)

    if task_id not in tasks:
        return web.json_response({
            "password": None,
            "err": ERR_TASK_NOT_FOUND
        })

    task = tasks[task_id]
    
    if not task.done():
        return web.json_response({
            "password": None,
            "err": ERR_TASK_NOT_FINISHED
        })

    password = task.result()

    return web.json_response({
        "password": password,
        "err": None
    })

if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)

    web.run_app(app, host="0.0.0.0", port=8003)