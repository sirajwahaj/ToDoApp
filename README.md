# To-do App
Your task is to create a "To-do App" using Python and Flask.

This project is a part of the basic Python course. It's good example for Create, Read, Update, and Delete (CRUD) for beginer Python developers.   



## Backend
You are to create an API in Flask that reads data from the file `tasks.json` and modifies it with certain requests with now html you will run on PostMan.

    How to Config: 
        FLASK_APP=app_backend.py
        FLASK_ENV=development
        FLASK_DEBUG=1
    Run in terminal : 
        flask run

### Endpoints

- `GET /tasks` Retrieves all tasks. For a higher grade (VG), add a parameter `completed` that can filter completed or uncompleted tasks.

- `POST /tasks` Adds a new task. The task is initially uncompleted when first added.

- `GET /tasks/{task_id}` Retrieves a task with a specific ID.

- `DELETE /tasks/{task_id}` Deletes a task with a specific ID.

- `PUT /tasks/{task_id}` Updates a task with a specific ID.

- `PUT /tasks/{task_id}/complete` Marks a task as completed.

- `GET /tasks/categories/` Retrieves all different categories.

- `GET /tasks/categories/{category_name}` Retrieves all tasks from a specific category.

## Frontend
You should create a frontend using a Flask template. From this frontend, users should be able to view all tasks. For a higher grade (VG), there should also be a form where users can add a new task. The frontend is preferably placed in the root ("/") and you can only run on Browser.

    How to Config: 
        FLASK_APP=app.py
        FLASK_ENV=development
        FLASK_DEBUG=1
    Run in terminal : 
        flask run

## Grading Criteria

### For a passing grade (Godkänt)
- The frontend displays all tasks.
- All endpoints are implemented.

### For a higher grade (VG)
- All implemented endpoints provide user-friendly responses if incorrect information is provided to them. For instance, if you use `POST /tasks` and send a task in the wrong format, you should receive an error message with helpful text. A task in an incorrect format should not be added.
- All endpoints have relevant unit tests.
- The testing does not modify the `tasks.json` file.
- `DELETE /tasks/{task_id}` requires authorization, possibly using a token, for example, flask-jwt-extended.
- Users can add a new task via the frontend.
