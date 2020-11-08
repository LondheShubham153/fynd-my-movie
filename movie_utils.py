import requests
from collections import OrderedDict
import logging
import json
import aiosqlite
import sqlite3
from pathlib import Path
from typing import Any, AsyncIterator, Awaitable, Callable, Dict
import numpy as np

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s -%(message)s', 
                    datefmt='%d-%b-%y %H:%M')

def validate_query(passed_params, required_params):
    missing_params = np.setdiff1d(required_params, passed_params).tolist()
    if missing_params:
        logging.error("Invalid request.Missing Params: " + ','.join(missing_params))
        return False
    return True

def get_db_path():
    here = Path.cwd()
    return here / "db.sqlite3"

def try_make_db():
    sqlite_db = get_db_path()
    if sqlite_db.exists():
        return

    with sqlite3.connect(sqlite_db) as conn:
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE movies (data json)"""
        )
        conn.commit()

def lookup_result(movie_id,data):
    keys = ['movie_id','99popularity', 'director', 'genre', 'imdb_score', 'name']
    response_obj = OrderedDict.fromkeys(keys, '')

    if data == 'NO_RECORD_FOUND':
        return data
    response_obj['movie_id'] = movie_id
    response_obj['99popularity'] = data[0]
    response_obj['director'] = data[1]
    response_obj['genre'] = data[2]
    response_obj['imdb_score'] = data[3]
    response_obj['name'] = data[4]
    return response_obj

async def admin_loader(token):
    """
    Checks Admin Token, allows 2 levels of Accesss 
    admin = who can add, remove or edit movies.
    users = who can just view the movies.
    """
    admin = None
    if token == 'admin-login-token':
        admin = {'uuid': 'fake-uuid'}
    return admin
