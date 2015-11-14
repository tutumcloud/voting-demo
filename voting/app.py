from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from redis import Redis, RedisError
import os
import socket
import logging

# Connect to Redis
redis = Redis(host="redis", db=0)

app = Flask(__name__)

optionA = "Cats"
optionB = "Dogs"

name = optionA + " VS " + optionB

@app.route("/", methods=['POST','GET'])
def hello():
    try:
        dogs = redis.get(optionB)
        cats = redis.get(optionA)
        visits = redis.incr('counter')
    except RedisError:
        dogs = "<i>cannot connect to Redis, counter disabled</i>"
        cats = "<i>cannot connect to Redis, counter disabled</i>"
        visits = "<i>cannot connect to Redis, counter disabled</i>"
    if request.method == 'POST':
        if request.form['cats'] == 'Cats' and 'cats' != request.cookies.get('vote'):
            try:
                cats = redis.incr(optionA)
                if 'dogs' == request.cookies.get('vote') and int(dogs) > 0:
                    dogs = redis.decr(optionB);
                print cats
                redis.publish('pubsub', '{"'+optionA+'":'+str(cats)+', "'+optionB+'":'+str(dogs)+'}')
            except Exception as e:
                print e
                cats = "<i>An error occured</i>"
            resp =  make_response(render_template('index.html', name=os.getenv('NAME', name), hostname=socket.gethostname(), optionA=optionA, optionB=optionB))
            resp.set_cookie('vote', 'cats')
            return resp
        if request.form['cats'] == 'Dogs' and 'dogs' != request.cookies.get('vote'):
            try:
                dogs = redis.incr(optionB)
                if 'cats' == request.cookies.get('vote') and int(cats) > 0:
                    cats = redis.decr(optionA);
                print dogs
                redis.publish('pubsub', '{"'+optionA+'":'+str(cats)+', "'+optionB+'":'+str(dogs)+'}')
            except Exception as e:
                print e
                dogs = "<i>An error occured</i>"
            resp =  make_response(render_template('index.html', name=os.getenv('NAME', name), hostname=socket.gethostname(), optionA=optionA, optionB=optionB))
            resp.set_cookie('vote', 'dogs')
            return resp
        else:
            return render_template('index.html', name=os.getenv('NAME', name), hostname=socket.gethostname(), visits=visits, optionA=optionA, optionB=optionB)
    elif request.method == 'GET':
        return render_template('index.html', name=os.getenv('NAME', name), hostname=socket.gethostname(), visits=visits, optionA=optionA, optionB=optionB)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)
