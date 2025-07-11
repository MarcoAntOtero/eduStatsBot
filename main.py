import schedule
import time
import threading
import logging
# Configure logging once at startup
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
from reddit_bot.collect import continuous_collection
from reddit_bot.analyze import clean_and_analyze
from reddit_bot.create_data import create_data
from reddit_bot.post_results import post_results

if __name__ == "__main__":
    # Start the data collection thread
    collect_thread = threading.Thread(target=continuous_collection, daemon=False)
    collect_thread.start()

    # Schedule the tasks
    schedule.every().day.at("12:00").do(lambda:clean_and_analyze("data/reddit_data_v2.csv"))
    schedule.every().sunday.at("12:00").do(lambda: create_data(type='kw', number_data_points=10))
    schedule.every().sunday.at("12:05").do(post_results)
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logging.info("Shutting down...")
