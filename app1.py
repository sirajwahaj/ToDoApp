from flask import Flask, jsonify, request, redirect, render_template, url_for
import json
import model

app = Flask(__name__)


# GET /tasks Hämtar alla tasks. För VG: lägg till en parameter completed som kan filtrera på färdiga eller ofärdiga tasks.
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


# @app.route('/tasks')
# def tasks():
#     return jsonify(task1 = "tasks" )


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


""" 
@app.route('/tasks/id')
def update_task():
    id = int(request.args.get('task_id'))
    # description = request.args.get('desc')
    # category = request.args.get('category')
    # status = request.args.get('status')

    return redirect('/',)
@app.route('/tasks/<task_id>')
def update_taskid(task_id):
    return task_id """

# PUT /tasks/{task_id}/complete Markerar en task som färdig.

# GET /tasks/categories/ Hämtar alla olika kategorier.

# GET /tasks/categories/{category_name} Hämtar alla tasks från en specifik kategori.

if __name__ == '__main__':
    app.run(debug=True)
