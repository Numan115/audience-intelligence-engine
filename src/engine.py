"""
engine.py
Central Machine Learning & Intelligence Module for Project 3:
- Engagement Metrics Engine
- Content Performance Analyzer
- Roman Urdu & English Comment Clustering (TF-IDF Character N-Grams + KMeans)
- Context-Aware Isolation Forest Anomaly Detection
- Automated Marketing Decision & Recommendation Engine
"""

import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest

from preprocess_nlp import clean_text, ALL_STOPWORDS

def load_data(base_dir=None):
    if base_dir is None:
        base_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    posts_path = os.path.join(base_dir, 'posts.csv')
    comments_path = os.path.join(base_dir, 'comments.csv')
    return pd.read_csv(posts_path), pd.read_csv(comments_path)

def add_metrics(posts_df):
    p = posts_df.copy()
    views_clipped = p['views'].clip(lower=1)
    p['engagement_rate'] = ((p['likes'] + p['comments_count'] + p['shares']) / views_clipped) * 100
    p['engagement_rate'] = p['engagement_rate'].round(2)
    p['like_rate'] = ((p['likes'] / views_clipped) * 100).round(2)
    p['comment_rate'] = ((p['comments_count'] / views_clipped) * 100).round(2)
    p['share_rate'] = ((p['shares'] / views_clipped) * 100).round(2)
    return p

def content_performance(posts_df):
    p = add_metrics(posts_df)
    perf = p.groupby('content_type').agg(
        posts=('post_id', 'count'),
        avg_likes=('likes', 'mean'),
        avg_comments=('comments_count', 'mean'),
        avg_shares=('shares', 'mean'),
        avg_views=('views', 'mean'),
        avg_engagement_rate=('engagement_rate', 'mean')
    ).round(2).sort_values(by='avg_engagement_rate', ascending=False)
    return perf

def cluster_comments(comments_df, k=8, random_state=42):
    c = comments_df.copy()
    
    # Clean text using Roman Urdu stopword and slang normalizer
    c['cleaned_text'] = c['comment_text'].apply(clean_text)
    c['cleaned_text'] = c['cleaned_text'].replace('', 'inquiry')
    
    # Character n-grams (char_wb, 2-4) to robustly capture Roman Urdu spelling variations
    char_vec = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4), min_df=3)
    X_char = char_vec.fit_transform(c['cleaned_text'])
    
    km = KMeans(n_clusters=k, n_init=10, random_state=random_state)
    c['cluster'] = km.fit_predict(X_char)
    
    # Extract clean top terms using word-level TF-IDF excluding Roman Urdu and English stopwords
    word_vec = TfidfVectorizer(stop_words=list(ALL_STOPWORDS), token_pattern=r'[a-zA-Z]{3,}', min_df=2)
    
    names = {}
    for cl in range(k):
        subset = c[c['cluster'] == cl]['comment_text']
        try:
            M = word_vec.fit_transform(subset)
            top_indices = np.asarray(M.sum(0)).ravel().argsort()[::-1][:4]
            top_words = word_vec.get_feature_names_out()[top_indices]
            
            top_str = " ".join(top_words).lower()
            if any(w in top_str for w in ['price', 'mehnga', 'rate']):
                label = f"Price Inquiry & Sensitivity ({top_words[0]})"
            elif any(w in top_str for w in ['delivery', 'days', 'order', 'tracking', 'cod']):
                label = f"Delivery & Shipping Concerns ({top_words[0]})"
            elif any(w in top_str for w in ['discount', 'sale', 'off', 'code']):
                label = f"Discounts & Promotions ({top_words[0]})"
            elif any(w in top_str for w in ['fabric', 'stuff', 'lawn', 'chiffon', 'pure']):
                label = f"Fabric Quality & Specs ({top_words[0]})"
            elif any(w in top_str for w in ['size', 'medium', 'small', 'stock', 'restock']):
                label = f"Sizing & Availability ({top_words[0]})"
            elif any(w in top_str for w in ['beautiful', 'love', 'pyara', 'gorgeous', 'mashallah']):
                label = f"Brand Praise & Aesthetics ({top_words[0]})"
            elif any(w in top_str for w in ['inbox', 'dm', 'book', 'details']):
                label = f"Direct Order & Inbox Requests ({top_words[0]})"
            else:
                label = ", ".join(top_words[:3]).title()
            names[cl] = label
        except ValueError:
            names[cl] = f"Cluster {cl}"
            
    c['cluster_name'] = c['cluster'].map(names)
    return c

def find_anomalies(posts_df, contamination=0.04):
    p = add_metrics(posts_df)
    v = p['views'].clip(lower=1)
    
    # Context-aware feature matrix normalized by content_type
    features = pd.DataFrame({
        'like_r': p['likes'] / v,
        'com_r': p['comments_count'] / v,
        'share_r': p['shares'] / v,
        'log_v': np.log1p(p['views'])
    })
    
    # Compare within comparable content types (e.g. Reels against Reels)
    normalized_features = features.groupby(p['content_type']).transform(
        lambda s: (s - s.mean()) / (s.std() + 1e-9)
    )
    
    iso = IsolationForest(contamination=contamination, random_state=42)
    p['anomaly'] = iso.fit_predict(normalized_features) == -1
    p['anomaly_score'] = (-iso.score_samples(normalized_features)).round(3)
    return p

def generate_recommendations(clustered_comments_df, perf_df):
    share = clustered_comments_df['cluster_name'].value_counts(normalize=True) * 100
    recs = []
    
    best_format = perf_df.index[0]
    worst_format = perf_df.index[-1]
    best_rate = perf_df['avg_engagement_rate'].iloc[0]
    worst_rate = perf_df['avg_engagement_rate'].iloc[-1]
    
    recs.append(
        f"**1. CONTENT STRATEGY:** '{best_format}' drives the highest average engagement ({best_rate}% vs {worst_format}'s {worst_rate}%). "
        f"Allocate 60%+ of digital creative production to {best_format}s and revamp low-performing {worst_format}s."
    )
    
    for name, pct in share.head(4).items():
        low = name.lower()
        if any(w in low for w in ['discount', 'sale', 'promo']):
            recs.append(f"**2. PROMOTION ({pct:.1f}% of inquiries):** High discount sensitivity detected. Pin flash sale promo codes and offer bundle savings (e.g. Buy 2, Get Free Delivery).")
        elif any(w in low for w in ['delivery', 'shipping', 'order', 'tracking']):
            recs.append(f"**3. CUSTOMER SERVICE ({pct:.1f}% of inquiries):** High delivery anxiety. Explicitly state city-wise delivery timelines in captions and activate automated WhatsApp order tracking.")
        elif any(w in low for w in ['price', 'rate', 'expensive']):
            recs.append(f"**4. PRICING TRANSPARENCY ({pct:.1f}% of inquiries):** Upfront pricing is critical. A/B test visible caption prices vs 'Inbox for price'; data shows hidden pricing increases friction.")
        elif any(w in low for w in ['availability', 'size', 'stock']):
            recs.append(f"**5. INVENTORY & SIZING ({pct:.1f}% of inquiries):** Fast stock-outs on Medium/Small sizes. Implement an automated 'Notify When Restocked' feature on your e-commerce store.")
        else:
            recs.append(f"**6. AUDIENCE ENGAGEMENT ({pct:.1f}% of inquiries):** Review sample comments under '{name}' to identify emerging customer preferences.")
            
    recs.append("**7. SYSTEMATIC A/B TESTING:** Test one variable per campaign (e.g. video hook duration or price in caption) to track incremental impact on conversion rates.")
    return recs
