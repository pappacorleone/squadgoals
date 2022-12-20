import logging
import time
from telegram import Bot, ChatAction, ParseMode, InputMediaPhoto
from telegram.error import TelegramError
from database import get_tasks, mark_task_incomplete
from dependencies import create_daily_summary_image, create_weekly_summary_image

logger = logging.getLogger(__name__)

def send_typing_action(func):
    """Sends typing action while processing func command."""
    def command_func(*args, **kwargs):
        bot, update = args
        bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(bot, update, **kwargs)
    return command_func

@send_typing_action
def daily_summary(bot, update):
    # Get the list of tasks
    tasks = get_tasks(update.message.chat_id)
    # Count the number of tasks and habits
    num_tasks = len([task for task in tasks if len(task) == 2])
    num_habits = len(tasks) - num_tasks
    # Build the message
    message = f"Here is your daily summary:\n\n"
    message += f"Tasks: {num_tasks}\n"
    message += f"Habits: {num_habits}\n\n"
    message += "Tasks:\n"
    for task in tasks:
        if len(task) == 2:
            message += f"- {task[0]}\n"
    message += "\nHabits:\n"
    for task in tasks:
        if len(task) == 3:
            message += f"- {task[0]}\n"
    # Send the message and image to the user
    try:
        # Send the message
        bot.send_message(update.message.chat_id, message, parse_mode=ParseMode.MARKDOWN)

        # Create the daily summary image
        create_daily_summary_image(tasks)

        # Send the image
        with open('daily_summary.jpg', 'rb') as image:
            bot.send_photo(update.message.chat_id, image)
    except TelegramError as e:
        logger.warning(f'Could not send daily summary: {e}')

    # Mark all habits as incomplete
    for task in tasks:
        if len(task) == 3:
            mark_task_incomplete(update.message.chat_id, task[0])

@send_typing_action
def weekly_summary(bot, update):
    # Get the list of tasks
    tasks = get_tasks(update.message.chat_id)
    # Count the number of completed tasks and habits
    num_completed_tasks = len([task for task in tasks if len(task) == 2 and task[1] == 1])
    num_completed_habits = len([task for task in tasks if len(task) == 3 and task[2] == 1])
    # Build the message
    message = f"Here is your weekly summary:\n\n"
    message += f"Tasks completed: {num_completed_tasks}\n"
    message += f'Habits completed: {num_completed_habits}\n\n'
    message += 'Tasks:\n'
    for task in tasks:
        if len(task) == 2 and task[1] == 1:
            message += f'- {task[0]}\n'
    message += '\nHabits:\n'
    for task in tasks:
        if len(task) == 3 and task[2] == 1:
            message += f'- {task[0]}\n'
    # Send the message to the user
    try:
        context.bot.send_message(context.job.context, message)
    except TelegramError as e:
        logger.warning(f'Could not send weekly summary: {e}')

def start_scheduler(updater):
    # Schedule the daily summary job
    # The job will be run every day at midnight
