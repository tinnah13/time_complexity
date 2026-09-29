from flask import Flask, request
from flask_jwt_extended import JWTManager, jwt_required
from flask_jwt_extended import create_access_token
import base64
import json
from algorithm import time_complexity_visualizer
from algorithm import linear_search, bubble_sort, binary_search, nested_loop, two_pointer, unique_users
from stk import stack, push, pop, peep, is_empty
from stk import push_algorithm, pop_algorithm, peep_algorithm, isempty_algorithm
from que import queue, enqueue, dequeue, peek, queis_empty
from que import enqueue_algorithm, dequeue_algorithm, peek_algorithm, queis_empty_algorithm
from algo_db import Analysis, db

algorithms = {
    "linear_search" : linear_search,
    "bubble_sort" : bubble_sort,
    "binary_search" : binary_search,
    "nested_loop" : nested_loop,
    "two_pointer" : two_pointer,
    "unique_users" : unique_users,
    "push_algorithm" : push_algorithm,
    "pop_algorithm" : pop_algorithm,
    "peep_algorithm" : peep_algorithm,
    "isempty_algorithm" : isempty_algorithm,
    "enqueue_algorithm" : enqueue_algorithm,
    "dequeue_algorithm" : dequeue_algorithm,
    "peek_algorithm" : peek_algorithm,
    "queis_empty_algorithm" : queis_empty_algorithm
}

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "your-secret-key"
jwt = JWTManager(app)
@jwt.unauthorized_loader
def unauthorized_error(error):
    return {
        "message": "I don't know you"
    }, 401

db.init_app(app)
with app.app_context():
    db.create_all()
@app.route("/analyze")

def analyze():
    algo = request.args.get("algo")
    step = request.args.get("step", type=int)
    n_max = request.args.get("n_max", type=int)

    algorithm = algorithms.get(algo)

    image = time_complexity_visualizer(algorithm, 0, n_max, step)

    with open(image, "rb") as image_file:
        imagebinary = base64.b64encode(image_file.read()).decode("utf-8")

    return {
        "algorithm" : algo,
        "step" : step,
        "n_max" : n_max,
        "image" : imagebinary
    }

@app.route('/login', methods=['GET'])
def login():
    token = create_access_token(identity="user")
    return {
        "access token": token
    }
@app.route('/save', methods=['POST'])
@jwt_required()
def saveanalysis():
    data = request.get_json()
    analysis = Analysis(
        algorithm = data["algo"],
        step = data["step"],
        n_max = data["n_max"]
        )

    db.session.add(analysis)
    db.session.commit() 

    return{"message": "Analysis saved successfully"}

if __name__ == "__main__":
    app.run(port=5000)
