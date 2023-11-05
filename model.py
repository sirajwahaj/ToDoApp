from flask import Flask, request, jsonify
import json


def read_form():
    task_dic = {}
    task_dic['id'] = int(request.form['id'])
    task_dic['description'] = request.form['description']
    task_dic['category'] = request.form['category']
    task_dic['status'] = request.form['status']
    return task_dic


def read_tasks_file():
    try:
        with open('tasks.json', 'r') as file:
            file_content = json.load(file)
            return list(file_content)
    except json.JSONDecodeError:
        return []


def write_tasks_to_file(dic):
    data = read_tasks_file()
    old_record = get_record(dic.get('id'))
    if old_record:
        data.remove(old_record)
    data.append(dic)
    with open('tasks.json', 'w') as file:
        json.dump(data, file, indent=4)


def get_record(id):
    data = read_tasks_file()
    for record in data:
        if record.get('id') == id:
            return record
    return None


def update_task(id):
    updated_record = read_form()
    orig_record = get_record(id)
    if orig_record:
        orig_record.update(updated_record)
        write_tasks_to_file(orig_record)
        return jsonify({"Message": "Task updated successfully"})
    else:
        return jsonify({"Error": "Task not found"}), 404
