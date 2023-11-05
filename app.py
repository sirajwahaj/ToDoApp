from html import unescape
from flask import (Flask, jsonify, request, 
                   render_template,redirect, url_for, flash)

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from functools import wraps

import requests
import config
import utility
import model

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
            return redirect(url_for("login")) 
    
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
    is_authen = get_is_auth()
    authForm = utility.AuthForm() 
    if not get_is_auth() :
        if request.method == "POST":
            config.jwt_token = create_access_token(identity=config.JWT_SECRET_KEY)
            flash("authorization has been successfully ", "success")
            return redirect(url_for("home"))
    
    return render_template("login.html", 
                           is_authen=is_authen, 
                           form=authForm)  

@app.route("/logout", endpoint="logout")
@allow_access_only_browser
def logout():
    config.jwt_token = ""
    flash("You have logout !! ", "success")
    return redirect(url_for("home"))



# #################### BACKEND : TASK ##########################
# 1. GET /tasks: Retrieves all tasks. For an "VG" (Very Good) requirement, add a "completed" parameter to filter by completed or uncompleted tasks.
# 2. POST /tasks: Adds a new task. The task is initially uncompleted when first added.
@app.route("/tasks/", methods=["POST","GET"])
def tasks():
    if request.method == "POST":
        new_task = {"id": model.get_max_id(is_task=True),
                "title": request.form['title'],
                "description": request.form['description'],
                "category": request.form['category'],
                "status": "Pending"
                }
        model.add_new_task(new_task)
        
        return {"requirement": "Adds a new task. The task is initially uncompleted when first added",
                 "result": new_task}
    else:
        return {"requirement": "Retrieves all tasks",
            "result": model.task_items}

@app.route("/tasks/completed/", methods=["GET"])
def completed():
    completed_tasks = model.search_completed_tasks()
    return {"requirement": "add a 'completed' parameter to filter by completed or uncompleted tasks",
            "result": completed_tasks}    

# 3. GET /tasks/{task_id}: Retrieves a task with a specific ID.
# 4. DELETE /tasks/{task_id}: Deletes a task with a specific ID.
# 5. PUT /tasks/{task_id}: Updates a task with a specific ID.
@app.route("/tasks/<int:task_id>", methods=["GET", "DELETE", "PUT"])
def get_task(task_id):
    task_info = model.get_task_info(task_id)
    if not task_info == None:
        if request.method == "GET":
            return {
                "requirement": "Retrieves a task with a specific ID",
                "taskId" :task_id,
                "result": task_info}  
        
        elif request.method == "DELETE":
            model.delete_task(task_id)
            return {
                    "requirement": "Deletes a task with a specific ID.",
                    "taskId" :task_id,
                    "result": "deleted"}  
        
        elif request.method == "PUT":
            update_task = {"id": task_id,
            "title": request.form['title'],
            "description": request.form['description'],
            "category": request.form['category'],
            "status": request.form['status']
            }

            model.update_task(task_id, update_task)
            return  {"requirement": "Updates a task with a specific ID.",
                     "taskId" :task_id,
                    "result": update_task}
    else:
            return {
            "taskId": task_id,
            "result": "Not found"
            } 
    
# 6. PUT /tasks/{task_id}/complete: Marks a task as completed.
@app.route("/tasks/<int:task_id>/complete", methods=["PUT"])
def set_task_completed(task_id):
    task_info = model.get_task_info(task_id)
    if task_info:
        task_to_update = task_info
        if not task_info["status"] == "completed":
            task_to_update["status"] = "completed"
            model.update_task(task_id, task_to_update)
            return  {
                "requirement": "Marks a task as completed",
                "taskId" :task_id,
                "result": f"set completed task: \n {task_info["description"]}"} 
        else:
            return {
                "requirement": "Marks a task as completed",
                "taskId" :task_id,
                "result": f"You already completed task: \n {task_info["description"]}"
                } 
    else:
        return {
            "taskId": task_id,
            "result": "Not found"
            }

# 7. GET /tasks/categories/: Retrieves all different categories.
@app.route("/tasks/categories", methods=["GET"])
def get_task_by_category():
    tasks_by_category = model.get_tasks_by_category(model.task_items)
    return {"requirement": "Retrieves all different categories.",
            "result": tasks_by_category} 

 # 8. GET /tasks/categories/{category_name}: Retrieves all tasks from a specific category.
