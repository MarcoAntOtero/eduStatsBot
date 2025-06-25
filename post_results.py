import config
import pandas as pd

r = config.authenticateReddit()

df = pd.read_csv("data/reddit_data_v2.csv")
subredditName = "dataIsBeautiful"

title = ""
caption = ""
image_post = r.subreddit(subredditName).submit(title, image_path="plot.png")
print(f"Image post created: {image_post.title} - {image_post.url}")
