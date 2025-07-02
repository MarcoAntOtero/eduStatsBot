import config
import csv
from datetime import datetime
import os
import time


keywords = [
    # Emotional strain & mental health
    "burnt out", "mental breakdown", "can't focus", "cannot focus", "overwhelmed", "lose my mind","losing my mind"
    "panic attacks", "feel like a failure", "am a failure", "cried", "losing motivation", "hate my major", "why am I even doing this?", "college has been horrible",
    "depressed", "hate myself", "stressed out", "I'm cooked", "i'm cooked", "am cooked", "need to lock in", "can't lock in", "cannot lock in",
    "overthinking", "so stressed", "disappointed in myself", "feeling overwhelmed", "withdraw", "am panicking",
    "aimlessness", "wasted all my potential", "wasted my time", "so exhausted", "feel exhausted", "am exhausted",

    # Academic struggle
    "failing classes", "barely passing", "not going to graduate", "wont graduate", "won't graduate" "killing me", "falling behind"
    "behind in school", "behind in my classes", "behind in all my classes","struggling to keep up", "my gpa is", "too many assignments",
    "dropped out", "can't pass", "retaking a class", "low grades", "how am i going to survive", "college lies", "flunking",
    "struggling with math", "hate math", "hard class", "don't understand", "screw over", "screwed over", "i'm screwed",
    "nothing is clicking", "don't get it", "difficult exam", "placed in wrong class", "disappointed in myself",
    "struggle to learn", "failed a class", "behind on all my work", "behind on my work", "behind on work",
 
    # Institutional barriers
    "no advisor helped me", "bad advising", "school won’t let me", "can’t afford",
    "debt", "financial hold",

    # Academic decisions / setbacks
    "withdrew from", "academic probation", "took a gap semester",
    "course recovery", "transfer schools", "going back to school",

    # Hopelessness
    "i feel dumb", "i'm not smart enough", "wish i could redo it", "hopeless",
    "no hope", "sm anxiety", "worrying about", "have anxiety"
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
    while True:
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

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

def main():
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
    

if __name__ == "__main__":
    main()  # Call the function to run the bot