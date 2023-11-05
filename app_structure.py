from flask import (Flask, jsonify, request)
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

import requests
import config

app = Flask(__name__)

# #################### AUTH PROCESS ##########################
# security mechanisms used in web applications to protect against Cross-Site Request 
app.secret_key = config.JWT_SECRET_KEY
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
jwt = JWTManager(app)

def get_is_auth():
    return config.jwt_token != "" 

# the 'Authorization' header with the JWT token 
def authorized_request():
    
    headers = {
        'Authorization': f"Bearer {config.jwt_token}"
    }

    # Make an HTTP GET request to the API with the 'Authorization' header
    request_url = request.url_root + "/protected"
    response = requests.get(request_url, headers=headers)
    if response.status_code != 200:
        config.jwt_token = ""

    return response.status_code

# #################### DECORATOR ##########################
# Custom authentication decorator
def requires_authentication(func):
    def decorated_function(*args, **kwargs):
        auth_result = authorized_request()
        if (auth_result != 200):
            return "http://127.0.0.1:5000/login" 
    
        return func(*args, **kwargs)
    return decorated_function

def is_access_from_postman():
    user_agent = request.headers.get('User-Agent')
    substring = "Postman"
    return substring in user_agent

def allow_access_only_browser(func):
    def decorated_function(*args, **kwargs): 
        if is_access_from_postman():
            return "Postman can't access to this URL"
        return func(*args, **kwargs)
    return decorated_function


# #################### ENDPOINT - AUTH PROCESS ##########################
@app.route("/protected", methods=["GET"], endpoint="protected")
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route("/login", methods=["GET","POST"], endpoint="login")
@allow_access_only_browser
def login():
    config.jwt_token = create_access_token(identity=config.JWT_SECRET_KEY)
    return "authorization has been successfully "

@app.route("/logout", endpoint="logout")
@allow_access_only_browser
def logout():
    config.jwt_token = ""
    return "You have logout !! "

# #################### BACKEND : TASK ##########################
# 1. GET /tasks: Retrieves all tasks. For an "VG" (Very Good) requirement, add a "completed" parameter to filter by completed or uncompleted tasks.
# 2. POST /tasks: Adds a new task. The task is initially uncompleted when first added.
@app.route("/tasks/", methods=["POST","GET"])
def tasks():
    return "do tasks()"

@app.route("/tasks/completed/", methods=["GET"])
def completed():
    return "do completed()" 

# 3. GET /tasks/{task_id}: Retrieves a task with a specific ID.
# 4. DELETE /tasks/{task_id}: Deletes a task with a specific ID.
# 5. PUT /tasks/{task_id}: Updates a task with a specific ID.
@app.route("/tasks/<int:task_id>", methods=["GET", "DELETE", "PUT"])
def get_task(task_id):
    return "do get_task(task_id)"
    
# 6. PUT /tasks/{task_id}/complete: Marks a task as completed.
@app.route("/tasks/<int:task_id>/complete", methods=["PUT"])
def set_task_completed(task_id):
    return "do set_task_completed(task_id)"

# 7. GET /tasks/categories/: Retrieves all different categories.
@app.route("/tasks/categories", methods=["GET"])
def get_task_by_category():
    return "do get_task_by_category()"

 # 8. GET /tasks/categories/{category_name}: Retrieves all tasks from a specific category.
@app.route("/tasks/categories/<string:category_name>")
def search_task_by_category(category_name): 
    return "do search_task_by_category(category_name)"


# #################### BACKEND : CATEGORY ##########################
# 9. GET /tasks/categories/: Retrieves all categories
# 10. POST /tasks/categories/: Adds a new category
@app.route("/tasks/categories/", methods=["POST","GET"])
def categories():
    return "do categories()"

# 11. GET /tasks/categories/<int:category_id>: Retrieves a category with a specific ID.
# 12. DELETE /tasks/categories/<int:category_id>: Deletes a category with a specific ID.
# 13. PUT /tasks/categories/<int:category_id>: Updates a category with a specific ID.
@app.route("/tasks/categories/<int:category_id>", methods=["GET", "DELETE", "PUT"])
def get_category(category_id):
    return "do get_category(category_id)"


# #################### ENDPOINT - FRONTEND ##########################
# -------- LIST ITEMS  ------------
@app.route("/", endpoint="home")
@allow_access_only_browser
def home(): 
    return "do home()"

# -------- ITEM DETAIL  ------------
@app.route("/todo/<int:task_id>/detail", methods=["GET"] ,endpoint="detail_tasks")
@allow_access_only_browser
def detail_tasks(task_id):
    return "do detail_tasks()"

# -------- NEW ITEM  ------------
@app.route("/todo/new", methods=["GET", "POST"], endpoint="new_tasks")
@allow_access_only_browser
@requires_authentication
def new_item():
    return "do new_item()"


# -------- UPDATE ITEM  ------------
@app.route("/todo/<int:task_id>/edit", methods=["GET", "POST"], endpoint="edit_tasks")
@allow_access_only_browser
@requires_authentication
def edit_item(task_id):
    return "do edit_item(task_id)"
        
# -------- COMPLATE TASK -------
#@app.route("/todo/<int:task_id>/complate", methods=["POST"], endpoint="complete_tasks")
@app.route("/todo/<int:task_id>/complate", methods=["GET"], endpoint="complete_tasks")
@allow_access_only_browser
@requires_authentication
def set_task_completed(task_id):
    return "do set_task_completed(task_id)"
    
# -------- DELETE ITEM  ------------
# @app.route("/todo/<int:task_id>/delete", methods=["POST"], endpoint="delete_tasks")
@app.route("/todo/<int:task_id>/delete", methods=["GET"], endpoint="delete_tasks")
@requires_authentication
def delete_tasks(task_id): 
    return "do delete_tasks(task_id)"

# -------- ERROR HANDLER  ------------
def page_404(e):
    if is_access_from_postman():
        return "404: Page Not Found"
    else:
        return 'render_template("errors/404.html", is_authen = get_is_auth())'

def page_405(e):
    if is_access_from_postman():
        return "405: Method Not Allowed"
    else:
        return 'render_template("errors/405.html", is_authen = get_is_auth())'

def page_401(e):
    if is_access_from_postman():
        return "401: Unauthorized Error"
    else:
        return 'render_template("errors/401.html", is_authen = get_is_auth())'

app.register_error_handler(404, page_404)
app.register_error_handler(405, page_405)
app.register_error_handler(401, page_401)
