import logging
import time
from telegram import Bot
from telegram.error import TelegramError
from database import get_tasks, mark_task_incomplete

logger = logging.getLogger(__name__)

def daily_summary(context):
    # Get the list of tasks
    tasks = get_tasks(context.job.context)
    # Count the number of tasks and habits
    num_tasks = len([task for task in tasks if len(task) == 2])
    num_habits = len(tasks) - num_tasks
    # Build the message
    message = f'Here is your daily summary:\n\n'
    message += f'Tasks: {num_tasks}\n'
    message += f'Habits: {num_habits}\n\n'
    message += 'Tasks:\n'
    for task in tasks:
        if len(task) == 2:
            message += f'- {task[0]}\n'
    message += '\nHabits:\n'
    for task in tasks:
        if len(task) == 3:
            message += f'- {task[0]}\n'
    # Send the message to the user
    try:
        context.bot.send_message(context.job.context, message)
    except TelegramError as e:
        logger.warning(f'Could not send daily summary: {e}')
    # Mark all habits as incomplete
    for task in tasks:
        if len(task) == 3:
            mark_task_incomplete(context.job.context, task[0])

def weekly_summary(context):
    # Get the list of tasks
    tasks = get_tasks(context.job.context)
    # Count the number of completed tasks and habits
    num_completed_tasks = len([task for task in tasks if len(task) == 2 and task[1] == 1])
    num_completed_habits = len([task for task in tasks if len(task) == 3 and task[2] == 1])
    # Build the message
    message = f'Here is your weekly summary:\n\n'
    message += f'Tasks completed: {num_completed_tasks}\n'
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
