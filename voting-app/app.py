from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
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
        if request.form['cats'] == 'Cats' and 'cats' != request.cookies.get('vote'):
            try:
                cats = redis.incr('cats')
                if 'dogs' == request.cookies.get('vote'):
                    dogs = redis.decr('dogs');
                redis.publish('pubsub', '{"cats":'+str(cats)+', "dogs":'+str(dogs)+'}')
            except Exception as e:
                print e
                cats = "<i>An error occured</i>"
            resp =  make_response(render_template('index.html', name=os.getenv('NAME', "Dogs")))
            resp.set_cookie('vote', 'cats')
            return resp
        if request.form['cats'] == 'Dogs' and 'dogs' != request.cookies.get('vote'):
            try:
                dogs = redis.incr('dogs')
                if 'cats' == request.cookies.get('vote'):
                    cats = redis.decr('cats');
                redis.publish('pubsub', '{"cats":'+str(cats)+', "dogs":'+str(dogs)+'}')
            except Exception as e:
                print e
                dogs = "<i>An error occured</i>"
            resp =  make_response(render_template('index.html', name=os.getenv('NAME', "Dogs")))
            resp.set_cookie('vote', 'dogs')
            return resp
        else:
            return render_template('index.html', name=os.getenv('NAME', "Dogs"), visits=visits)
    elif request.method == 'GET':
        return render_template('index.html', name=os.getenv('NAME', "Dogs"), visits=visits)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
