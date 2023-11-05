from flask import Flask, request, render_template, redirect, url_for
import json
import os 

app = Flask(__name__)

db_file = "tasks.json"

# Home page 
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# Add new task
@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.form
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "description": data["description"],
        "category": data["category"],
        "status": "uncompleted"
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return redirect(url_for('home'))

# View all tasks
@app.route('/view_tasks', methods=['GET'])
def view_tasks():
    tasks = load_tasks()
    return render_template('view_tasks.html', tasks=tasks)

# Edit task
@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is not None:
        if request.method == 'POST':
            data = request.form
            task['title'] = data['title']
            task['description'] = data['description']
            task['category'] = data['category']
            save_tasks(tasks)
            return redirect(url_for('view_tasks'))
        return render_template('edit_task.html', task=task)
    return "Task not found!"

# Delete task
@app.route('/delete_task/<int:task_id>', methods=['GET'])
def delete_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is not None:
        tasks.remove(task)
        save_tasks(tasks)
    return redirect(url_for('view_tasks'))

# Edit Status
@app.route('/update_status/<int:task_id>', methods=['GET'])
def update_status(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is not None:
        task['status'] = 'completed' if task['status'] == 'uncompleted' else 'uncompleted'
        save_tasks(tasks)
    return redirect(url_for('view_tasks'))

#ID
@app.route('/view_task', methods=['GET'])
def view_task():
    task_id = request.args.get('task_id')
    if task_id:
        task = get_task_by_id(int(task_id))
        if task:
            return render_template('view_task.html', task=task)
        else:
            return "Task not found!"
    return render_template('view_task.html')

def get_task_by_id(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None

# JSON file
def load_tasks():
    try:
        if os.path.exists(db_file):
            with open(db_file, "r", encoding="utf-8") as file:
                tasks = json.load(file)
        else:
            tasks = []
        return tasks
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        return []

def save_tasks(tasks):
    try:
        with open(db_file, 'w') as f:
            json.dump(tasks, f, indent=2)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)