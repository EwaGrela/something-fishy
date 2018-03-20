from flask import Flask, render_template, request, Response, make_response, redirect, session
import json
from functools import wraps

app = Flask(__name__)

user = {
	"login": "Akwarysta69",
	"pass":"J3si07r"
}

app.config['fishes'] = {
    "id_1": {
        "who": "Znajomy",
        "where": {
            "lat": 0.001,
            "long": 0.002
        },
        "mass": 34.56,
        "length": 23.67,
        "kind": "szczupak"
    },
    "id_2": {
        "who": "Kolega kolegi",
        "where": {
            "lat": 34.001,
            "long": 52.002
        },
        "mass": 300.12,
        "length": 234.56,
        "kind": "sum olimpijczyk"
    }
}

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('username'):
            return "please authenticate"
        return f(*args, **kwargs)
    return decorated

@app.route("/")
def home():
	return "sum fanatics vs szczupak hooligans"

@app.route("/login", methods=["POST"])
def login():
	if request.authorization and request.authorization.username ==user["login"] and request.authorization.password ==user["pass"]:
		session['username'] = request.authorization.username
		session['fishes'] = app.config['fishes']
		resp = redirect('hello')
		return resp
	return make_response('not verified!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@app.route("/hello")
@auth_required
def hello():
	usr = user["login"]
	return make_response(
			render_template("hello_template.html", user=usr)
		)

@app.route("/logout", methods=["POST"])
@auth_required
def logout():
	resp = make_response("logged out", 200 )
	session.pop('username', None)
	session.pop('fishes', None)
	return resp

@app.route("/fishes", methods=["GET", "POST"])
@auth_required
def fishy():
	if request.method =="GET":
		return get_fish()
	elif request.method=="POST":
		return post_fish()

def get_fish():
	# kinds = ",".join(sorted([i.get("kind") for i in session["fishes"].values()], key=lambda s: s.lower()))
	kinds = ",".join([i.get("kind") for i in session["fishes"].values()])
	kinds = json.dumps(kinds, indent=4)
	return kinds

def post_fish():
	data = request.get_json()
	new_fish = {
 		"who": data.get("who"),
 		"where": data.get("where"),
 		"mass": data.get("mass"),
 		"length": data.get("length"),
 		"kind": data.get("kind")
    }
	keys = [int(key.split("_")[1]) for key in sorted(session['fishes'].keys())]
	index = "id_" + str((keys[-1]+1))
	session['fishes'][index] = new_fish
	session.modified = True
	return "OK"
    
@app.route("/fishes/<id>", methods=["GET", "PATCH", "PUT", "DELETE"])
@auth_required
def single_fish(id):
	if request.method=="GET":
		return get_single_fish(id)
	elif request.method =="PUT":
		return put_single_fish(id)
	elif request.method=="DELETE":
		return delete_single_fish(id)
	elif request.method=="PATCH":
		return patch_single_fish(id)


def get_single_fish(id):
	idx = str(id)
	single_fish = json.dumps(session['fishes'].get(idx), indent=4)
	return single_fish

def put_single_fish(id):
	idx = str(id)
	data = request.get_json()
	new_fish = {
 		"who": data.get("who"),
 		"where": data.get("where"),
 		"mass": data.get("mass"),
 		"length": data.get("length"),
 		"kind": data.get("kind")
    }
	session['fishes'][idx] = new_fish
	session.modified = True
	return "OK"
	
def delete_single_fish(id):
	idx = str(id)
	del session['fishes'][idx]
	session.modified = True
	return "OK"


def patch_single_fish(id):
	idx = str(id)
	data = request.get_json()
	for i in list(data.keys()):
		session['fishes'][idx][i] = data[i]
		session.modified = True
	return "OK"

app.secret_key = "fsgagfsfs78qgf784ewgfcdsf"

if __name__ == '__main__':
	app.run(debug=True, threaded=False)