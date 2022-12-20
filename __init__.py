import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from database import add_task, get_tasks, delete_task, mark_task_complete, mark_task_incomplete

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# Define the states
class State:
    DELETE_TASK = 1

# Define the dictionary to store the states
states = {}

def start(update, context):
    update.message.reply_text('Welcome to the Task Manager chatbot! Use /menu to see the available commands.')

def handle_command(update):
    # Split the command into the command and arguments
    command, *args = update.message.text.split()
    # Check the command and call the appropriate function
    if command == '/menu':
        message = 'Welcome to the Task Manager chatbot!\n\n'
        message += 'Here are the available commands:\n'
        message += '/add <task> [due date] - Add a new task\n'
        message += '/delete - Delete a task\n'
        message += '/list - List all tasks\n'
        message += '/done - Mark a task as complete\n'
        message += '/undone - Mark a task as incomplete\n'
        update.message.reply_text(message)
    elif command == '/add':
        # Check if the frequency argument was provided
        if 'daily' in args:
            frequency = 'daily'
            # Remove the frequency argument from the list of arguments
            args.remove('daily')
        elif 'weekly' in args:
            frequency = 'weekly'
            # Remove the frequency argument from the list of arguments
            args.remove('weekly')
        else:
            frequency = None
        task = ' '.join(args)
        add_task(update.message.chat_id, task, frequency=frequency)
        update.message.reply_text('Task added!')
    elif command == '/delete':
        # Get the list of tasks
        tasks = get_tasks(update.message.chat_id)
        # Display the tasks as a list of options
        options = '\n'.join(f'{i+1}. {task[0]}' for i, task in enumerate(tasks))
        message = 'Please select a task to delete:\n' + options
        # Send the message as a reply keyboard
        reply_keyboard = [[str(i+1)] for i in range(len(tasks))]
        update.message.reply_text(
            message,
            reply_markup=ReplyKeyboardMarkup(
