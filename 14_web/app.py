from aiohttp import web
import json
from hident import long_solve_hash, identify_hashes


routes = web.RouteTableDef()


@routes.get('/define/{hash}')
async def define(request: web.Request) -> web.Response:
    hash = request.match_info['hash']
    algorithms = identify_hashes(hash)
    return web.Response(text=json.dumps({"algorithms": algorithms}), headers={'Content-Type': 'application/json'})


@routes.get('/solve')
async def solve(request: web.Request) -> web.Response:
    hash = request.query.get("hash")
    algorithm = request.query.get("algorithm")

    solve = await long_solve_hash(hash, algorithm)
    
    return web.Response(text=json.dumps({"solve": solve}), headers={'Content-Type': 'application/json'})


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host="0.0.0.0", port=8003)