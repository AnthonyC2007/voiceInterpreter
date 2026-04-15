import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

if __name__ == "__main__":
    df = pd.read_csv("data/features.csv")
    print(df.head())

    color_map = {
    "angry": "red",
    "happy": "green",
    "neutral": "blue",
    "sad": "orange",
    "fear": "purple",
    "disgust": "brown"
}
    colors = df["label"].map(color_map)

    fig, axes = plt.subplots(1, 3, figsize = (15, 5))

    plot_1 = axes[0].scatter(df["jitter"], df["shimmer"], c = colors, alpha = 0.5)
    axes[0].set_title("Jitter vs Shimmer")
    axes[0].set_xlabel("Jitter")
    axes[0].set_ylabel("Shimmer")

    plot_2 = axes[1].scatter(df["jitter"], df["mean_pitch"], c = colors, alpha = 0.5)
    axes[1].set_title("Jitter vs Mean Pitch")
    axes[1].set_xlabel("Jitter")
    axes[1].set_ylabel("Mean Pitch")

    plot_3 = axes[2].scatter(df["shimmer"], df["mean_pitch"], c = colors, alpha = 0.5)
    axes[2].set_title("Shimmer vs Mean Pitch")
    axes[2].set_xlabel("Shimmer")
    axes[2].set_ylabel("Mean Pitch")

    legend_handles = [mpatches.Patch(color=color, label=label) for label, color in color_map.items()]

    fig.legend(handles = legend_handles, loc = "lower center", ncol = 6)

    plt.tight_layout()
    plt.show()