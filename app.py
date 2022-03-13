from flask import Flask, request, jsonify, make_response

import chat as theChat
import auth as Auth

import jwt
import datetime
import time

app = Flask(__name__)

app.config['SECRET_KEY'] = '7jP0F8825ArNv21jLlu7fzXgkM98pTD5GkgAtuYdkv57tXGCZwqzgSG5uF8Llv5' 

def encode_jwt(json, secret = app.config['SECRET_KEY']):
    return jwt.encode(json, secret, algorithm = 'HS256')

def is_decode_jwt(token, secret = app.config['SECRET_KEY']):
    try:
        return jwt.decode(token, secret, algorithms = ['HS256'])
    except:
        return False

def is_token_expired(token, secret = app.config['SECRET_KEY']):
    jwtToken = jwt.decode(token, secret, algorithms = ['HS256'])
    now = int(time.time())
    if jwtToken['exp'] < now:
        return True
    return False


@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        # create time now
        now = int(time.time())
        json = {
            'username' : 'admin',
            'iat'   : now,
            'exp'   : now + 3600 * 24 * 7
        }
        return encode_jwt(json)
    else:
        # redirect to front end chat    
        name = 'ade'
        return 'Hello ' + name

# @app.route('/greeting/<name>', methods=['GET'])
# def greeting(name):
#     token = None
#     # jwt is passed in the request header
#     if 'x-access-token' in request.headers:
#         token = request.headers['x-access-token']
    
#     if not token:
#         return jsonify({'message' : 'Token is missing!'}), 401
    
#     if not is_decode_jwt(token):
#         return jsonify({'message' : 'Token is invalid!'}), 401
    
#     try:
#         greeting = theChat.greeting(name)
#     except:
#         return jsonify({'message' : 'error function!'}), 500
    
#     return jsonify({'message' : f'{greeting}'}), 200

@app.route('/get/token', methods=['GET'])
def get_token():
    now = int(time.time())
    json = {
        'username' : 'admin',
        'iat'   : now,
        'exp'   : now + 3600 * 24 * 7
    }
    return encode_jwt(json)

@app.route('/ask', methods=['POST'])
def ask():
    token = None
    # jwt is passed in the request header
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']
    
    if not token:
        return jsonify({'message' : 'Token is missing!'}), 401
    
    if not is_decode_jwt(token):
        return jsonify({'message' : 'Token is invalid!'}), 401
    
    if is_token_expired(token):
        return jsonify({'message' : 'Token is expired!'}), 401

    # get the http body message { 'message' : 'a sentance'}
    body = request.get_json()
    if not body:
        return jsonify({'message' : 'No message!'}), 401
    
    if not 'message' in body:
        return jsonify({'message' : 'No message!'}), 401
    
    try:
        response = theChat.ask(body['message'])
    except:
        return jsonify({'message' : 'error function!'}), 500

    return jsonify({'message' : f'{response}'}), 200

if __name__ == '__main__':
    app.run(debug=True)