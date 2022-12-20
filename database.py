import sqlite3

# Connect to the database
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Create the tasks table if it doesn't already exist
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS tasks (
        chat_id INTEGER,
        task TEXT,
        due_date TEXT,
        completed INTEGER
    )
    '''
)

# Create the habits table if it doesn't already exist
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS habits (
        chat_id INTEGER,
        task TEXT,
        frequency TEXT,
        completed INTEGER
    )
    '''
)

def add_task(chat_id, task, due_date=None, frequency=None):
    if frequency is None:
        # Add the task to the tasks table
        cursor.execute(
            'INSERT INTO tasks (chat_id, task, due_date, completed) VALUES (?, ?, ?, 0)',
            (chat_id, task, due_date)
        )
    else:
        # Add the task to the habits table
        cursor.execute(
            'INSERT INTO habits (chat_id, task, frequency, completed) VALUES (?, ?, ?, 0)',
            (chat_id, task, frequency)
        )
    # Commit the changes to the database
    conn.commit()

def get_tasks(chat_id):
    # Retrieve the tasks from the tasks table
    cursor.execute(
        'SELECT task, due_date FROM tasks WHERE chat_id = ?',
        (chat_id,)
    )
    tasks = cursor.fetchall()
    # Retrieve the habits from the habits table
    cursor.execute(
        'SELECT task, frequency FROM habits WHERE chat_id = ?',
        (chat_id,)
    )
    habits = cursor.fetchall()
    # Combine the tasks and habits into a single list and return it
    return tasks + habits

def delete_task(chat_id, task_id):
    # Get the list of tasks
    tasks = get_tasks(chat_id)
    # Get the task to delete
    task = tasks[task_id-1]
    # Check if the task is a task or a habit
    if len(task) == 2:
        # Delete the task from the tasks table
        cursor.execute(
            'DELETE FROM tasks WHERE chat_id = ? AND task = ?',
            (chat_id, task[0])
        )
    else:
        # Delete the habit from the habits table
        cursor.execute(
            'DELETE FROM habits WHERE chat_id = ? AND task = ?',
            (chat_id, task[0])
        )
    # Commit the changes to the database
    conn.commit()

def mark_task_complete(chat_id, task_id):
    # Get the list of tasks
    tasks = get_t
