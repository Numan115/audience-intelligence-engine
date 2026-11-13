"""
generate_data.py
Simulates realistic Pakistani fashion social media posts and comments dataset
for Project 3: Pakistan Social Audience & Campaign Intelligence Engine.

Creates:
- Table A: data/raw/posts_raw.csv (2,500 public posts)
- Table B: data/raw/comments_raw.csv (10,000 public comments in Roman Urdu / English)
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_pakistani_fashion_data(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    
    print("[Dataset Engine] Generating Table A: Social Media Posts (~2,500 records)...")
    
    brands = [
        'Sapphire', 'Khaadi', 'Gul Ahmed', 'Alkaram Studio', 
        'Nishat Linen', 'Sana Safinaz', 'Maria.B', 'Asim Jofa'
    ]
    brand_weights = [0.18, 0.18, 0.15, 0.14, 0.12, 0.09, 0.08, 0.06]
    
    platforms = ['Instagram', 'TikTok', 'Facebook']
    platform_weights = [0.50, 0.30, 0.20]
    
    campaigns = [
        'Eid-ul-Fitr Festive 2024',
        'Summer Lawn Vol 1',
        '11.11 Mega Sale',
        'Blessed Friday 12.12',
        'Winter Khaddar & Linen',
        'Mid-Summer Pret Drop'
    ]
    
    content_types = [
        'Reel',
        'Product Carousel',
        'Influencer Video',
        'Static Photo',
        'Styling Video',
        'Sale Announcement'
    ]
    content_weights = [0.35, 0.25, 0.15, 0.10, 0.10, 0.05]
    
    product_categories = [
        'Unstitched 3-Piece Lawn',
        'Ready-to-Wear Stitched Pret',
        'Luxury Festive Chiffon',
        'Embroidered 2-Piece Kurti',
        'Digital Printed Lawn'
    ]
    
    num_posts = 2500
    posts = []
    
    for i in range(1, num_posts + 1):
        post_id = f"P{i:04d}"
        brand = np.random.choice(brands, p=brand_weights)
        platform = np.random.choice(platforms, p=platform_weights)
        campaign = np.random.choice(campaigns)
        content_type = np.random.choice(content_types, p=content_weights)
        product_cat = np.random.choice(product_categories)
        days_since = int(np.random.randint(1, 90))
        
        # Base price in PKR based on category
        if 'Luxury' in product_cat:
            price_pkr = int(np.random.choice([8990, 10990, 12990, 14990, 18500]))
        elif 'Stitched' in product_cat:
            price_pkr = int(np.random.choice([4990, 5990, 7490, 8990]))
        elif 'Kurti' in product_cat:
            price_pkr = int(np.random.choice([2490, 2990, 3490, 3990]))
        else: # Lawn 3-piece
            price_pkr = int(np.random.choice([3490, 3990, 4490, 4990, 5990]))
            
        # Realistic engagement dynamics by content format
        if content_type == 'Reel':
            views = int(np.random.lognormal(mean=9.8, sigma=0.8)) # ~18k avg
            likes = int(views * np.random.uniform(0.04, 0.09))
            shares = int(likes * np.random.uniform(0.08, 0.20))
            comments_count = int(likes * np.random.uniform(0.05, 0.15))
        elif content_type == 'Influencer Video':
            views = int(np.random.lognormal(mean=10.2, sigma=0.7)) # ~27k avg
            likes = int(views * np.random.uniform(0.05, 0.10))
            shares = int(likes * np.random.uniform(0.06, 0.16))
            comments_count = int(likes * np.random.uniform(0.06, 0.18))
        elif content_type == 'Sale Announcement':
            views = int(np.random.lognormal(mean=9.2, sigma=0.6))
            likes = int(views * np.random.uniform(0.03, 0.07))
            shares = int(likes * np.random.uniform(0.12, 0.30)) # highly shared
            comments_count = int(likes * np.random.uniform(0.10, 0.25)) # high inquiries
        else: # Carousel / Static / Styling
            views = int(np.random.lognormal(mean=8.9, sigma=0.7))
            likes = int(views * np.random.uniform(0.03, 0.06))
            shares = int(likes * np.random.uniform(0.03, 0.08))
            comments_count = int(likes * np.random.uniform(0.03, 0.09))
            
        # Ensure minimums
        likes = max(15, likes)
        comments_count = max(5, comments_count)
        shares = max(1, shares)
        views = max(likes * 5, views)
        
        posts.append({
            'post_id': post_id,
            'brand': brand,
            'platform': platform,
            'campaign': campaign,
            'content_type': content_type,
            'product_category': product_cat,
            'price_pkr': price_pkr,
            'likes': likes,
            'comments_count': comments_count,
            'shares': shares,
            'views': views,
            'days_since_post': days_since
        })
        
    df_posts = pd.DataFrame(posts)
    
    print("\n[Dataset Engine] Generating Table B: Social Media Comments (~10,000 records)...")
    
    # Archetype comment templates covering authentic Pakistani shopping interactions
    comment_archetypes = [
        # 1. Price Inquiries & Price Sensitivity
        {"text": "Price please?", "lang": "English", "topic": "Price Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Price kya hai is suit ki?", "lang": "Roman Urdu", "topic": "Price Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Price bohat zyada hai yar, lawn suit itna mehnga!", "lang": "Roman Urdu", "topic": "Price Resistance", "intent": "Feedback", "sentiment": "Negative"},
        {"text": "Overpriced honestly, quality doesn't justify this rate", "lang": "English", "topic": "Price Resistance", "intent": "Feedback", "sentiment": "Negative"},
        {"text": "Plz inbox price details and discount code", "lang": "Mixed", "topic": "Price Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Any discount on this article?", "lang": "English", "topic": "Price Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Sale mein kitne ka milega ye?", "lang": "Roman Urdu", "topic": "Price Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Rate bta dain plz", "lang": "Roman Urdu", "topic": "Price Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        
        # 2. Delivery, Logistics & City Inquiries
        {"text": "Delivery kitne din mein hogi Lahore mein?", "lang": "Roman Urdu", "topic": "Delivery Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Is Cash on Delivery (COD) available for Karachi?", "lang": "Mixed", "topic": "Delivery Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Ordered last week, still waiting for delivery! Very slow service", "lang": "English", "topic": "Delivery Delay", "intent": "Complaint", "sentiment": "Negative"},
        {"text": "Peshawar delivery charges kitne hain?", "lang": "Roman Urdu", "topic": "Delivery Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Tracking number kab tak aega? 5 days ho gye hain", "lang": "Roman Urdu", "topic": "Delivery Delay", "intent": "Complaint", "sentiment": "Negative"},
        {"text": "Do you offer urgent 1-day delivery in Islamabad / Rawalpindi?", "lang": "English", "topic": "Delivery Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Faisalabad delivery kitne time me hoti hai?", "lang": "Roman Urdu", "topic": "Delivery Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Parcel received today, on-time delivery thank you!", "lang": "English", "topic": "Delivery Praise", "intent": "Feedback", "sentiment": "Positive"},

        # 3. Product Details, Fabric & Material Quality
        {"text": "Fabric stuff kaisa hai? Pure lawn hai ya mixed?", "lang": "Roman Urdu", "topic": "Fabric Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Is the dupatta pure silk or chiffon?", "lang": "English", "topic": "Fabric Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Color fade toh nahi hoga after first wash?", "lang": "Roman Urdu", "topic": "Quality Concern", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Fabric is sheer or see-through? Need unstitched details", "lang": "English", "topic": "Fabric Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Embroidery thread work hai ya printed?", "lang": "Roman Urdu", "topic": "Fabric Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Very poor fabric quality, rough stuff, not worth buying", "lang": "English", "topic": "Quality Complaint", "intent": "Complaint", "sentiment": "Negative"},
        {"text": "Quality was top notch! Original lawn fabric, loved it", "lang": "English", "topic": "Quality Praise", "intent": "Feedback", "sentiment": "Positive"},

        # 4. Sizing, Availability & Restock
        {"text": "Is Medium size available in this color?", "lang": "English", "topic": "Sizing Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Small size out of stock dikha raha hai, restock kab hoga?", "lang": "Roman Urdu", "topic": "Stock Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Plus size / XL stitching option hai kya?", "lang": "Mixed", "topic": "Sizing Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Please restock this article! Missed it during sale", "lang": "English", "topic": "Stock Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Unstitched available hai ya only ready to wear?", "lang": "Roman Urdu", "topic": "Stock Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},
        {"text": "Size chart send kar dain please", "lang": "Roman Urdu", "topic": "Sizing Inquiry", "intent": "Inquiry", "sentiment": "Neutral"},

        # 5. Purchase Intent & Direct Ordering
        {"text": "How can I order this? Website link please", "lang": "English", "topic": "Purchase Intent", "intent": "High Intent", "sentiment": "Positive"},
        {"text": "Book one piece for me in Medium, check DM", "lang": "English", "topic": "Purchase Intent", "intent": "High Intent", "sentiment": "Positive"},
        {"text": "Mera order confirm kar dein, details inbox kardi hain", "lang": "Roman Urdu", "topic": "Purchase Intent", "intent": "High Intent", "sentiment": "Positive"},
        {"text": "Want to buy 2 suits, any bundle offer?", "lang": "English", "topic": "Purchase Intent", "intent": "High Intent", "sentiment": "Positive"},
        {"text": "Plz book this dress for me urgently", "lang": "Mixed", "topic": "Purchase Intent", "intent": "High Intent", "sentiment": "Positive"},

        # 6. Aesthetic Praise & Brand Appreciation
        {"text": "Bohat hi pyara design hai, mashallah!", "lang": "Roman Urdu", "topic": "Appreciation", "intent": "Casual", "sentiment": "Positive"},
        {"text": "Gorgeous color combination! Loved the reel", "lang": "English", "topic": "Appreciation", "intent": "Casual", "sentiment": "Positive"},
        {"text": "Zabardast collection as always", "lang": "Roman Urdu", "topic": "Appreciation", "intent": "Casual", "sentiment": "Positive"},
        {"text": "Stunning model and elegant styling", "lang": "English", "topic": "Appreciation", "intent": "Casual", "sentiment": "Positive"},
        {"text": "Disappointed with customer support, no one replies to DMs", "lang": "English", "topic": "Customer Support", "intent": "Complaint", "sentiment": "Negative"}
    ]
    
    comments = []
    num_comments = 10000
    
    # Sample posts proportionally to comments_count
    all_post_ids = df_posts['post_id'].values
    
    # We assign comments across posts
    comment_id_counter = 1
    for _ in range(num_comments):
        p_id = random.choice(all_post_ids)
        arch = random.choice(comment_archetypes)
        
        # Slight variation in comment text to simulate organic human typing
        text = arch['text']
        if random.random() < 0.25:
            # Add emojis or variations
            emojis = [" ❤️", " 😍", " ✨", " 🙏", " !!", "...", " 🔥", " 👗"]
            text += random.choice(emojis)
        if random.random() < 0.15:
            text = text.lower()
            
        comments.append({
            'comment_id': f"C{comment_id_counter:05d}",
            'post_id': p_id,
            'comment_text': text,
            'language_type': arch['lang'],
            'reference_topic': arch['topic'],
            'reference_intent': arch['intent'],
            'reference_sentiment': arch['sentiment']
        })
        comment_id_counter += 1
        
    df_comments = pd.DataFrame(comments)
    
    # Save files to Project_3/data/raw/
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
    os.makedirs(out_dir, exist_ok=True)
    
    posts_path = os.path.join(out_dir, 'posts_raw.csv')
    comments_path = os.path.join(out_dir, 'comments_raw.csv')
    
    df_posts.to_csv(posts_path, index=False)
    df_comments.to_csv(comments_path, index=False)
    
    print(f"\n[Done] Successfully generated:")
    print(f" -> Table A: {posts_path} ({len(df_posts):,} posts)")
    print(f" -> Table B: {comments_path} ({len(df_comments):,} comments)")
    print("\nTable A Preview:")
    print(df_posts.head(3))
    print("\nTable B Preview:")
    print(df_comments.head(3))
    
    return df_posts, df_comments

if __name__ == '__main__':
    generate_pakistani_fashion_data()