@app.route("/tasks/categories/<string:category_name>")
def search_task_by_category(category_name): 
    task_by_category_name = model.search_tasks_by_category_name(model.task_items, category_name) 
    return {"requirement": "Retrieves all tasks from a specific category.",
            "category": category_name,
            "result": task_by_category_name} 


# #################### BACKEND : CATEGORY ##########################
# 9. GET /tasks/category/: Retrieves all categories
# 10. POST /tasks/category/: Adds a new category
@app.route("/tasks/category", methods=["POST","GET"])
def new_category():
    if request.method == "POST":
        new_category = {"id": model.get_max_id(is_task=False),
                "title": request.form['title'],
                "status": "Active"
                }
        
        model.add_new_category(new_category)
        
        return {"requirement": "Adds a new category",
                 "result": new_category}
    else:
        return {"requirement": "Retrieves all categories",
            "result": model.category_items}

# 11. GET /tasks/category/<int:category_id>: Retrieves a category with a specific ID.
# 12. DELETE /tasks/category/<int:category_id>: Deletes a category with a specific ID.
# 13. PUT /tasks/category/<int:category_id>: Updates a category with a specific ID.
@app.route("/tasks/category/<int:category_id>", methods=["GET", "PUT", "DELETE"])
def get_category(category_id):
    category_info = model.get_category_info(category_id) 
    if request.method == "GET":
        return {
            "requirement": "Retrieves a category with a specific ID",
            "categoryId" :category_id,
            "result": category_info}  
    
    elif request.method == "DELETE":
        result = ""
        if category_info:
            model.delete_category(category_id)
            result = "deleted"
        else:
            result = "not found"
            
        return {
                "requirement": "Deletes a category with a specific ID.",
                "categoryId" :category_id,
                "result": result} 
    
    elif request.method == "PUT":
        if category_info:
            status = "Active"
            if 'status' in request.form:
                status = request.form['status']

            update_category = {"id": category_id,
            "title": request.form['title'],
            "status": status
            }

            model.update_category(category_id, update_category)
            return  {"requirement": "Updates a category with a specific ID.",
                        "categoryId" :category_id,
                    "result": update_category}
        else:
            return  {"requirement": "Updates a category with a specific ID.",
                        "categoryId" :category_id,
                    "result": "not found"} 


# #################### ENDPOINT - FRONTEND ##########################
# -------- LIST ITEMS  ------------
@app.route("/", endpoint="home")
@allow_access_only_browser
def home(): 
    deleteItemForm = utility.DeleteItemForm() 
    filter_form = utility.FilterForm(request.args, meta={"csrf": False})

    categories = model.categories
    if model.get_category_name_by_id(0):
        categories = categories[1:] 

    filter_items = []

    filter_title = "-"
    filter_status = "-"
    filter_category = "-"

    category_items = model.get_categories_tuples()
    category_items.insert(0, (0, "---"))   
    filter_form.category.choices = category_items

    filter_form.status.choices.insert(0, ("-", "---"))

    filter_items = model.get_all_tasks()

    if filter_form.validate():  
        filter_title = filter_form.title.data
        filter_status = filter_form.status.data
        category_id = filter_form.category.data
   
        if filter_title.strip():
             filter_items = model.search_task_by_title(filter_items, filter_title)
        else:
            filter_title = "-"

        if not filter_status == "-":
             filter_items = model.search_task_by_status(filter_items, filter_status)
            
        
        if category_id > 0:
            filter_items = model.search_tasks_by_category_id(filter_items, category_id)
            filter_category = model.get_category_name_by_id(category_id)
 
    return render_template("home.html",
                           is_authen = get_is_auth(),
                            items=filter_items,
                            categories=categories,
                            form=filter_form,
                            filterTitle=filter_title,
                            filterStatus=filter_status,
                            filterCategory=filter_category,
                            deleteItemForm=deleteItemForm)

# -------- ITEM DETAIL  ------------
@app.route("/todo/<int:task_id>/detail", methods=["GET"] ,endpoint="detail_tasks")
@allow_access_only_browser
def item(task_id):
    task_info = {}
    deleteItemForm = utility.DeleteItemForm() 
    task_info = model.get_task_info(task_id)
    if task_info:
        return render_template("item.html", 
                                is_authen = get_is_auth(),
                                item=task_info, 
                                deleteItemForm=deleteItemForm) 
    else: 
        flash("This item does not exist.", "danger")

    return redirect(url_for("home"))

