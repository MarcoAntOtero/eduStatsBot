import pandas as pd
from collect import load_keywords
import json
from lock import file_lock  # Import the file lock for thread-safe file operations

def clean_and_analyze(filename):
    with file_lock:  # Ensure thread-safe file access
        df = pd.read_csv(filename)
        df.drop_duplicates(subset="url", inplace=True)
        df.fillna("",inplace=True)

        df["combined_text"] = (df["title"] + " " + df["selftext"]).str.lower()

        kw_counts = {kw.strip().lower() : 0 for kw in load_keywords()}  # Initialize counts for each keyword
        for i in df["combined_text"]:
            for keyword in kw_counts:
                if (keyword in i):
                    kw_counts[keyword] += 1
        with open("data/keyword_counts.json", "w") as f:
            json.dump(kw_counts, f, indent=4)
    
if __name__ == "__main__":
    clean_and_analyze("data/reddit_data_v2.csv")

#def count_subreddits(df):
#    return dict(zip(df["subreddit"].value_counts().keys().tolist(),df["subreddit"].value_counts().tolist()))

