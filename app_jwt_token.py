# #################### Sample how basic jwt web token works ##########################
from flask import (Flask, jsonify, request)
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import requests

class Config:
    JWT_SECRET_KEY = "YOUR SECRET KEY"
    jwt_token = ''
 
app = Flask(__name__)
# #################### SECURITY ##########################
# security mechanisms used in web applications to protect against Cross-Site Request 
app.secret_key = Config.JWT_SECRET_KEY
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
jwt = JWTManager(app)
 
# #################### AUTH PROCESS ##########################
# the 'Authorization' header with the JWT token 
def authorized_request():
    
    headers = {
        'Authorization': f"Bearer {Config.jwt_token}"
    }

    # Make an HTTP GET request to the API with the 'Authorization' header
    request_url = request.url_root + "/protected"
    response = requests.get(request_url, headers=headers)
    if response.status_code != 200:
        jwt_token = ""

    return response.status_code

def get_is_auth():
    return Config.jwt_token != "" 

# #################### DECORATOR ##########################
# Custom authentication decorator
def requires_authentication(func):
    def decorated_function(*args, **kwargs):
        auth_result = authorized_request()
        if (auth_result != 200):
            return "Requires authentication : http://127.0.0.1:5000/login"
    
        return func(*args, **kwargs)
    return decorated_function

# #################### ENDPOINT - AUTH PROCESS ##########################
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route("/login", endpoint="login")
def login():
    if not get_is_auth() :
        Config.jwt_token = create_access_token(identity=Config.JWT_SECRET_KEY)
        return "authorization has been successfully \nYou have got Token" 
    return "You ready have token"

@app.route("/logout", endpoint="logout")
def logout():
    Config.jwt_token = ""
    return "You have logout !! "
 
@app.route("/", endpoint="home")
def home(): 
    return ("Authorization Process \n " +
            "| Login : http://127.0.0.1:5000/login \n" + 
            "| Delete : http://127.0.0.1:5000/delete \n" + 
            "| Logout : http://127.0.0.1:5000/logout \n"
            )

@app.route("/delete")
@requires_authentication
def delete():
    return "Do delete process"

# -------- ERROR HANDLER  ------------
def page_404(e):
    return "404-Page not found"

def page_405(e):
    return "405-"

def page_401(e):
    return "401 -"

app.register_error_handler(404, page_404)
app.register_error_handler(405, page_405)
app.register_error_handler(401, page_401)

if __name__ == '__main__':
    app.run(debug=True)