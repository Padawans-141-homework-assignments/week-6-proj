from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, unset_jwt_cookies, JWTManager

from flask.views import MethodView
from flask_smorest import abort

from app import app
from models.user_model import userModel
from schemas import userSchema
from . import bplog

#sets the secret key for the JWT to decode against
app.config['JWT_SECRET_KEY'] = "This is a scret key. Don't give this to anyone!"

jwt = JWTManager(app)

#route for logging in for registered users
@bplog.post('/login')
def usr_login():
    
    #grabs the user data
    usr = request.get_json()

    #grabs the username from the user data
    username = usr['username']

    #checks the tabe for a row with a username that matches the 
    #username the user sent.
    user = userModel.query.filter_by(username = username).first()

    #if there is a username match and a password match
    if user and user.check_usr_password(usr['password']):
        #an access token is made with the username being the token header
        usr_token = create_access_token(identity=username)
        return {'Access token' : usr_token}, 201
    
    #aborts if nothing matches
    abort(400, message = 'Either username or password is invalid.')

#route for logging out user
@bplog.post('/logout')
def usr_logout():
    
    #confirms successful logout
    response = jsonify({'Confirmation' : "You have logged out successfully."})
    #deletes any cookies/tokens still in the client
    unset_jwt_cookies(response)
    return response

#gets all the registered users
@bplog.route('/signup')
class signupResourceList(MethodView):

    @bplog.response(200, userSchema(many=True))

    def get(self):

        try:
            return userModel.query.all(), 200
        except:
            abort(400, message = "Couldn\'t get information from db.")


    @bplog.arguments(userSchema)
    @bplog.response(201, userSchema)

    #creates new user in the database
    def post(self, data):

        try:
            #calls in the user model
            login = userModel()
            #forms the user data
            login.from_usr(data)
            #saves the formed user data to the database
            login.save_usr()
            return jsonify({"confirmation" : "Your user information was created."}), 201
        except:
            #aborts is an error happens
            abort(400, message  = 'There was a problem entering the information into the database.')

#route for updating and deleting users
@bplog.route('/signup/<int:id>')
class signupResource(MethodView):
    @bplog.arguments(userSchema)
    def put(self, data, id):

        #grabs user information at the given id endpoint
        login = userModel.query.get(id)

        try:
            #forms the new user data in the endpoint location
            login.from_usr(data)
            #saves the new user data to the endpoint location
            login.save_usr()
            return {"confirmation" : "user info updated successfully."}, 200
        except:
            #returns error if it happens
            abort(400, message = "There was a problem updating user information.")
        
    
    def delete(self, id):

        #gets the information at the given id endpoint
        login = userModel.query.get(id)

        #if that endpoint exists
        if login:
            #delete that user at that endpoint
            login.del_usr()
            return{"Confirmation" : 'User is now deleted from the database.'}, 200
        else:
            #abort if an error shows up
            abort(400, message = 'User with that ID not in the database.')