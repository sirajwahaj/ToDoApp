from flask import Flask, request, jsonify
import json


def read_form():
    task_dic = {}
    task_dic['id'] = int(request.form['id'])
    task_dic['description'] = request.form['description']
    task_dic['category'] = request.form['category']
    task_dic['status'] = request.form.get('status', 'pending')
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
        return True


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


def delete_task(id):
    expired_task = get_record(id)
    if expired_task is None:
        return jsonify({"Error": f"Task with ID {id} not found"}), 404

    tasks = read_tasks_file()
    try:
        tasks.remove(expired_task)
        with open('tasks.json', 'w') as file:
            json.dump(tasks, file, indent=4)
            return jsonify({"Message": "Task deleted successfuly."})
    except json.JSONDecodeError:
        return jsonify({"Message": "Task has not been deleted."}), 500
    except ValueError:
        return jsonify({"Error": f"Task with ID {id} not found in the list"}), 404
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


def mark_complete(id):
    completed_task = get_record(id)
    completed_task['status'] = "completed"
    if write_tasks_to_file(completed_task):
        return jsonify({'Message': 'Task has marked completed'})


def get_categories():
    tasks = read_tasks_file()
    categoreis = set()
    for value in tasks:
        categoreis.add(value['category'])
    return list(categoreis)


def get_category1():
    tasks = read_tasks_file()
    categories = get_categories()
    task_of_categories = list()
    category_dict = dict()
    for category in categories:
        for task in tasks:
            if category == task['category']:
                task_of_categories.append({category: task})
    return task_of_categories


def get_category():
    tasks = read_tasks_file()
    categories = get_categories()
    category_dict = {category: [] for category in categories}

    for task in tasks:
        category = task['category']
        category_dict[category].append(task)

    return dict(category_dict)


def filter_by_status():
    tasks = read_tasks_file()
    category_dict = {'completed': [], 'pending': []}

    for task in tasks:
        status = task['status']
        category_dict[status].append(task)

    return dict(category_dict)


def filter_by_category(category_name):
    tasks = read_tasks_file()
    tasks_list = list()

    for task in tasks:
        if task['category'] == category_name:
            tasks_list.append(task)

    return tasks_list


def readable_dic(dictionary):
    max_key_length = max(len(str(key)) for key in dictionary.keys())

    for key, value in dictionary.items():
        padding = " " * (max_key_length - len(str(key)))
        print(f"{key}: {padding}{value} \n")
