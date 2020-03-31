from flask import Flask, jsonify, abort, request
import urllib.request, json, os
from github import Github

app = Flask(__name__)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
DEBUG = os.getenv('DEBUG')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

g = Github(CLIENT_ID, CLIENT_SECRET)

@app.route('/')
def get_repos():
    r = []

    try:
        args = request.args
        n = int(args['n'])
    except (ValueError, LookupError) as e:
        abort(jsonify(error="Please  provide the 'n' parameter"))

    repositories = g.search_repositories(query='language:python')[:n]

    try:
        for repo in repositories:
            with urllib.request.urlopen(repo.url) as url:
                data = json.loads(url.read().decode())
            r.append(data)
        return jsonify({
            'repos':r,
            'status': 'ok'
            })
    except IndexError as e:
        return jsonify({
          'repos':r,
          'status': 'ko'
        })

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
