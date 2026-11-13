"""
audience_clustering.py
Core Machine Learning Module for Project 3:
Performs unsupervised clustering on Pakistani social media comments
using TF-IDF Vectorization and K-Means to identify audience needs and intents.
"""

import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from preprocess_nlp import clean_text

def run_audience_clustering(raw_comments_path='../data/raw/comments_raw.csv',
                            raw_posts_path='../data/raw/posts_raw.csv',
                            output_dir='../data/processed',
                            n_clusters=6,
                            random_state=42):
    print("\n=======================================================")
    print("   AUDIENCE NEED & INTENT CLUSTERING ENGINE (PHASE 1)  ")
    print("=======================================================")
    
    # Resolve paths relative to script location if needed
    if not os.path.exists(raw_comments_path):
        base_dir = os.path.dirname(__file__)
        raw_comments_path = os.path.join(base_dir, '..', 'data', 'raw', 'comments_raw.csv')
        raw_posts_path = os.path.join(base_dir, '..', 'data', 'raw', 'posts_raw.csv')
        output_dir = os.path.join(base_dir, '..', 'data', 'processed')

    print(f"Loading comments from: {raw_comments_path}")
    df_comments = pd.read_csv(raw_comments_path)
    df_posts = pd.read_csv(raw_posts_path)
    
    print(f"Total comments loaded: {len(df_comments):,}")
    print(f"Total posts loaded: {len(df_posts):,}")
    
    # 1. Clean comment text using Roman Urdu & English NLP pipeline
    print("\n[Step 1] Preprocessing text with Roman Urdu & English normalizer...")
    df_comments['cleaned_text'] = df_comments['comment_text'].apply(clean_text)
    
    # Filter empty texts if any
    df_comments['cleaned_text'] = df_comments['cleaned_text'].replace('', 'general inquiry')
    
    # 2. TF-IDF Feature Extraction
    print("[Step 2] Vectorizing text with TF-IDF (Unigrams + Bigrams)...")
    vectorizer = TfidfVectorizer(max_features=1200, ngram_range=(1, 2), min_df=3)
    X_tfidf = vectorizer.fit_transform(df_comments['cleaned_text'])
    print(f"TF-IDF matrix shape: {X_tfidf.shape[0]} samples x {X_tfidf.shape[1]} features")
    
    # 3. K-Means Clustering
    print(f"\n[Step 3] Training K-Means model with {n_clusters} clusters...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    cluster_labels = kmeans.fit_predict(X_tfidf)
    df_comments['cluster_id'] = cluster_labels
    
    # Silhouette evaluation on sample
    sample_size = min(3000, len(df_comments))
    sil_score = silhouette_score(X_tfidf[:sample_size], cluster_labels[:sample_size])
    print(f"Silhouette Score (Sampled N={sample_size:,}): {sil_score:.3f}")
    
    # 4. Interpret Clusters via Top Keywords
    print("\n[Step 4] Extracting Top Keywords per Cluster:")
    terms = vectorizer.get_feature_names_out()
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    
    cluster_names = {}
    for i in range(n_clusters):
        top_terms = [terms[ind] for ind in order_centroids[i, :8]]
        print(f"  Cluster {i}: {', '.join(top_terms)}")
        
        # Rule-based semantic labelling based on top tokens
        top_str = " ".join(top_terms)
        if 'price' in top_str or 'mehnga' in top_str or 'rate' in top_str or 'discount' in top_str:
            cluster_names[i] = 'Price Inquiry & Sensitivity'
        elif 'delivery' in top_str or 'tracking' in top_str or 'cod' in top_str or 'waiting' in top_str:
            cluster_names[i] = 'Delivery, Shipping & Logistics'
        elif 'fabric' in top_str or 'stuff' in top_str or 'chiffon' in top_str or 'lawn' in top_str or 'pure' in top_str:
            cluster_names[i] = 'Fabric Quality & Product Specs'
        elif 'size' in top_str or 'medium' in top_str or 'small' in top_str or 'stock' in top_str or 'restock' in top_str:
            cluster_names[i] = 'Sizing & Stock Availability'
        elif 'order' in top_str or 'book' in top_str or 'confirm' in top_str or 'link' in top_str:
            cluster_names[i] = 'High-Intent Order / Booking'
        else:
            cluster_names[i] = 'Aesthetic Appreciation & Social Praise'

    df_comments['cluster_name'] = df_comments['cluster_id'].map(cluster_names)
    
    print("\n[Cluster Distribution Summary]")
    dist = df_comments['cluster_name'].value_counts()
    for name, cnt in dist.items():
        pct = (cnt / len(df_comments)) * 100
        print(f" - {name}: {cnt:,} comments ({pct:.1f}%)")
        
    # 5. Link Clustered Needs back to Table A (Posts)
    print("\n[Step 5] Aggregating audience need profiles by Post...")
    post_cluster_piv = df_comments.pivot_table(index='post_id', columns='cluster_name', 
                                               aggfunc='size', fill_value=0).reset_index()
    
    df_posts_enriched = df_posts.merge(post_cluster_piv, on='post_id', how='left').fillna(0)
    
    # Calculate Engagement Rates for Posts
    df_posts_enriched['engagement_rate'] = (
        (df_posts_enriched['likes'] + df_posts_enriched['comments_count'] + df_posts_enriched['shares']) / 
        np.maximum(1, df_posts_enriched['views'])
    ) * 100
    df_posts_enriched['engagement_rate'] = df_posts_enriched['engagement_rate'].round(2)
    
    # 6. Save Processed Datasets
    os.makedirs(output_dir, exist_ok=True)
    out_comments = os.path.join(output_dir, 'comments_clustered.csv')
    out_posts = os.path.join(output_dir, 'posts_cleaned.csv')
    
    df_comments.to_csv(out_comments, index=False)
    df_posts_enriched.to_csv(out_posts, index=False)
    
    print(f"\n[Saved] Processed datasets successfully:")
    print(f" -> {out_comments}")
    print(f" -> {out_posts}")
    
    return df_comments, df_posts_enriched

if __name__ == '__main__':
    run_audience_clustering()
