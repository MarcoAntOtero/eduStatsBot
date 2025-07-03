import reddit_bot.config as config

def post_results():
    # Authenticate with Reddit 
    r = config.authenticateReddit()
    subreddit = r.subreddit("dataIsBeautiful")
    subreddit.submit_image(title="Key Word Frequency This Month", image_path="created_data/.png")

if __name__ == "__main__":
    post_results() 