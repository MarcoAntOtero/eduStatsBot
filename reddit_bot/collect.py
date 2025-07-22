import logging
from reddit_bot.config import authenticateReddit
import csv
import json 
import time
from datetime import datetime, timezone, timedelta
from reddit_bot.lock import file_lock  # Import the file lock for thread-safe file operations

subreddits = ["GenZ","college","highschool","Adulting","CollegeRant","ApplyingToCollege"]

def load_keywords():
    # Load keywords from a JSON file or define them directly in the code.
    try:
        with open("data/keywords.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("Keywords file not found. Using default keywords.")
        # If the file is not found, use the default keywords defined below.
        return ("burnt out", "mental breakdown", "can't focus", "cannot focus", "overwhelmed", "lose my mind")
def load_seen_ids():
    # Load seen IDs from a JSON file or define them directly in the code.
    try:
        with open("data/seen_ids.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return dict()  # Return an empty dictionary if the file does not exist
    
def add_seen_ids(post):
    try:
        with file_lock:  # Ensure thread-safe file access
            with open("data/seen_ids.json", "w") as f:
                json.dump(post, f, indent=4)
    except FileNotFoundError:
        logging.error("Seen IDs file not found.")


def collect_data():
    r = authenticateReddit()
    keywords = load_keywords()
    seen_ids = load_seen_ids()  # Load seen IDs to avoid duplicates
    # Create a list to store posts that match the keywords
    for subreddit in subreddits:

        logging.info(f"Collecting data from subreddit: {subreddit}")

        # Iterate through the new submissions in the subreddit
        # Limit to the most recent 100 submissions

        for post in r.subreddit(subreddit).new(limit=100):

            if post.id in seen_ids:
                # If the post ID is already seen, skip it
                continue
            combined_text = (post.title + " " + (post.selftext or "")).lower()

            if any(keyword.lower() in combined_text for keyword in keywords):
                # If any keyword is found in the title or selftext, add the submission to the data list
                save_post_to_csv(post) # add to csv
                seen_ids[post.id] = post.created_utc  # Add the post ID to the seen IDs set
    add_seen_ids(seen_ids)  # Save the updated seen IDs to the file

def continuous_collection():
    # Continuously collect data from Reddit.
    r = authenticateReddit()
    keywords = load_keywords()
    seen_ids = load_seen_ids()  # Load seen IDs to avoid duplicates
    last_add = time.time()
    last_prune = time.time()  # Initialize last prune time

    while True:
        try:
            target_subreddits = "+".join(subreddits)
            sub = r.subreddit(target_subreddits)
            logging.info(f"Starting stream for: {target_subreddits}")
            for post in sub.stream.submissions(skip_existing=True, pause_after=3):
                if post is None:  # No new posts
                    logging.debug("⏳ No new posts, waiting...")
                    time.sleep(30)
                    continue
                logging.info(f"📝 New post in r/{post.subreddit}: {post.title[:50]}...")
                if post.id in seen_ids:
                    # If the post ID is already seen, skip it
                    continue

                #Combine the title and selftext for keyword matching and check if any keyword is present
                combined_text = (post.title + " " + (post.selftext or "")).lower()
                if any(keyword.lower() in combined_text for keyword in keywords):
                    # If any keyword is found in the title or selftext, add the submission to the data list
                    save_post_to_csv(post) # add to csv
                    seen_ids[post.id] = post.created_utc  # Add the post ID to the seen IDs set
                    logging.info(f"Post saved: {post.title} (ID: {post.id})")

                    # After 605 seconds add to json
                    if ((time.time() - last_add) > 605): # 10 minutes + 5s buffer
                        add_seen_ids(seen_ids)
                        last_add = time.time()
                    # Prune old IDs every day
                    if((time.time() - last_prune) > 43200):
                        seen_ids = prune_old_ids(seen_ids, max_age_days=30)
                        last_prune = time.time()
            # Sleep for a short time to avoid hitting Reddit's rate limits
            time.sleep(2)
        except KeyboardInterrupt:
            logging.info("Data collection stopped by user.")
            add_seen_ids(seen_ids)  # Save the seen IDs before exiting
            break
        except Exception as e:
            logging.error(f"Error: {e}")
            time.sleep(60)

def save_post_to_csv(post):
    # Save a single post to a CSV file.
    try: 
        filename = "data/reddit_data_v2.csv"
        with file_lock:  # Ensure thread-safe file access
            # Open the CSV file in append mode
            with open(filename, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                if f.tell() == 0:
                    writer.writeheader(["title","selftext","url","created_utc","subreddit","author"])
                writer.writerow([post.title, post.selftext, post.url, post.created_utc, str(post.subreddit), str(post.author)])
    except Exception as e:
        logging.error(f"Error saving post to CSV: {e}")


def prune_old_ids(seen_ids, max_age_days=30):
    """Remove IDs older than `max_age_days` to save memory."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    cutoff_timestamp = cutoff.timestamp()
    return {id: ts for id, ts in seen_ids.items() if ts > cutoff_timestamp}


if __name__ == "__main__":
    continuous_collection()
    #collect_data()  # Call the function to run the bot