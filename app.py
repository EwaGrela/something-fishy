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
        auth = request.authorization
        cookie = request.cookies
        if not cookie.get('login_cookie'):
            return "please authenticate"
        return f(*args, **kwargs)
    return decorated




@app.route("/")
def home():
	return "sum fanatics vs szczupak hooligans"

@app.route("/login", methods=["POST"])
def login():
	if request.authorization and request.authorization.username ==user["login"] and request.authorization.password ==user["pass"]:
		#login_cookie = request.cookies.get('login_cookie')
		session['username'] = request.authorization.username
		session['fishes'] = app.config['fishes']
		resp = redirect('hello')
		#resp.set_cookie("login_cookie", "login cookie")
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
	#resp.set_cookie("login_cookie", "", expires=0)
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
#	global fishes
#	fish = json.dumps(fishes, sort_keys=True, indent=4)
	fish = json.dumps(session['fishes'], indent=4)
	return fish

def post_fish():
	data = request.get_json()
	new_fish = {
 		"who": data.get("who"),
 		"where": data.get("where"),
 		"mass": data.get("mass"),
 		"length": data.get("length"),
 		"kind": data.get("kind")
    }
#	global fishes
#	index = "id_" + str(len(fishes)+1)
#	fishes[index] = new_fish
	index = "id_" + str(len(session['fishes'])+1)

	session['fishes'][index] = new_fish
	session.modified = True
	print("AFTER ADD FISHES: '{}'".format(session['fishes']))
	return "OK"
    
@app.route("/fishes/<id>", methods=["GET", "PATCH", "PUT", "DELETE"])
@auth_required
def single_fish(id):
	print("ACCESS SINGLE FISH")
	print("FISHES: '{}'".format(session['fishes']))
	if request.method=="GET":
		return get_single_fish(id)
	elif request.method =="PUT":
		return put_single_fish(id)
	elif request.method=="DELETE":
		return delete_single_fish(id)
	elif request.method=="PATCH":
		return patch_single_fish(id)


def get_single_fish(id):
	idx = "id_"+ str(id)
	# global fishes
	print("FISHES: '{}'".format(session['fishes']))
	print("IDX: {}".format(idx))
	single_fish = json.dumps(session['fishes'].get(idx), indent=4)
	return single_fish

def put_single_fish(id):
	idx = "id_"+ str(id)
	data = request.get_json()
	new_fish = {
 		"who": data.get("who"),
 		"where": data.get("where"),
 		"mass": data.get("mass"),
 		"length": data.get("length"),
 		"kind": data.get("kind")
    }
	# global fishes
	print("FISHES: '{}'".format(session['fishes']))
	print("IDX: {}".format(idx))
	session['fishes'][idx] = new_fish
	session.modified = True
	return "ok"
	
def delete_single_fish(id):
	idx = "id_"+ str(id)
	# global fishes
	print("FISHES: '{}'".format(session['fishes']))
	print("IDX: {}".format(idx))
	del session['fishes'][idx]
	session.modified = True
	return "ok"


def patch_single_fish(id):
	idx = "id_"+ str(id)
	data = request.get_json()
	# global fishes
	print(list(data.keys()))
	for i in list(data.keys()):
		session['fishes'][idx][i] = data[i]
		session.modified = True
	return "ok"

app.secret_key = "fsgagfsfs78qgf784ewgfcdsf"

if __name__ == '__main__':
	app.run(debug=True, threaded=False)