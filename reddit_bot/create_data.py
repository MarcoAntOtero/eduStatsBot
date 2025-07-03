import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
from datetime import date

def create_data(type='',number_data_points=5):
    # Load keyword counts from a JSON file
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

    # Save to file
    current_date = date.today()
    if(type == 'kw'):
        # Styling
        plt.xlabel("Number of Mentions", color="#323232", size = 16)
        plt.ylabel("Keyword", color="#323232", size = 16)
        plt.title("Frequency of Keywords in Subreddits", color="#323232", size = 20)
        plt.tight_layout() # has to be here, otherwise graph gets clipped
        plt.savefig(f"created_data/{current_date}_kw.png", dpi=300)
    elif(type == 'subreddit'):
        plt.xlabel("Number of Keywords", color="#323232", size = 16)
        plt.ylabel("Subreddits", color="#323232", size = 16)
        plt.title("Frequency of Keywords in Subreddits", color="#323232", size = 20)
        plt.tight_layout()
        plt.savefig(f"created_data/{current_date}_subreddit.png", dpi=300)
    else:
        print("Error has occured")

if __name__ == "__main__":

    create_data(type='kw', number_data_points=10)
    # create_data(num_kw, type='subreddit', number_data_points=5) Uncomment to create subreddit plot