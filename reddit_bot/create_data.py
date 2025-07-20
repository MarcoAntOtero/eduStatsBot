import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
from datetime import date
from reddit_bot.lock import file_lock  # Import the file lock for thread-safe file operations

def create_weekly_data(number_data_points=5):
    # Load keyword counts from a JSON file
    with file_lock:
        with open("data/keyword_counts.json", "r") as f:
            kw_counts = json.load(f)

    #Sorted items
    kw_counts = sorted(kw_counts.items(), key=lambda item: item[1], reverse=True) # sorts dictionary by keyword value in reverse(first is highest)
    kw_downsample = kw_counts[:number_data_points]  # Get the top N keywords
    keywords = [kw[0] for kw in kw_downsample]  # Get the keywords
    counts = [kw[1] for kw in kw_downsample]  # Get the counts

    # Create a DataFrame from the keyword counts
    df_plot = pd.DataFrame({
        "keyword": keywords,
        "count": counts
    }).sort_values(by="count", ascending=True)

    # Plot setup
    sns.set(style="whitegrid")
    plt.figure(figsize=(14, 10))
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

    plt.xticks(size=12, color="#757575")
    plt.yticks(size=12, color="#757575")
    sns.despine(left=True)

    # Styling
    plt.xlabel("Number of Mentions", color="#323232", size = 16)
    plt.ylabel("Keyword", color="#323232", size = 16)
    plt.title("Frequency of Keywords in Subreddits", color="#323232", size = 20)
    plt.tight_layout() # has to be here, otherwise graph gets clipped
    plt.savefig(f"created_data/{date.today()}_kw.png", dpi=300)

def create_data_alltime():
    with file_lock:
            # Load DataFrame from the keyword counts
            df_plot = pd.read_csv("data/keywords_history.csv") 
    df_plot["total_values"] = df_plot.drop(columns=["date"], axis=1).sum(axis=1)

    # Plot setup
    plt.figure(figsize=(14, 10))
    sns.lineplot(
        data=df_plot,
        x=df_plot["date"],
        y=df_plot["total_values"],
        color="#4CAF50",
        linewidth=2.5,
        marker="o",
        markersize=8
    )
    plt.legend([], [], frameon=False)  # removes the legend
    plt.xticks(size=12, color="#757575")
    plt.yticks(size=12, color="#757575")
    sns.despine(left=True)

    plt.xlabel("Dates", color="#323232", size = 16)
    plt.ylabel("Key Word Mentions", color="#323232", size = 16)
    plt.title("Total Keyword Mentions Over Time", color="#323232", size = 20)
    plt.tight_layout()
    plt.savefig(f"created_data/{date.today()}_total_kw_mentions.png", dpi=300)

if __name__ == "__main__":
    create_weekly_data(number_data_points=10)
    create_data_alltime()