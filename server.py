import os
from flask import Flask, send_from_directory, render_template, redirect

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)
listSing = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o']
exclude = ['el','la','los','les']

@app.route("/")
def home():
    sings = ['h','o','l','a']
    #retorna un objeto json
    return {
        "msg": "hola",
        "sings": sings
    }

@app.route('/<path:path>')
def all_routes(path):
    return redirect('/')

if __name__ == "__main__":
    app.run(port=port)
