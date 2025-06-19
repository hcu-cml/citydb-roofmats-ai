import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_training_metrics(csv_file):
    # Set seaborn style and fonts for scientific plots
    sns.set(style="whitegrid", context="talk", font_scale=1.2)
    plt.rcParams["font.family"] = "serif"

    # Load CSV
    df = pd.read_csv(csv_file)

    # Columns
    epoch = df['epoch']
    losses_train = ['train/box_loss', 'train/cls_loss', 'train/dfl_loss']
    losses_val = ['val/box_loss', 'val/cls_loss', 'val/dfl_loss']
    metrics = ['metrics/precision(B)', 'metrics/recall(B)', 'metrics/mAP50(B)', 'metrics/mAP50-95(B)']

    # Create figure
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Training Progress Overview", fontsize=20, fontweight='bold')

    # Define color palette
    palette = sns.color_palette("Set2", n_colors=4)

    # Plot training losses
    for i, col in enumerate(losses_train):
        sns.lineplot(x=epoch, y=df[col], ax=axs[0, 0], label=col.split('/')[-1], linewidth=2)
    axs[0, 0].set_title("Training Losses")
    axs[0, 0].set_xlabel("Epoch")
    axs[0, 0].set_ylabel("Loss")

    # Plot validation losses
    for i, col in enumerate(losses_val):
        sns.lineplot(x=epoch, y=df[col], ax=axs[0, 1], label=col.split('/')[-1], linewidth=2)
    axs[0, 1].set_title("Validation Losses")
    axs[0, 1].set_xlabel("Epoch")
    axs[0, 1].set_ylabel("Loss")

    # Plot metrics
    for i, col in enumerate(metrics):
        sns.lineplot(x=epoch, y=df[col], ax=axs[1, 0], label=col.split('/')[-1], linewidth=2)
    axs[1, 0].set_title("Evaluation Metrics")
    axs[1, 0].set_xlabel("Epoch")
    axs[1, 0].set_ylabel("Score")

    # Hide unused subplot
    axs[1, 1].axis("off")

    # General layout tweaks
    for ax in axs.flat:
        ax.legend()
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Save
    fig.savefig("./figures/training_metrics.pdf", format='pdf', dpi=300, bbox_inches='tight')
    fig.savefig("./figures/training_metrics.png", format='png', dpi=300, bbox_inches='tight')

    plt.show()

plot_training_metrics("./results.csv")

