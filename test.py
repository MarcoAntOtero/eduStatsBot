import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import reddit

def load_and_clean_data(filename):
    df = pd.read_csv(filename)
    df.fillna("",inplace=True)

    return df

def combine_text_fields(df):
    df["combined_text"] = (df["title"] + " " + df["selftext"]).str.lower()
    return df

def count_kw(df, keywords):
    num_kw = {}
    for kw in keywords:
        num_kw[kw] = 0
    for i in df["combined_text"]:
        for keyword in keywords:
            if (keyword in i):
                num_kw[keyword] += 1

    return num_kw

def create_data(num_kw):
    sorted_dict = dict(sorted(num_kw.items(), key=lambda item: item[1]))
    key_list = list(sorted_dict.keys())
    value_list = list(sorted_dict.values())
    
    

    plt.figure(figsize=(5, 10))
    plt.barh(key_list, value_list, color='skyblue')
    plt.xlabel("Number of Keywords")
    plt.title("Analysis of keywords in subreddits")
    plt.tight_layout()
    plt.gca().invert_yaxis()
    plt.savefig("plot.png", dpi=300)

def count_subreddits(df):
    print(df["subreddit"].value_counts())


  
def main():
    df = load_and_clean_data("data/reddit_data_v2.csv")
    df = combine_text_fields(df)
    keyword_counts = count_kw(df, reddit.keywords)
    count_subreddits(df)
    create_data(keyword_counts)

if __name__ == "__main__":
    main()