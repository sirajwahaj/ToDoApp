import json
import config

# #################### MODEL : FILE MANAGER ##########################
task_filename = "task.json"
task_items = []

category_filename = "category.json"
category_items = []

# tuples for front end
categories = []

def load_db(filename):
    json_dict = {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
                try:
                    json_dict = json.load(file)
                except json.JSONDecodeError as e:
                    print(f"Wrong JSON format: {e}")
                except ValueError:
                    print("File is not json format")
    except FileNotFoundError:
        f = open(filename, "w", encoding="utf-8")
        f.writelines("[]")  

    return json_dict

def save_db(is_task):
    if is_task:
        with open(task_filename, 'w') as f:
            return json.dump(task_items, f, indent=4)
    else:
        with open(category_filename, 'w') as f:
            return json.dump(category_items, f, indent=4)


def get_max_id(is_task):
    items = []
    if is_task:
        items = load_db(task_filename)
    else:
        items = load_db(category_filename)

    # Both Task and categegory has id as the key
    if not items: 
        return 1
    else: 
        # Find the maximum ID in the list
        max_id = max(task["id"] for task in items)
        # Calculate the next ID
        return max_id + 1    

            
# #################### MODEL : TASK ##########################
def get_all_tasks():
    return task_items

def add_new_task(new_task): 
    task_items.append(new_task)
    save_db(is_task=True)
    
def get_task_info(task_id):
    for task in task_items:
        if task["id"] == int(task_id):
            return task  # Return the task if the ID matches
    
    return None  

def delete_task(task_id):
    for index, task in enumerate(task_items):
        if task["id"] == task_id:
            del task_items[index]
            save_db(is_task=True)
            break
    
def update_task(task_id, update_task):
    for index, task in enumerate(task_items):
        if task["id"] == task_id:
            task_items[index] = update_task
            save_db(is_task=True)
            break


# #################### MODEL : CATEGORY ##########################
def get_categories(): 
    return categories

def get_categories_tuples():
    return [(item['id'], item['title']) for item in category_items]

def get_category_info(category_id):
    return next((category for category in category_items if category["id"] == category_id), None)
    # for category in category_items:
    #     if category["id"] == category_id:
    #         return category  # Return the category if the ID matches
    # return None

def add_new_category(new_category): 
    category_items.append(new_category)
    save_db(is_task=False) 

def delete_category(category_id):
    for index, category in enumerate(category_items):
        if category["id"] == category_id:
            del category_items[index]
            save_db(is_task=False)
            break
    
def update_category(category_id, update_category):
    for index, category in enumerate(category_items):
        if category["id"] == int(category_id):
            category_items[index] = update_category
            save_db(is_task=False)
            break

# #################### MODEL : QUERY FOR FRONTEND/BACKEND ##########################
def get_category_name_by_id(category_id):
    # Iterate through the list of tuples
    return next((item[1] for item in categories if item[0] == int(category_id)), None)
    # for item in categories:
    #     if item[0] == int(category_id):
    #         return item[1]
    # return None
 
def get_category_id_by_name(category_name): 
    # Iterate through the list of tuples
    return next((item[0] for item in categories if item[1] == category_name), None)
    # for item in categories:
    #     if item[1] == category_name:
    #         return item[0]
    # return None

# get parameter task_items because user might submmit fillter
def get_tasks_by_category(task_items):
    tasks_by_category = {}

    # Group tasks by category
    for task in task_items:
        category = task["category"]
        if category not in tasks_by_category:
            tasks_by_category[category] = []
         
        tasks_by_category[category].append(task)
 
    return tasks_by_category

def search_tasks_by_category_id(task_items, category_id):
    category_name = get_category_name_by_id(category_id)
    return [task for task in task_items if category_name.lower() in task["category"].lower()]
    
    # matching_tasks = []
    # for task in task_items:
    #     if category_name.lower() in task["category"].lower():
    #         matching_tasks.append(task)
    # return matching_tasks

def search_tasks_by_category_name(task_items, category_name):
    return [task for task in task_items if category_name.lower() in task["category"].lower()]
    

def search_completed_tasks():
    status = "completed"
    return [task for task in task_items if status in task["status"].lower()]
    # matching_tasks = []
    # for task in task_items:
    #     if "completed" in task["status"].lower():
    #         matching_tasks.append(task)
    # return matching_tasks

def search_task_by_title(task_items, search_text):
    # Create a list to store matching items
    return [task for task in task_items if search_text in task["title"]]
    # matching_tasks = []
    # for task in task_items:
    #     if search_text in task["title"]:
    #         matching_tasks.append(task)
    # return matching_tasks

def search_task_by_status(task_items, status):
    # Create a list to store matching items
    return [task for task in task_items if status in task["status"]]
    # matching_tasks = []
    # for task in task_items:
    #     if status in task["status"]:
    #         matching_tasks.append(task)
    # return matching_tasks


# #################### MODEL : FETCH DATA ##########################
task_items = load_db(task_filename)
category_items = load_db(category_filename)
categories = get_categories_tuples()