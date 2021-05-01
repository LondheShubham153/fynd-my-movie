from aiohttp import web
import movie_utils as movi
import logging
import aiosqlite
import json
from aiohttp_tokenauth import token_auth_middleware
import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s -%(message)s', 
                    datefmt='%d-%b-%y %H:%M')

routes = web.RouteTableDef()

# This is the API end point for App to give health check status
@routes.get('/')
async def healthcheck_handler(re):
    """
    ---
    description: This end-point allow to test that service is up.
    tags:
    - Health check
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation. Return "up" text
        "405":
            description: invalid HTTP Method
    """
    return web.json_response({'status': 'up'}, status=200)

# This is the API end point for App to get data
@routes.get('/movies')
async def get_handler(request):
    """
    ---
    description: This end-point allow to get all the movies from the db.
    You can even pass search in query params to search your favourite movie
    tags:
    - Get all movies
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation. Return movies
        "405":
            description: invalid HTTP Method
    """
    result = []
    query = request.rel_url.query.get('search',None)
    db = request.config_dict["DB"]
    if query:
        get_query = "SELECT rowid, json_extract(data, '$.99popularity', '$.director', \
    '$.genre', '$.imdb_score', '$.name') FROM movies WHERE json_extract(data,'$.name') LIKE '%"+query+"%'"
    else:
        get_query = "SELECT rowid, json_extract(data, '$.99popularity', '$.director', \
    '$.genre', '$.imdb_score', '$.name') FROM movies"
    async with db.execute(get_query) as cursor:
        async for row in cursor:
            movie_id = row[0]
            data = json.loads(row[1])
            response_obj = movie.lookup_result(movie_id,data)
            result.append(
                response_obj
            )
    return web.json_response({"status": "ok", "data": result})

# This is the API end point for App to upload data
@routes.post('/movies')
async def post_handler(request):
    """
    ---
    description: This end-point allow to Add a movie int the db, you need admin access to use the API.
    tags:
    - Add moviek
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation. Return 'Uploaded movie' text
        "405":
            description: invalid HTTP Method
    """
    try:
        payload = await request.json()
        keys = ['99popularity', 'director', 'genre', 'imdb_score', 'name']
        assert movie.validate_query(list(payload.keys()), keys),\
         "A required key is missing in the body"
        db = request.config_dict["DB"]
        async with db.execute(
            "INSERT INTO movies (data) VALUES(?)", [json.dumps(payload)]
        ) as cursor:
            movie_id = cursor.lastrowid
        await db.commit()
        response_obj = {'message': 'success',
                        'movie_id': movie_id,
                        'detail': 'message: Uploaded movie data to the DB'}
        return web.json_response(response_obj, status=200)
    except Exception as e:
        response_obj = {'status': 'error', 'message': str(e)}
        return web.json_response(response_obj, status=500)

# This is the API end point for App to get data
@routes.get('/movies/{id}')
async def get_by_id_handler(request):
    """
    ---
    description: This end-point allow to get any movie by movie's id.
    tags:
    - Get movie by id
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation. Returns movie object for given movie id
        "405":
            description: invalid HTTP Method
    """
    ret = []
    db = request.config_dict["DB"]
    movie_id = str(request.match_info["id"])
    get_query = "SELECT json_extract(data, '$.99popularity', '$.director', \
    '$.genre', '$.imdb_score', '$.name') FROM movies WHERE rowid ="+movie_id
    async with db.execute(get_query) as cursor:
        row = await cursor.fetchone()
        if row is None:
            return web.json_response(
                    {"status": "fail", "reason": f"Movie {movie_id} doesn't exist"},
                    status=404,
                )
        data = json.loads(row[0])
        response_obj = movie.lookup_result(movie_id,data)
        ret.append(
            response_obj
        )
    return web.json_response({"status": "ok", "data": ret})

# This is the API end point for App to edit data
@routes.put('/movies/{id}')
async def put_handler(request):
    """
    ---
    description: This end-point allow to update a given movie by it's id.
    tags:
    - Edit movie
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation. Return "Updated movie" text
        "405":
            description: invalid HTTP Method
    """
    try:
        movie_id = request.match_info["id"]
        payload = await request.json()
        keys = ['99popularity', 'director', 'genre', 'imdb_score', 'name']
        assert movie.validate_query(list(payload.keys()), keys),\
         "A required key is missing in the body"
        db = request.config_dict["DB"]
        update_query = f"UPDATE movies set data =(\
                        SELECT json_set(data, '$.99popularity',{payload['99popularity']},\
                                '$.director','{payload['director']}',\
                                '$.genre',json_array({str(payload['genre'])[1:-1]}),\
                                '$.imdb_score',{payload['imdb_score']},\
                                '$.name','{payload['name']}')\
                                FROM movies where rowid={movie_id}) where rowid={movie_id}"
        async with db.execute(update_query) as cursor:
            pass
        await db.commit()
        response_obj = {'message': 'success',
                        'movie_id': movie_id,
                        'detail': 'message: Updated movie data to the DB'}
        return web.json_response(response_obj, status=200)
    except Exception as e:
        response_obj = {'status': 'error', 'message': str(e)}
        return web.json_response(response_obj, status=500)

# This is the API end point for App to delete data
@routes.delete('/movies/{id}')
async def delete_handler(request):
    """
    ---
    description: This end-point allows to delete movie from the db by given id.
    tags:
    - Delete movie
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation. Returns "ok" text
        "405":
            description: invalid HTTP Method
    """
    try:
        movie_id = request.match_info["id"]
        db = request.config_dict["DB"]
        delete_query = "DELETE FROM movies WHERE rowid = ?"
        async with db.execute(delete_query, [movie_id]) as cursor:
            if cursor.rowcount == 0:
                return web.json_response(
                    {"status": "fail", "reason": f"Movie {movie_id} doesn't exist"},
                    status=404,
                )
        await db.commit()
        return web.json_response({"status": "ok", "id": movie_id})

    except Exception as e:
        response_obj = {'status': 'error', 'message': str(e)}
        return web.json_response(response_obj, status=500)

async def init_db(app: web.Application):
    """
    ---
    description: This method allows to initialize the sqlite database.
    tags:
    - initialize database
    produces:
    - database connection object
    """
    sqlite_db = movie.get_db_path()
    db = await aiosqlite.connect(sqlite_db)
    db.row_factory = aiosqlite.Row
    app["DB"] = db
    yield
    await db.close()

def init_app(argv=None):
    app = web.Application(middlewares=[token_auth_middleware(movie.admin_loader,
                                    exclude_methods=('GET',))
                                ])
    app.add_routes(routes)
    app.cleanup_ctx.append(init_db)
    web.run_app(app,port=os.environ['PORT'])
    return app

movie.try_make_db()
app = init_app()
