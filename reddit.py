import config
import csv
from datetime import datetime
import os
import time


# This script collects data from Reddit using PRAW (Python Reddit API Wrapper) and saves it to a CSV file.
#keywords = ["failing", "drop out", "no internet", "burned out", "behind in school", "can't focus", "cannot focus", "overwhelmed", "no laptop",
#            "struggling","difficult", "hard to learn", "can't keep up", "not enough","fail", "support", "resources",
#            "assistance", "guidance", "tutoring" , "not passing", "can't"]
#subreddits = ["GenZ","college","highschool"]


keywords = [
    # Emotional strain & mental health
    "burnt out", "mental breakdown", "can't focus", "cannot focus", "overwhelmed",
    "panic attacks", "i feel like a failure", "cried", "losing motivation",
    "depressed", "i hate myself", "stressed out", "I'm cooked", "i'm cooked", "need to lock in", "can't lock in", "cannot lock in"

    # Academic struggle
    "failing classes", "barely passing", "not going to graduate",
    "behind in school", "struggling to keep up", "my gpa is",
    "dropped out", "can't pass", "retaking a class", "low grades",
    "struggling with math", "hate math", "hard class", "don't understand",
    "nothing is clicking", "don't get it", "difficult exam", "placed in wrong class",

    # Institutional barriers
    "no advisor helped me", "bad advising", "school won’t let me", "can’t afford",
    "debt", "$1000 for a class", "financial hold",

    # Academic decisions / setbacks
    "withdrew from class", "academic probation", "took a gap semester",
    "course recovery", "transfer schools", "going back to school",
    "community college",

    # Hopelessness
    "i feel dumb", "i'm not smart enough", "wish i could redo it",
    "no hope", "what should i do"
]


subreddits = ["GenZ","college","highschool","Adulting","CollegeRant","ApplyingToCollege"]


def collect_data_subreddit(keywords,reddit):
    # Create a list to store posts that match the keywords
    for subreddit in subreddits:

        print(f"Collecting data from subreddit: {subreddit}")

        # Iterate through the new submissions in the subreddit
        # Limit to the most recent 100 submissions

        for submission in reddit.subreddit(subreddit).new(limit=100):

            text = (submission.title + " " + (submission.selftext or "")).lower()

            if any(keyword.lower() in text for keyword in keywords):
                # If any keyword is found in the title or selftext, add the submission to the data list
                # yield do not return, it will yield the data to the caller
                #appended in run_bot function
                yield{
                    "title": submission.title,
                    "selftext": submission.selftext,
                    "url": submission.url,
                    "created_utc": datetime.utcfromtimestamp(submission.created_utc),
                    "subreddit": subreddit,
                    "author": str(submission.author),
                }

def save_data_to_csv(data, filename):
    # Save the collected data to a CSV file.
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename,mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ["title", "selftext", "url", "created_utc", "subreddit", "author"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader() # writes header inside data file
        for row in data:
            writer.writerow(row)

def continuous_collection(filename):
    # Continuously collect data from Reddit.
    r = config.authenticateReddit()
    target_subreddits = "+".join(subreddits)
    count = 0
    while count < 5:
        print("Collecting data...")
        try:
            for submission in r.subreddit(target_subreddits).stream_submissions(skip_existing=True):
                # Check if the submission is new and matches the keywords
                if submission is None or submission.author is None:
                    continue
                    
                text = (submission.title + " " + (submission.selftext or "")).lower()

                if any(keyword.lower() in text for keyword in keywords):

                    #collect data from post
                    new_row = {"title": submission.title,
                            "selftext": submission.selftext,
                            "url": f"https://reddit.com/{submission.permalink}",
                            "created_utc": datetime.utcfromtimestamp(submission.created_utc),
                            "subreddit": submission.subreddit.display_name,
                            "author": str(submission.author)
                            }
                    # If any keyword is found in the title or selftext, add the submission to the data list
                    # yield do not return, it will yield the data to the caller
                    #appended in run_bot function
                    already_exists = os.path.isfile(filename)
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(filename,mode='a', newline='', encoding='utf-8') as f:
                        fieldnames = ["title", "selftext", "url", "created_utc", "subreddit", "author"]
                        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
                        if not already_exists:
                            writer.writer()
                        writer.writerow(new_row)

                    print(f"Matched: {submission.title[:60]}")
                    count = count + 1
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

def run_bot():
    # Run the bot to post data to Reddit.
    print("Bot is running...")
    r = config.authenticateReddit()

    # Load the data
    valid_posts = []
    for i in collect_data_subreddit(keywords,r):
        # Append the data to the valid_posts list
        valid_posts.append(i)

    if not valid_posts:
        print("No valid posts found.")
        return
    else:
        print(f"Found {len(valid_posts)} valid posts.")
        # Save the data to a CSV file
        save_data_to_csv(valid_posts,"data/reddit_data_v2.csv")
    

run_bot()  # Call the function to run the bot








'''
# Load the data
df = pd.read_csv("data/cleaned2.csv")
df = df[["state", "percent_children_without_internet_access"]]
df = df.sort_values(by="percent_children_without_internet_access", ascending=False)


# Get the top 5 states with the highest percent of children without internet access
top5 = df.head(5)
worst_state = top5.iloc[0]
title = "[OC] Top 5 U.S. States with the Highest Percent of Children Without Internet Access (NCES 2021)"
caption = (
    "**Data source:** U.S. Department of Commerce, Census Bureau, 2021 ACS PUMS (cleaned via NCES tables)**\n"
    "**Tools used:** Python, pandas, matplotlib**\n"
    "*Quote from:* Laura Bestler, *Is there a Correlation between the Digital Divide and College Access?*\n\n"
    f"**Worst states for children's internet access**\n"
    f"In **{worst_state['state']}**, **{worst_state['percent_children_without_internet_access']:.1f}%** "
    "of children do not have internet access at home.\n"
    "Quote: 'Several studies show that youth with digital access at both home and school perform better academically than those with access only at school.'"
)

# Create a post with an image in the dataisbeautiful subreddit
subreddit = reddit.subreddit("dataisbeautiful")

image_post = subreddit.submit_image(title, image_path="plot.png")
image_post.reply(caption)

print(f"Image post created: {image_post.title} - {image_post.url}")

subreddit = reddit.subreddit("test")

title = "Test Post"
body = "This is a test post created by the EduStatsBot."
post = subreddit.submit(title, selftext=body)

print(f"Post created: {post.title} - {post.url}")


# Create the plot
plt.figure(figsize=(8, 4))
plt.barh(top5["state"], top5["percent_children_without_internet_access"], color='skyblue')
plt.xlabel("percent_children_without_internet_access")
plt.title("Top 5 States with Highest Percent of Children without Internet Access")
plt.tight_layout()
plt.gca().invert_yaxis()
plt.savefig("plot.png", dpi=300)


df = df[["State", "Percent Households with internet access"]]
df = df.rename(columns={
    "State": "state",
    "Number of children ages 3 to 18 living in households(in thousands),": "number_of_children_ages_3_to_18",
    "Percentage of children with any type of computer or smartphone,": "percent_children_with_computer_or_smartphone",
    "Percentage distribution of children with internet access": "percent_children_with_internet_access",
    "Percentage distribution of children with no internet access": "percent_children_without_internet_access",
})
df.to_csv("data/cleaned2.csv", index=False)
})'''
