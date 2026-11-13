"""
generate_visualizations.py
Phase 1 Visualizations for Project 3:
- 01_comment_cluster_distribution.png (Audience Need Breakdown)
- 02_brand_audience_needs_heatmap.png (Brand vs Audience Inquiry Topics)
- 03_content_type_engagement.png (Reel vs Carousel vs Influencer Performance)
- 04_language_distribution.png (Roman Urdu vs English vs Mixed)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid')
plt.rcParams['font.sans-serif'] = 'Arial'

def create_phase1_visualizations(processed_dir='Project_3/data/processed',
                                 vis_dir='Project_3/visualizations'):
    os.makedirs(vis_dir, exist_ok=True)
    
    comments_path = os.path.join(processed_dir, 'comments_clustered.csv')
    posts_path = os.path.join(processed_dir, 'posts_cleaned.csv')
    
    if not os.path.exists(comments_path):
        print(f"File not found: {comments_path}. Run audience_clustering.py first.")
        return
        
    df_comments = pd.read_csv(comments_path)
    df_posts = pd.read_csv(posts_path)
    
    # 1. Comment Cluster Distribution
    plt.figure(figsize=(10, 6))
    cluster_counts = df_comments['cluster_name'].value_counts().reset_index()
    cluster_counts.columns = ['Audience_Need', 'Count']
    palette = ['#2b5c8f', '#4ca585', '#d4a373', '#e76f51', '#3a86ff', '#9b5de5']
    ax = sns.barplot(data=cluster_counts, y='Audience_Need', x='Count', palette=palette)
    plt.title('Discovered Audience Need Clusters in Pakistani Fashion Comments', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Number of Comments', fontsize=12)
    plt.ylabel('Audience Need / Intent Cluster', fontsize=12)
    total = len(df_comments)
    for p in ax.patches:
        w = p.get_width()
        pct = (w / total) * 100
        ax.annotate(f"{int(w):,} ({pct:.1f}%)",
                    (w, p.get_y() + p.get_height() / 2.),
                    ha='left', va='center', fontsize=10, fontweight='bold', xytext=(5, 0),
                    textcoords='offset points')
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, '01_comment_cluster_distribution.png'), dpi=300)
    plt.close()

    # 2. Brand vs Audience Needs Heatmap
    plt.figure(figsize=(11, 7))
    merged = df_comments.merge(df_posts[['post_id', 'brand']], on='post_id', how='left')
    pivot_brand = pd.crosstab(merged['brand'], merged['cluster_name'], normalize='index') * 100
    sns.heatmap(pivot_brand, annot=True, fmt='.1f', cmap='YlGnBu', cbar_kws={'label': '% of Brand Comments'})
    plt.title('Audience Inquiry Profiles Across Pakistani Fashion Brands (%)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Audience Need Category', fontsize=12)
    plt.ylabel('Brand', fontsize=12)
    plt.xticks(rotation=25, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, '02_brand_audience_needs_heatmap.png'), dpi=300)
    plt.close()

    # 3. Content Type vs Engagement Rate
    plt.figure(figsize=(10, 6))
    content_eng = df_posts.groupby('content_type').agg(
        avg_eng=('engagement_rate', 'mean'),
        avg_views=('views', 'mean')
    ).sort_values(by='avg_eng', ascending=False).reset_index()
    
    ax = sns.barplot(data=content_eng, x='content_type', y='avg_eng', palette='viridis')
    plt.title('Engagement Rate (%) by Social Content Type', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Content Format', fontsize=12)
    plt.ylabel('Average Engagement Rate (%)', fontsize=12)
    plt.xticks(rotation=15)
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f}%",
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=10, fontweight='bold', xytext=(0, 4),
                    textcoords='offset points')
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, '03_content_type_engagement.png'), dpi=300)
    plt.close()

    # 4. Language Type Distribution
    plt.figure(figsize=(7, 7))
    lang_counts = df_comments['language_type'].value_counts()
    colors = ['#2b5c8f', '#4ca585', '#d4a373']
    plt.pie(lang_counts, labels=lang_counts.index, autopct='%1.1f%%', startangle=140,
            colors=colors, explode=[0.04, 0.04, 0.04], wedgeprops=dict(width=0.6))
    plt.title('Comment Language Breakdown (Roman Urdu vs English)', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, '04_language_distribution.png'), dpi=300)
    plt.close()

    print(f"Generated 4 Phase-1 visualizations successfully inside: {vis_dir}")

if __name__ == '__main__':
    create_phase1_visualizations()
