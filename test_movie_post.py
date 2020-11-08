import requests
import json


def test_get_headers_movie():

    url = "https://fynd-my-movie.herokuapp.com/movies"
    payload={}
    headers = {}

    resp = requests.request("GET", url, headers=headers, data=payload)
    assert resp.status_code == 200


def test_get_search_headers_movie():

    url = "https://fynd-my-movie.herokuapp.com/movies?search=shutter"
    payload={}
    headers = {}

    resp = requests.request("GET", url, headers=headers, data=payload)
    assert resp.status_code == 200

def test_post_headers_movie():

    url = "https://fynd-my-movie.herokuapp.com/movies"
    token = "admin-login-token"
    payload="{\n    \"99popularity\": 92.0,\n    \"director\": \"Stanley Kuberick\",\n    \"genre\": [\n      \"Sci-fy\",\n      \"Drama\"\n    ],\n    \"imdb_score\": 9.5,\n    \"name\": \"A.I\"\n}"
    headers = {
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json'
    }

    resp = requests.request("POST", url, headers=headers, data=payload)
    assert resp.status_code == 200


def test_put_headers_movie():

    url = "https://fynd-my-movie.herokuapp.com/movies/1"
    token = "admin-login-token"
    payload="{\n    \"99popularity\": 84.0,\n    \"director\": \"Victor Frank.\",\n    \"genre\": [\n      \"Adventure\",\n      \" Family\",\n      \" Fantasy\"\n    ],\n    \"imdb_score\": 8.3,\n    \"name\": \"The Wizard of Oz\"\n}"
    headers = {
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json'
    }

    resp = requests.request("PUT", url, headers=headers, data=payload)
    assert resp.status_code == 200
    

def test_delete_headers_movie():

    url = "https://fynd-my-movie.herokuapp.com/movies/252"
    token = "admin-login-token"
    payload={}
    headers = {
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json'
    }

    resp = requests.request("DELETE", url, headers=headers, data=payload)
    assert resp.status_code == 200
    