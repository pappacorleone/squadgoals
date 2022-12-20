import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from database import add_task, get_tasks, delete_task, mark_task_complete, mark_task_incomplete

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)



# Define the states
class State:
    ADD_TASK = 1
    DELETE_TASK = 2
    MARK_TASK_COMPLETE = 3
    MARK_TASK_INCOMPLETE = 4

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
                reply_keyboard,
                one_time_keyboard=True,
                selective=True,
            )
        )
        # Store the state in the dictionary
        states[update.message.chat_id] = State.DELETE_TASK
    elif command == '/done':
    # Get the list of tasks
    tasks = get_tasks(update.message.chat_id)
    # Display the tasks as a list of options
    options = '\n'.join(f'{i+1}. {task[0]}' for i, task in enumerate(tasks))
    message = 'Please select a task to mark as complete:\n' + options
    # Send the message as a reply keyboard
    reply_keyboard = [[str(i+1)] for i in range(len(tasks))]
    update.message.reply_text(
        message,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            selective=True,
        )
    )
    # Store the state in the dictionary
    states[update.message.chat_id] = State.MARK_TASK_COMPLETE
    elif command == '/undone':
    # Get the list of tasks
    tasks = get_tasks(update.message.chat_id)
    # Display the tasks as a list of options
    options = '\n'.join(f'{i+1}. {task[0]}' for i, task in enumerate(tasks))
    message = 'Please select a task to mark as incomplete:\n' + options
    # Send the message as a reply keyboard
    reply_keyboard = [[str(i+1)] for i in range(len(tasks))]
    update.message.reply_text(
        message,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            selective=True,
        )
    )
    # Store the state in the dictionary
    states[update.message.chat_id] = State.MARK_TASK_INCOMPLETE


def handle_response(update, context):
    # Get the state from the dictionary
    state = states.get(update.message.chat_id)
    if state == State.DELETE_TASK:
        # Get the index of the task to delete
        try:
            index = int(update.message.text) - 1
            # Delete the task
            delete_task(update.message.chat_id, index)
            update.message.reply_text('Task deleted!')
        except ValueError:
            update.message.reply_text('Invalid option. Please try again.')
        except IndexError:
            update.message.reply_text('Task not found. Please try again.')
        # Remove the state from the dictionary
        states.pop(update.message.chat_id, None)
    elif state == State.MARK_TASK_COMPLETE:
        # Get the index of the task to mark as complete
        try:
            index = int(update.message.text) - 1
            # Mark the task as complete
            mark_task_complete(update.message.chat_id, index)
            update.message.reply_text('Task marked as complete!')
        except ValueError:
            update.message.reply_text('Invalid option. Please try again.')
        except IndexError:
            update.message.reply_text('Task not found. Please try again.')
        # Remove the state from the dictionary
        states.pop(update.message.chat_id, None)

def main():
# Create the Updater and pass it the bot's token
updater = Updater(5879721167:AAEl1EzoHTbLNJOHKeYJt_KlxzgBAsyaozU, use_context=True)

# Add the start command handler
dp.add_handler(CommandHandler('start', start))

# Add the command handler for the /menu command
dp.add_handler(CommandHandler('menu', handle_command))

# Add the command handler for the /add command
dp.add_handler(CommandHandler('add', handle_command))

# Add the command handler for the /delete command
dp.add_handler(CommandHandler('delete', handle_command))

# Add the command handler for the /list command
dp.add_handler(CommandHandler('list', handle_command))

# Add the command handler for the /done command
dp.add_handler(CommandHandler('done', handle_command))

# Add the command handler for the /undone command
dp.add_handler(CommandHandler('undone', handle_command))

# Add the message handler for handling responses
dp.add_handler(MessageHandler(Filters.text, handle_response))

# Start the bot
updater.start_polling()

# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT
updater.idle()
