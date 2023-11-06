from flask import Flask, jsonify, request, redirect, render_template, url_for
import json
import model

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


# GET /tasks Hämtar alla tasks. För VG: lägg till en parameter completed som kan filtrera på färdiga eller ofärdiga tasks.
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    all_tasks = model.filter_by_status()
    return jsonify(all_tasks)


# POST /tasks Lägger till en ny task. Tasken är ofärdig när den först läggs till.
@app.route('/tasks', methods=['POST'])
def task():
    task_dic = model.read_form()
    model.write_tasks_to_file(task_dic)
    return redirect(url_for('home'))


# DELETE /tasks/{task_id} Tar bort en task med ett specifikt id.
# PUT /tasks/{task_id} Uppdaterar en task med ett specifikt id.
# GET /tasks/{task_id} Hämtar en task med ett specifikt id.
@app.route('/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
def get_record(task_id):
    if request.method == 'GET':
        return model.get_record(task_id)
    elif request.method == 'PUT':
        return model.update_task(task_id)
        # model.get_record(task_id)
    elif request.method == 'DELETE':
        return model.delete_task(task_id)


# PUT /tasks/{task_id}/complete Markerar en task som färdig.
@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def mark_complete(task_id):
    return model.mark_complete(task_id)


# GET /tasks/categories/ Hämtar alla olika kategorier.
@app.route('/tasks/categories', methods=['GET'])
def get_categories():
    return model.get_categories()


# GET /tasks/categories/{category_name} Hämtar alla tasks från en specifik kategori.
@app.route('/tasks/categories/<category_name>', methods=['GET'])
def filter_by_category(category_name):
    return model.filter_by_category(category_name)


@app.route('/tasks/by/categories', methods=['GET'])
def get_category():
    category = model.get_category()
    return jsonify(category)


if __name__ == '__main__':
    app.run(debug=True)
