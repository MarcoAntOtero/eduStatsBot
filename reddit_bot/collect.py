import config
import csv
import json 

def load_keywords():
    # Load keywords from a JSON file or define them directly in the code.
    try:
        with open("data/keywords.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Keywords file not found. Using default keywords.")
        # If the file is not found, use the default keywords defined below.
        return ("burnt out", "mental breakdown", "can't focus", "cannot focus", "overwhelmed", "lose my mind")
def load_seen_ids():
    # Load seen IDs from a JSON file or define them directly in the code.
    try:
        with open("data/seen_ids.json", "r", encoding="utf-8") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()
def add_seen_ids(post):
    try:
        with open("data/seen_ids.json", "w") as f:
            json.dump(post, f, indent=4)
    except FileNotFoundError:
        print("Seen IDs file not found.")

subreddits = ["GenZ","college","highschool","Adulting","CollegeRant","ApplyingToCollege"]


def collect_data():
    r = config.authenticateReddit()
    keywords = load_keywords()
    seen_ids = load_seen_ids()  # Load seen IDs to avoid duplicates
    # Create a list to store posts that match the keywords
    for subreddit in subreddits:

        print(f"Collecting data from subreddit: {subreddit}")

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
                seen_ids.add(post.id)  # Add the post ID to the seen IDs set
    add_seen_ids(list(seen_ids))  # Save the updated seen IDs to the file

def save_post_to_csv(post):
    # Save a single post to a CSV file.
    filename = "data/reddit_data_v2.csv"
    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        if f.tell() == 0:
            writer.writeheader(["title","selftext","url","created_utc","subreddit","author"])
        writer.writerow([post.title, post.selftext, post.url, post.created_utc, str(post.subreddit), str(post.author)])




if __name__ == "__main__":
    collect_data()  # Call the function to run the bot

'''
def save_data_to_csv(data, filename):
    # Save the collected data to a CSV file.
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename,mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ["title", "selftext", "url", "created_utc", "subreddit", "author"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader() # writes header inside data file
        for row in data:
            writer.writerow(row)

    with open("data/reddit_data_v2.json", "a", encoding='utf-8') as f:
        writer= csv.write
        json.dump(data, json_file, indent=4, ensure_ascii=False)

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
    
'''