"""
Task 3: Food Delivery Visualisation Dashboard
Assessment: M4-A1 | Program: Data Science
Domain: Multi-panel Exploratory Visualisation using Matplotlib & Seaborn
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Import data cleaning pipeline from Task 2 to obtain cleaned data
from task2_pandas_cleaning import create_raw_orders_dataset, run_cleaning_pipeline

def generate_dashboard(df: pd.DataFrame, output_path: str = "food_delivery_dashboard.png"):
    print("=" * 75)
    print("       TASK 3: FOOD DELIVERY MULTI-PANEL VISUALISATION DASHBOARD")
    print("=" * 75)

    # Set overall aesthetic style
    sns.set_theme(style="whitegrid", font="sans-serif")
    
    # Create 2x2 subplot figure as specified
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Food Delivery Operations & Performance Dashboard", fontsize=18, fontweight='bold', y=0.995)

    # -------------------------------------------------------------
    # Plot 1 (Top-Left): Seaborn Countplot - Order Count per Category
    # -------------------------------------------------------------
    category_order = df['category'].value_counts().index
    palette_cat = sns.color_palette("mako", n_colors=len(category_order))
    
    sns.countplot(
        data=df, 
        x='category', 
        order=category_order, 
        ax=axes[0, 0], 
        palette=palette_cat,
        hue='category',
        legend=False
    )
    axes[0, 0].set_title("Plot 1: Total Order Volume by Cuisine Category", fontsize=13, fontweight='bold', pad=10)
    axes[0, 0].set_xlabel("Restaurant Category / Cuisine", fontsize=11, fontweight='semibold')
    axes[0, 0].set_ylabel("Number of Completed Orders", fontsize=11, fontweight='semibold')
    axes[0, 0].grid(axis='y', linestyle='--', alpha=0.5)

    # Add direct data labels above each bar
    for p in axes[0, 0].patches:
        height = p.get_height()
        if not np.isnan(height) and height > 0:
            axes[0, 0].annotate(f"{int(height)}",
                                (p.get_x() + p.get_width() / 2., height),
                                ha='center', va='bottom', fontsize=10, fontweight='bold',
                                xytext=(0, 3), textcoords='offset points')

    # -------------------------------------------------------------
    # Plot 2 (Top-Right): Seaborn Boxplot - Delivery Time by Category
    # -------------------------------------------------------------
    sns.boxplot(
        data=df, 
        x='category', 
        y='delivery_time_mins', 
        order=category_order,
        ax=axes[0, 1], 
        palette="crest",
        hue='category',
        legend=False,
        showmeans=True,
        meanprops={"marker":"o", "markerfacecolor":"red", "markeredgecolor":"black", "markersize":"6"}
    )
    axes[0, 1].set_title("Plot 2: Delivery Time Distribution by Category", fontsize=13, fontweight='bold', pad=10)
    axes[0, 1].set_xlabel("Restaurant Category / Cuisine", fontsize=11, fontweight='semibold')
    axes[0, 1].set_ylabel("Delivery Time (Minutes)", fontsize=11, fontweight='semibold')
    axes[0, 1].grid(axis='y', linestyle='--', alpha=0.5)

    # -------------------------------------------------------------
    # Plot 3 (Bottom-Left): Matplotlib Horizontal Bar Chart - Avg Order Value per Restaurant
    # -------------------------------------------------------------
    avg_order_val = df.groupby('restaurant_name')['order_value'].mean().sort_values(ascending=True)
    y_pos = np.arange(len(avg_order_val))
    colors_barh = plt.cm.viridis(np.linspace(0.3, 0.85, len(avg_order_val)))

    bars = axes[1, 0].barh(y_pos, avg_order_val.values, color=colors_barh, edgecolor='navy', alpha=0.85, height=0.65)
    axes[1, 0].set_yticks(y_pos)
    axes[1, 0].set_yticklabels(avg_order_val.index, fontsize=10)
    axes[1, 0].set_title("Plot 3: Average Order Value (AOV) per Restaurant", fontsize=13, fontweight='bold', pad=10)
    axes[1, 0].set_xlabel("Average Order Value (INR)", fontsize=11, fontweight='semibold')
    axes[1, 0].set_ylabel("Restaurant Partner Name", fontsize=11, fontweight='semibold')
    axes[1, 0].grid(axis='x', linestyle='--', alpha=0.5)

    # Annotate bar values
    for bar in bars:
        width = bar.get_width()
        axes[1, 0].annotate(f"INR {width:.1f}",
                            xy=(width, bar.get_y() + bar.get_height() / 2),
                            xytext=(5, 0), textcoords="offset points",
                            ha='left', va='center', fontsize=9, fontweight='bold')
    axes[1, 0].set_xlim(0, max(avg_order_val.values) * 1.15)

    # -------------------------------------------------------------
    # Plot 4 (Bottom-Right): Seaborn Correlation Heatmap of Numeric Columns
    # -------------------------------------------------------------
    numeric_cols = ['delivery_time_mins', 'order_value', 'rating']
    corr_matrix = df[numeric_cols].corr()

    sns.heatmap(
        corr_matrix, 
        annot=True, 
        fmt=".2f", 
        cmap='coolwarm', 
        vmin=-1, 
        vmax=1, 
        square=False,
        linewidths=1.5, 
        linecolor='white',
        ax=axes[1, 1],
        cbar_kws={'label': 'Pearson Correlation Coefficient'}
    )
    axes[1, 1].set_title("Plot 4: Correlation Matrix of Numeric Metrics", fontsize=13, fontweight='bold', pad=10)
    axes[1, 1].set_xlabel("Operational & Financial Metrics", fontsize=11, fontweight='semibold')
    axes[1, 1].set_ylabel("Operational & Financial Metrics", fontsize=11, fontweight='semibold')

    # Apply tight layout to prevent any overlapping of labels or titles
    plt.tight_layout()

    # Save figure as specified
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"\n[SUCCESS] Multi-panel visualization figure successfully saved to:")
    print(f"          '{os.path.abspath(output_path)}'")
    print(f"          Dimensions: 14x10 inches | Resolution: 150 DPI | bbox_inches: tight\n")
    print("=" * 75)

if __name__ == "__main__":
    raw_df = create_raw_orders_dataset()
    clean_df = run_cleaning_pipeline(raw_df)
    generate_dashboard(clean_df)
