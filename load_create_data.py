import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import collectData

def load_and_clean_data(filename):
    df = pd.read_csv(filename)
    df.drop_duplicates(subset="url", inplace=True)
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
    for kw in keywords:
        if(num_kw[kw] == 0):
            del num_kw[kw]  # Remove keywords with zero count
    return num_kw

def create_data(num_kw):
    # Create a DataFrame from the keyword counts
    df_plot = pd.DataFrame({
        "keyword": list(num_kw.keys()),
        "count": list(num_kw.values())
    }).sort_values(by="count", ascending=True)

    # Plot setup
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 8))
    colors = sns.color_palette("viridis", len(df_plot))

    sns.barplot(
        data=df_plot,
        x="count",
        y="keyword",
        hue="keyword",       # tell seaborn to map color by keyword
        palette=colors,
        dodge=False,          # prevent weird bar splitting
        orient='h'
    )
    plt.legend([], [], frameon=False)  # removes the legend

    # Styling
    plt.xlabel("Keyword", color="darkgray")
    plt.ylabel("Number of Mentions", color="darkgray")
    plt.title("Frequency of Keywords in Subreddits", color="darkgray")
    plt.xticks(rotation=45, ha="right", size=14, color="darkgray")
    plt.yticks(size=14, color="darkgray")
    plt.tight_layout()
    sns.despine(left=True)

    # Save to file
    plt.savefig("plot.png", dpi=300)

def count_subreddits(df):
    print(list(df["subreddit"].value_counts()))


  
def main():
    df = load_and_clean_data("data/reddit_data_v2.csv")
    df = combine_text_fields(df)
    keyword_counts = count_kw(df, collectData.keywords)
    count_subreddits(df)
    create_data(keyword_counts)

if __name__ == "__main__":
    main()