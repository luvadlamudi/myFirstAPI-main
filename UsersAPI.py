#import libraries
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

users = []
#establish routes
@app.route('/login')
def login():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        for user in users:
            if(user["username"] == username and user["password"] == password):
                return jsonify(True)
        return jsonify(False)
    except:
        return "An error has occured"

@app.route('/addCredentials')
def addUser():
    username = request.args.get('username')
    password = request.args.get('password')
    users.append({"username": username, "password": password})
    return "Success"

 
if __name__ == '__main__':
    app.run(host='0.0.0.0')