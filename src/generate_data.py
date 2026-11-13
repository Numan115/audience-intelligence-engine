"""
generate_data.py
Simulates realistic Pakistani fashion social media posts and comments dataset
for Project 3: Pakistan Social Audience & Campaign Intelligence Engine.

Creates:
- Table A: data/posts.csv (2,000 public posts)
- Table B: data/comments.csv (8,000 public comments in Roman Urdu / English)
All simulated records are tagged with data_source='simulated'.
"""

import os
import random
import numpy as np
import pandas as pd

def generate_pakistani_fashion_data(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    
    print("[Dataset Engine] Generating Table A: Social Media Posts (2,000 records)...")
    
    brands = [
        'Sapphire', 'Khaadi', 'Gul Ahmed', 'Alkaram Studio', 
        'Nishat Linen', 'Sana Safinaz', 'Maria.B', 'Asim Jofa'
    ]
    brand_weights = [0.18, 0.18, 0.15, 0.14, 0.12, 0.09, 0.08, 0.06]
    
    platforms = ['Instagram', 'TikTok', 'Facebook']
    platform_weights = [0.50, 0.30, 0.20]
    
    campaigns = [
        'Eid Collection',
        '11.11 Mega Sale',
        '12.12 Sale',
        'Summer Lawn Vol 1',
        'Winter Khaddar'
    ]
    
    content_types = [
        'Reel',
        'Product Photo',
        'Influencer Post',
        'Styling Video',
        'Sale Announcement'
    ]
    
    base_multipliers = {
        'Reel': 1.6,
        'Influencer Post': 1.3,
        'Styling Video': 1.1,
        'Sale Announcement': 1.0,
        'Product Photo': 0.8
    }
    
    # Authentic Pakistani fashion comment topics and texts (Roman Urdu + English)
    topics_dict = {
        "Price inquiry": [
            "Price please?",
            "Price kya hai is suit ki?",
            "Rate bata dein please",
            "Kitne ka hai ye suit?",
            "Price?"
        ],
        "Price complaint": [
            "Price bohat zyada hai yar, lawn suit itna mehnga!",
            "Itna mehnga kyun hai?",
            "Too expensive for an unstitched lawn suit",
            "Rate bohat high hai honestly, not worth it"
        ],
        "Discount": [
            "Any discount on this suit?",
            "Sale kab lag rahi hai?",
            "Discount code hai koi?",
            "11.11 pe kitna off hoga?",
            "Is there any promo code available?"
        ],
        "Delivery": [
            "Delivery kitne din mein hogi Lahore mein?",
            "Ordered last week, still waiting! Very slow service",
            "Order abhi tak nahi pohancha, tracking id dein",
            "Is Cash on Delivery (COD) available for Karachi?",
            "Delivery charges kitne hain Karachi ke?"
        ],
        "Availability": [
            "Is this available in Karachi store?",
            "Stock mein hai ya out of stock?",
            "Medium size available hai?",
            "Please restock this article! Missed it during sale",
            "Large size restock kab hoga?"
        ],
        "Fabric": [
            "Fabric kaisa hai? Pure lawn hai ya mixed?",
            "Is the dupatta pure silk or chiffon?",
            "Quality achi hai ya nahi?",
            "Colour fade to nahi hota wash ke baad?",
            "Fabric stuff kaisa hai?"
        ],
        "Praise": [
            "Very beautiful dress! Loved the color",
            "Bohat hi pyara design hai mashallah!",
            "Love this collection as always",
            "Gorgeous styling and elegant embroidery"
        ],
        "Inbox request": [
            "Inbox me details send kar dein",
            "DM details please",
            "Inbox kardo price aur fabric details",
            "Book this piece for me, check inbox"
        ]
    }
    
    def get_topic_weights(ctype, camp):
        w = {k: 1.0 for k in topics_dict}
        if "Sale" in camp or ctype == "Sale Announcement":
            w["Discount"] *= 3.5
            w["Price complaint"] *= 1.8
        if ctype == "Influencer Post":
            w["Praise"] *= 3.0
            w["Inbox request"] *= 2.2
        if ctype == "Product Photo":
            w["Fabric"] *= 2.8
            w["Availability"] *= 2.2
        if camp == "Eid Collection":
            w["Delivery"] *= 2.5
            w["Availability"] *= 1.8
        return w

    num_posts = 2000
    posts = []
    comments = []
    
    for i in range(1, num_posts + 1):
        pid = f"P{i:04d}"
        brand = np.random.choice(brands, p=brand_weights)
        platform = np.random.choice(platforms, p=platform_weights)
        camp = random.choice(campaigns)
        ct = random.choice(content_types)
        days_since = random.randint(1, 30)
        
        base = base_multipliers[ct]
        views = int(np.random.lognormal(10, 0.6) * base)
        likes = int(views * np.random.uniform(0.02, 0.06) * base)
        cc = int(views * np.random.uniform(0.002, 0.008) * base)
        shares = int(views * np.random.uniform(0.001, 0.005))
        
        # Inject realistic anomalies (~3.5% of posts)
        # e.g., viral reach with high comments/complaints or high likes/low shares
        is_anomaly = False
        if random.random() < 0.035:
            is_anomaly = True
            choice = random.choice(['viral_burst', 'comment_surge', 'low_engagement'])
            if choice == 'viral_burst':
                likes = int(likes * random.uniform(3.5, 6.0))
                views = int(views * random.uniform(2.5, 4.0))
            elif choice == 'comment_surge':
                cc = int(cc * random.uniform(4.0, 7.5)) # customer complaint surge
            else:
                likes = max(5, int(likes * 0.15))
                views = max(100, int(views * 0.25))

        likes = max(15, likes)
        cc = max(5, cc)
        shares = max(1, shares)
        views = max(likes * 5, views)

        posts.append({
            'post_id': pid,
            'brand': brand,
            'platform': platform,
            'campaign': camp,
            'content_type': ct,
            'product_category': "Lawn suit",
            'likes': likes,
            'comments_count': cc,
            'shares': shares,
            'views': views,
            'days_since_post': days_since,
            'data_source': 'simulated'
        })
        
        # Generate 4 associated comments per post = 8,000 comments total
        tw = get_topic_weights(ct, camp)
        topic_keys = list(tw.keys())
        topic_weights = list(tw.values())
        
        for _ in range(4):
            t = random.choices(topic_keys, weights=topic_weights)[0]
            txt = random.choice(topics_dict[t])
            
            # Determine language type
            is_english = txt.isascii() and any(x in txt for x in [
                "Price please", "Any discount", "Is this", "Very beautiful", 
                "DM", "Too expensive", "Ordered", "Love", "Is it", "Is there"
            ])
            lang = "English" if is_english else "Roman Urdu"
            if "please" in txt.lower() and ("kya" in txt or "bata" in txt or "kitne" in txt):
                lang = "Mixed"
                
            comments.append({
                'post_id': pid,
                'comment_text': txt,
                'true_topic': t,
                'language_type': lang,
                'data_source': 'simulated'
            })
            
    df_posts = pd.DataFrame(posts)
    df_comments = pd.DataFrame(comments)
    
    # Save to data/ (standard) and data/raw/
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'raw'), exist_ok=True)
    
    # Save standard posts.csv & comments.csv
    df_posts.to_csv(os.path.join(base_dir, 'posts.csv'), index=False)
    df_comments.to_csv(os.path.join(base_dir, 'comments.csv'), index=False)
    
    # Save raw mirrors
    df_posts.to_csv(os.path.join(base_dir, 'raw', 'posts_raw.csv'), index=False)
    df_comments.to_csv(os.path.join(base_dir, 'raw', 'comments_raw.csv'), index=False)
    
    print(f"\n[Generated Successfully]")
    print(f" -> {os.path.join(base_dir, 'posts.csv')} ({len(df_posts):,} posts)")
    print(f" -> {os.path.join(base_dir, 'comments.csv')} ({len(df_comments):,} comments)")
    return df_posts, df_comments

if __name__ == '__main__':
    generate_pakistani_fashion_data()
