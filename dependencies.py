import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

def create_daily_summary_image(tasks):
    # Count the number of completed and incomplete tasks
    completed = [task for task in tasks if task[1] == 'complete']
    incomplete = [task for task in tasks if task[1] != 'complete']
    completed_count = len(completed)
    incomplete_count = len(incomplete)
    # Create the bar chart
    labels = ['Completed', 'Incomplete']
    values = [completed_count, incomplete_count]
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['#00FF00', '#FF0000'])
    plt.title('Daily Summary')
    plt.xlabel('Task Status')
    plt.ylabel('Number of Tasks')
    # Save the chart to a JPEG file
    plt.savefig('daily_summary.jpg', format='jpeg')
    # Create the text summary
    lines = []
    if completed_count == 0:
        lines.append('No tasks completed today :( Keep up the hard work!')
    elif completed_count == 1:
        lines.append('One task completed today! Great job!')
    else:
        lines.append(f'{completed_count} tasks completed today! You rock!')
    if incomplete_count > 0:
        lines.append(f'{incomplete_count} tasks left for tomorrow. Let\'s get to work!')
    # Create an image and draw the text on it
    image = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('arial.ttf', 24)
    y = 0
    for line in lines:
        draw.text((0, y), line, font=font, fill=(0, 0, 0))
        y += 30
    # Save the image to a JPEG file
    image.save('text_summary.jpg', 'jpeg')
    # Combine the bar chart and text summary into a single image
    chart = Image.open('daily_summary.jpg')
    text = Image.open('text_summary.jpg')
    image = Image.new('RGB', (600, 400), color='white')
    image.paste(chart, (0, 0))
    image.paste(text, (0, 200))
    image.save('daily_summary.jpg', 'jpeg')
                       
    def create_weekly_summary_image(tasks):
    # Group tasks by day
    tasks_by_day = {}
    for task in tasks:
        if task[2] not in tasks_by_day:
            tasks_by_day[task[2]] = []
        tasks_by_day[task[2]].append(task)
    # Count the number of completed and incomplete tasks for each day
    completed_by_day = {}
    incomplete_by_day = {}
    for day, day_tasks in tasks_by_day.items():
        completed = [task for task in day_tasks if task[1] == 'complete']
        incomplete = [task for task in day_tasks if task[1] != 'complete']
        completed_by_day[day] = len(completed)
        incomplete_by_day[day] = len(incomplete)
    # Create the bar chart
    labels = list(completed_by_day.keys())
    completed_values = list(completed_by_day.values())
    incomplete_values = list(incomplete_by_day.values())
    fig, ax = plt.subplots()
    ax.bar(labels, completed_values, color='#00FF00', label='Completed')
    ax.bar(labels, incomplete_values, bottom=completed_values, color='#FF0000', label='Incomplete')
    plt.title('Weekly Summary')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Tasks')
    plt.legend()
    # Save the chart to a JPEG file
    plt.savefig('weekly_summary.jpg', format='jpeg')
    # Create the text summary
    total_completed = sum(completed_values)
    total_incomplete = sum(incomplete_values)
    lines = []
    if total_completed == 0:
        lines.append('No tasks completed this week :( Keep up the hard work!')
    elif total_completed == 1:
        lines.append('One task completed this week! Great job!')
    else:
        lines.append(f'{total_completed} tasks completed this week! You rock!')
    if total_incomplete > 0:
        lines.append(f'{total_incomplete} tasks left for next week. Let\'s get to work!')
    
    # Create an image and draw the text on it
    image = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('arial.ttf', 24)
    y = 0
    for line in lines:
        draw.text((0, y), line, font=font, fill=(0, 0, 0))
        y += 30
    # Save the image to a JPEG file
    image.save('text_summary.jpg', 'jpeg')
    # Combine the bar chart and text summary into a single image
    chart = Image.open('weekly_summary.jpg')
    text = Image.open('text_summary.jpg')
    image = Image.new('RGB', (600, 400), color='white')
    image.paste(chart, (0, 0))
    image.paste(text, (0, 200))
    image.save('weekly_summary.jpg', 'jpeg')
