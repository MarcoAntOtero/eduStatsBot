import reddit_bot.config as config
import os
from datetime import date
import logging

def post_results():
    # Authenticate with Reddit 
    r = config.authenticateReddit()

    image_path = f"created_data/{date.today()}_kw.png"
    # Check if the image file exists
    if not os.path.exists(image_path):
        logging.error(f"Image file {image_path} does not exist. Please create the image first.")
        return
    subreddit = r.subreddit("dataIsBeautiful")
    subreddit.submit_image(title="Key Word Frequency This Month", image_path=image_path, selftext="This is a visualization of the most frequently used keywords in the subreddits I monitor. The data is collected and analyzed automatically by my Reddit bot. If you want to see more visualizations like this, please upvote and comment!")

if __name__ == "__main__":
    post_results() 