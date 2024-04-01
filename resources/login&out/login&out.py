from app import app
from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager

jwt = JWTManager(app)

@app.post('/login')
def make_token():
    data = request.get_json()
    email = request.json.get(data["email"], None)
    password = request.json.get(data["password"], None)
    if email != "test" or password != "test":
        return {"msg" : "Wrong email or password"}, 401
    
    access_token = create_access_token(identity=email)
    response = {"access token" : access_token}
    return response

@app.post('/logout')
def del_token():
    response = jsonify({"message" : "logout successful"})
    unset_jwt_cookies(response)
    return response