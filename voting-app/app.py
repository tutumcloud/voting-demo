from flask import Flask
from flask import render_template
from flask import request
from redis import Redis, RedisError
import os
import socket

# Connect to Redis
redis = Redis(host="redis", db=0, password=os.environ.get('REDIS_ENV_REDIS_PASS'))

app = Flask(__name__)

redis.set("dogs", 0)
redis.set("cats", 0)

@app.route("/", methods=['POST','GET'])
def hello():
    try:
        dogs = redis.get("dogs")
        cats = redis.get("cats")
        visits = redis.incr('counter')
    except RedisError:
        dogs = "<i>cannot connect to Redis, counter disabled</i>"
        cats = "<i>cannot connect to Redis, counter disabled</i>"
        visits = "<i>cannot connect to Redis, counter disabled</i>"
    if request.method == 'POST':
        if request.form['cats'] == 'Cats':
            try:
                cats = redis.incr('cats')
            except Exception as e:
                print e
                cats = "<i>An error occured</i>"
            return render_template('index.html', name=os.getenv('NAME', "Dogs"), hostname=socket.gethostname(), visits=visits, dogs=dogs, cats=cats)
        if request.form['cats'] == 'Dogs':
            try:
                dogs = redis.incr('dogs')
            except Exception as e:
                print e
                dogs = "<i>An error occured</i>"
            return render_template('index.html', name=os.getenv('NAME', "Dogs"), hostname=socket.gethostname(), visits=visits, dogs=dogs, cats=cats)
    elif request.method == 'GET':
        return render_template('index.html', name=os.getenv('NAME', "Dogs"), hostname=socket.gethostname(), visits=visits, dogs=dogs, cats=cats)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
