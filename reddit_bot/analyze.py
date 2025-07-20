import pandas as pd
from reddit_bot.collect import load_keywords
import json
import os
import logging
from reddit_bot.lock import file_lock  # Import the file lock for thread-safe file operations
from datetime import datetime, timezone, timedelta

def clean_and_analyze(filename):
    with file_lock:  # Ensure thread-safe file access
        try:
            df = pd.read_csv(filename)
        except FileNotFoundError:
            logging.error(f"File not found. Error: {filename}")
            return
        df.drop_duplicates(subset="url", inplace=True)
        df.fillna("",inplace=True)

        # Reads through all csv files and dumps its into 
        all_time_counts = count_kw(df)
        with open("data/keyword_counts.json", "w") as f:
            json.dump(all_time_counts, f, indent=4)

        #weekly posts
        df["date"] = pd.to_datetime(df["created_utc"], unit="s", utc=True)
        week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        weekly_posts = df[df["date"] >= week_ago]
        weekly_counts = count_kw(weekly_posts)
        
        # Keyword Dictionary after 
        today = datetime.now().strftime("%Y-%m-%d")
        history_path = "data/keywords_history.csv"
        
        if os.path.exists(history_path):
            history_df = pd.read_csv(history_path)
        else:
            history_df = pd.DataFrame(columns=["date"] + list(weekly_counts.keys()))
    
        #New row date and each kw in dict
        new_row = {"date": today, **weekly_counts}
        #add to df and save
        history_df = pd.concat([history_df, pd.DataFrame([new_row])],ignore_index=True)
        history_df.to_csv(history_path, index=False)

        

def count_kw(df):
    df["combined_text"] = (df["title"] + " " + df["selftext"]).str.lower()
    kw_counts = {kw.strip().lower() : 0 for kw in load_keywords()}  # Initialize counts for each keyword
    for i in df["combined_text"]:
        for keyword in kw_counts:
            if (keyword in i):
                kw_counts[keyword] += 1
    return kw_counts

if __name__ == "__main__":
    clean_and_analyze("data/reddit_data_v2.csv")