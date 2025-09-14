import schedule
import time
import threading
import logging
from queue import Queue
import sys

# Configure logging once at startup
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

from reddit_bot.collect import continuous_collection
from reddit_bot.analyze import clean_and_analyze
from reddit_bot.create_data import create_weekly_data
from reddit_bot.create_data import create_data_alltime

# Create a queue for scheduled tasks
task_queue = Queue()

def schedule_checker():
    """Run scheduled tasks and put them in the main thread queue"""
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Start the data collection thread
    collect_thread = threading.Thread(target=continuous_collection, daemon=True)
    collect_thread.start()

    # Schedule the tasks
    schedule.every().day.at("12:00").do(lambda: task_queue.put(
        lambda: clean_and_analyze("data/reddit_data_v2.csv")
    ))
    schedule.every().sunday.at("12:01").do(lambda: task_queue.put(
        lambda: create_weekly_data(number_data_points=10)
    ))
    schedule.every().sunday.at("12:02").do(lambda: task_queue.put(
        create_data_alltime
    ))

    # Start schedule checker in background
    schedule_thread = threading.Thread(target=schedule_checker, daemon=True)
    schedule_thread.start()

    try:
        while True:
            # Check for tasks in the main thread
            try:
                task = task_queue.get_nowait()
                task()  # Execute in main thread
            except:
                pass
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down...")
        sys.exit(0)