from Google import Create_Service
from schedule import every, repeat, run_pending
import datetime
import json

CLIENT_SECRET_FILE = 'client-secret-file.json'
API_NAME = 'tasks'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/tasks']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

def get_month_day_year_time():
    """
    Function used to get the current date in month/day/year format
    @return: the current date in the format specified
    """
    current_date = datetime.date.today()
    current_date = current_date.strftime("%m/%d/%y")
    return current_date

@repeat(every().sunday.at("20:00"))
#@repeat(every(2).seconds)
def create_weekly_daily_task_list():
    """
    Weekly recurring event that constructs a new daily task list for the specified week
    """
    tasklist_info = service.tasklists().insert(
        body={'title': f'Daily Task Lists Week of {get_month_day_year_time()}'}
    ).execute()
    create_weekly_tasks(tasklist_info.get('id'))


def get_body(path_to_body: str):
    """
    Function used to access JSON file contents used in constructing tasklist and task bodies
    @param path_to_body, a path to the location of the JSON file
    @return data, the loaded JSON data
    """
    with open(path_to_body, 'r') as f:
        data = json.load(f)
    return data


def create_weekly_tasks(tasklist_id: str):
    """
    Function used for creating weekly tasks and subtasks
    @param tasklist_id, the ID for the tasklist that contains the tasks
    """
    week_data = get_body('weekly-tasks-body.json')
    day_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 
    5: 'Saturday', 6: 'Sunday'}
    day_info = None
    for num in day_dict.keys():
        day_info = service.tasks().insert(
            tasklist=tasklist_id,
            body={
                'title': day_dict.get(num),
                'notes': week_data.get('notes') if week_data.get('notes') is not None else None,
                'due': week_data.get('due') if week_data.get('due') is not None else None,
                'deleted': week_data.get('deleted') if week_data.get('deleted') is not None else None,
                'status': week_data.get('status') if week_data.get('status') is not None else None
            },
            previous = None if day_info is None else day_info.get('id')
        ).execute()
        create_daily_tasks(tasklist_id, day_info.get('id'))
    create_special_weekly_tasks(tasklist_id)


def create_special_weekly_tasks(tasklist_id: str):
    """
    Function used to create 'special weekly tasks', or long-term tasks that I want to accomplish
    throughout the week
    @param tasklist_id, the ID for the tasklist that contains the tasks"""
    special_week_data = get_body('special-weekly-tasks-body.json')
    prev_key = None
    for task in special_week_data:
        prev_key = create_task(tasklist_id, special_week_data[task], prev_key=prev_key)


def create_daily_tasks(tasklist_id: str, task_id: str):
    """Function used to create daily tasks (subtasks)
    @param tasklist_id, the ID for the tasklist that contains the tasks
    @param task_id, the ID parent task of the subtasks
    """
    day_data = get_body('daily-tasks-body.json')
    prev_key = None
    for task in day_data:
        prev_key = create_task(tasklist_id, day_data[task], task_id, prev_key)


def create_task(tasklist_id: str, task_body: dict, task_id: str=None, prev_key: str=None):
    """Function used to create tasks
    @param tasklist_id, the ID for the tasklist that contains the task
    @oaram task_body, body contents of the task
    @param task_id, ID of parent task (applicable only if subtask)
    @param prev_key, key of task which comes before current task
    @return task_info.get('id'), the ID of the generated task
    """
    task_info = service.tasks().insert(
            tasklist=tasklist_id,
            body={
                'title': task_body.get('title'),
                'notes': task_body.get('notes') if task_body.get('notes') is not None else None,
                'due': task_body.get('due') if task_body.get('due') is not None else None,
                'deleted': task_body.get('deleted') if task_body.get('deleted') is not None else None,
                'status': task_body.get('status') if task_body.get('status') is not None else None
            },
            previous = None if prev_key is None else prev_key,
            parent = None if task_id is None else task_id
    ).execute()
    return task_info.get('id')


# While loop used to run the process on a rolling basis
while True:
    run_pending()

#TODO: CREATE FUNCTIONALITY WHEREIN YOU CAN REFRESH ACCESS BEFORE IT EXPIRES





