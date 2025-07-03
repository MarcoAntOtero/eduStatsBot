import schedule
import time
from reddit_bot.collect import collect_data
from reddit_bot.analyze import clean_and_analyze
from reddit_bot.create_data import create_data
from reddit_bot.post_results import post_results

schedule.every(30).minutes.do(collect_data())
schedule.every().day.at("12:00").do(clean_and_analyze())
schedule.every().sunday.at("12:00").do(create_data())
#schedule.every().sunday.at("12:05").do(post_results())

while True:
    schedule.run_pending()
    time.sleep(1)
