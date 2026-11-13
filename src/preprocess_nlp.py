"""
preprocess_nlp.py
Specialized Natural Language Processing (NLP) pipeline for Pakistani e-commerce
comments containing a mixture of English and Roman Urdu.
"""

import re
import string

# Curated Roman Urdu and English Stopwords
ROMAN_URDU_STOPWORDS = {
    'hai', 'hain', 'ho', 'he', 'ka', 'ke', 'ki', 'ko', 'se', 'par', 'per', 
    'me', 'mein', 'men', 'ya', 'ye', 'yeh', 'wo', 'woh', 'aur', 'or', 'tu', 
    'toh', 'to', 'bhi', 'b', 'aik', 'ek', 'ap', 'aap', 'apka', 'apki', 'apna', 
    'apni', 'hum', 'main', 'meri', 'mera', 'mere', 'sab', 'sub', 'kab', 'kahan', 
    'kidhar', 'kyun', 'q', 'kia', 'kya', 'kaisa', 'kaisi', 'kaise', 'nahi', 
    'ni', 'na', 'rha', 'rhi', 'rhe', 'raha', 'rahi', 'rahe', 'tha', 'thi', 
    'the', 'dein', 'dain', 'den', 'karo', 'kar', 'kr', 'krna', 'karna', 
    'krte', 'krta', 'krty', 'gy', 'gae', 'ga', 'gi', 'ge', 'btao', 'bta', 
    'btayein', 'batao', 'btain', 'do', 'dy', 'de', 'le', 'ly', 'lo', 'kisi', 
    'koi', 'ab', 'tak', 'kuch', 'is', 'iss', 'in', 'inn', 'us', 'uss', 'un'
}

ENGLISH_STOPWORDS = {
    'the', 'is', 'at', 'which', 'on', 'for', 'a', 'an', 'in', 'of', 'to', 
    'it', 'and', 'or', 'as', 'are', 'was', 'were', 'been', 'being', 'have', 
    'has', 'had', 'do', 'does', 'did', 'but', 'by', 'with', 'about', 'into', 
    'through', 'after', 'before', 'this', 'that', 'these', 'those', 'am', 
    'be', 'so', 'can', 'will', 'just', 'should', 'now', 'any', 'some', 'my', 
    'your', 'you', 'i', 'me', 'we', 'us', 'our', 'them', 'they', 'their'
}

ALL_STOPWORDS = ROMAN_URDU_STOPWORDS.union(ENGLISH_STOPWORDS)

# Spelling and slang normalizations
SLANG_MAP = {
    'plz': 'please',
    'pls': 'please',
    'bht': 'bohat',
    'boht': 'bohat',
    'buht': 'bohat',
    'bhot': 'bohat',
    'v': 'very',
    'vry': 'very',
    'drs': 'dress',
    'delivry': 'delivery',
    'delvry': 'delivery',
    'dlvry': 'delivery',
    'inbx': 'inbox',
    'msg': 'message',
    'availble': 'available',
    'avlbl': 'available',
    'stuf': 'stuff',
    'fabrc': 'fabric',
    'clr': 'color',
    'colr': 'color',
    'pz': 'price',
    'prc': 'price',
    'rt': 'rate',
    'chck': 'check',
    'chk': 'check',
    'ur': 'your',
    'u': 'you',
    'r': 'are'
}

def clean_text(text):
    if not isinstance(text, str):
        return ""
    
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # 3. Remove non-ASCII characters & emojis
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # 4. Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # 5. Tokenize & normalize slangs
    words = text.split()
    normalized_words = [SLANG_MAP.get(w, w) for w in words]
    
    # 6. Remove stopwords
    filtered_words = [w for w in normalized_words if w not in ALL_STOPWORDS and len(w) > 1]
    
    return " ".join(filtered_words)

if __name__ == '__main__':
    sample = "Plz inbox price details! Bht mehnga suit hai yar, delivery Karachi kitne din me hogi?"
    print("Sample:", sample)
    print("Cleaned:", clean_text(sample))
