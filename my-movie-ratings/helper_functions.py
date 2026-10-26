"""
helper_functions.py - Reusable utilities for Movie Ratings Analysis
Author: Atharv Chaudhari
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_bayesian_rating(df, rating_col='imdb_score', vote_col='vote_count', m=15000):
    """
    Computes IMDb Weighted Formula:
    WR = (v / (v + m)) * R + (m / (v + m)) * C
    where:
      R = average rating of the movie
      v = number of votes for the movie
      m = minimum votes required to be listed in the top chart
      C = the mean vote across the whole dataset
    """
    C = df[rating_col].mean()
    v = df[vote_col]
    R = df[rating_col]
    return ((v / (v + m)) * R + (m / (v + m)) * C).round(2)

def normalize_ratings(series):
    """Min-Max normalizes ratings to scale [0, 1]"""
    return ((series - series.min()) / (series.max() - series.min())).round(3)

def plot_genre_ratings(df, output_path='plot.png'):
    """Generates comparison bar chart of IMDb score vs Bayesian rating"""
    df_sorted = df.sort_values(by='bayesian_weighted_score', ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=150)
    x = np.arange(len(df_sorted))
    width = 0.38
    
    b1 = ax.bar(x - width/2, df_sorted['imdb_score'], width, label='Raw IMDb Score', color='#6366F1', alpha=0.9)
    b2 = ax.bar(x + width/2, df_sorted['bayesian_weighted_score'], width, label='Bayesian Weighted Score', color='#10B981', alpha=0.9)
    
    ax.set_ylabel('Rating (0 - 10 Scale)', fontsize=11, fontweight='bold')
    ax.set_title('Task 4: Movie Ratings Analysis — Raw IMDb vs Bayesian Weighted Rating', fontsize=12, fontweight='bold', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(df_sorted['title'], rotation=35, ha='right', fontsize=9, fontweight='bold')
    ax.set_ylim(4, 10.2)
    ax.legend(frameon=True, facecolor='white', framealpha=0.95)
    ax.grid(axis='y', linestyle='--', alpha=0.35)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Generated plot saved to: {output_path}")