# -------- NEW ITEM  ------------
@app.route("/todo/new", methods=["GET", "POST"], endpoint="new_tasks")
@allow_access_only_browser
@requires_authentication
def new_item():
    form = utility.NewItemForm() 

    category_items = model.get_categories_tuples()
    form.category.choices = category_items
    
    # Form
    if form.validate_on_submit():
        category_name = model.get_category_name_by_id(request.form['category'])
        if category_name:
            new_task = {"id": model.get_max_id(is_task=True),
                    "title": request.form['title'],
                    "description": request.form['description'],
                    "category": category_name,
                    "status": "Pending"
                    }
            
            model.add_new_task(new_task)
            # Redirect to some page
            flash("Item {} has been successfully submitted"
                .format(request.form.get("title")), "success")
            return redirect(url_for("home")) 
        else:
            flash("Category is not matched with database", "danger")
    
    return render_template("new_item.html", is_authen = get_is_auth(), form=form)


# -------- UPDATE ITEM  ------------
@app.route("/todo/<int:task_id>/edit", methods=["GET", "POST"], endpoint="edit_tasks")
@allow_access_only_browser
@requires_authentication
def edit_item(task_id):
 
    task_info = model.get_task_info(task_id) 

    if task_info:
        form = utility.EditItemForm()
        
        if form.validate_on_submit(): 
            category_name = model.get_category_name_by_id(request.form['category'])
            update_task = {"id": task_id,
                "title": request.form['title'],
                "description": request.form['description'],
                "category": category_name,
                "status": request.form['status']
                }

            model.update_task(task_id, update_task) 

            flash("Item {} has been successfully updated".format(form.title.data), "success")
            return redirect(url_for("detail_tasks", task_id=task_id))

        form.category.choices = model.categories[1:]
        form.category.default = model.get_category_id_by_name(task_info["category"])

        form.status.default = task_info["status"]
        
        form.process()
        form.title.data       = task_info["title"]
        form.description.data = unescape(task_info["description"])
        

        return render_template("edit_item.html", 
                                is_authen = get_is_auth(),
                                item=task_info, form=form)
    else: 
        flash("This item does not exist.", "danger")

    return redirect(url_for("home")) 
        
# -------- COMPLATE TASK -------
@app.route("/todo/<int:task_id>/complate", methods=["POST"], endpoint="complete_tasks")
@allow_access_only_browser
@requires_authentication
def set_task_completed(task_id):
    task_info = model.get_task_info(task_id) 
    if task_info:
        task_to_update = task_info
        if not task_info["status"] == "Completed":
            task_to_update["status"] = "Completed"
            model.update_task(task_id, task_to_update) 
            flash(f"You have set completed to task: \n {task_info["description"]}", "success")
        else:
            task_to_update["status"] = "Completed"
            model.update_task(task_id, task_to_update) 
            flash(f"Warning: You already completed task: \n {task_info["description"]}", "danger")

    return redirect(url_for("home")) 
    
# -------- DELETE ITEM  ------------
@app.route("/todo/<int:task_id>/delete", methods=["POST"], endpoint="delete_tasks")
@requires_authentication
def delete_tasks(task_id): 
    task_info = model.get_task_info(task_id)
    if task_info:
        model.delete_task(task_id)
        flash("Item {} has been successfully deleted.".format(task_info["title"]), "success")
    else: 
        flash("This item does not exist.", "danger")

    return redirect(url_for("home")) 

# -------- ERROR HANDLER  ------------
def page_404(e):
    if is_access_from_postman():
        return "404: Page Not Found"
    else:
        return render_template("errors/404.html", is_authen = get_is_auth())

def page_405(e):
    if is_access_from_postman():
        return "405: Method Not Allowed"
    else:
        return render_template("errors/405.html", is_authen = get_is_auth())

def page_401(e):
    if is_access_from_postman():
        return "401: Unauthorized Error"
    else:
        return render_template("errors/401.html", is_authen = get_is_auth())

app.register_error_handler(404, page_404)
app.register_error_handler(405, page_405)
app.register_error_handler(401, page_401)
